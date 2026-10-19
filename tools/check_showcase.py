"""Check the gallery's showcase: contributors' own portfolio sites (ADR-0016).

  python tools/check_showcase.py                       the files
  python tools/check_showcase.py --fetch-changed REV   also the sites added or
                                                       changed since REV (pull
                                                       requests)
  python tools/check_showcase.py --fetch-all           also every site and every
                                                       design's in_use (weekly)
  python tools/check_showcase.py --fetch-url URL [--login LOGIN]
                                                       one address's response

The files. showcase/ holds one folder per person, named by their GitHub
login in lower case, and nothing else. Each folder holds entry.json and
one screenshot, screenshot.png, .jpg, .jpeg or .webp, and nothing else.

  - entry.json: "name" (at most 80 characters), "url" (an https:// address
    of at most 300 characters, with no user name, password or port), and
    optionally "description" (one line of at most 120 characters); no
    other field; at most 4 KB.
  - The screenshot: its first bytes are the format its name says; one
    frame, never animated; landscape, wider than it is tall; between
    MIN_WIDTH and MAX_WIDTH pixels wide; at most MAX_BYTES; and no location
    in its EXIF or XMP metadata. Other metadata passes: a Mac's own
    screenshots carry EXIF and XMP blocks saying "Screenshot", and
    Windows' JPEG encoder writes an EXIF block of resolution tags
    (measured 2026-10-19).
  - No two entries list the same site; every design's "in_use" is https.

The responses, with --fetch-*: each address is fetched, never rendered or
run (the owner's decision D1 of 2026-10-18, read as never rendering on
2026-10-19). Every hop is https with its certificate verified; at most
MAX_REDIRECTS redirects; never an IP address, or a host that resolves to a
private, loopback, link-local or reserved address; TIMEOUT seconds a
request; at most READ_LIMIT bytes read. The answer must be 200 and HTML;
no hop may be a domain parking or sale service; when the site's host
changed on the way, its first PHRASE_WINDOW bytes may not say the domain is
for sale; and a showcase entry's page must link to
https://github.com/<login>, anywhere on it (ADR-0016, Q5). A 403 or 429,
as bot protection often answers a runner, is reported as "could not be
checked" for the owner to open by hand, and does not fail.

Exit 0 when everything passes; 1 when anything fails, each printed, and
listed in the job summary in GitHub Actions; 2 on a usage error. Standard
library only. --test-local, for tools/prove_checks.py only, also accepts
http:// and the loopback address for 127.0.0.1 and localhost, so the
response checks can be proven against a local server; no workflow passes
it.
"""

from __future__ import annotations

import argparse
import http.client
import ipaddress
import json
import os
import re
import socket
import ssl
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zlib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SHOWCASE = ROOT / "showcase"
DESIGNS = ROOT / "designs"

# The screenshot's limits, from the measurements of 2026-10-19 (the session
# log, Round 8): first screens of four sites at 1280x720 weighed at most
# 477 KB as PNG and 122 KB as JPEG, and at 1920x1080 at most 657 KB as PNG
# and 202 KB as JPEG. The owner's target is HD, about 1280x720 (2026-10-19).
MIN_WIDTH = 1024
MAX_WIDTH = 1920
MAX_BYTES = 500 * 1024
ENTRY_BYTES = 4 * 1024
NAME_LIMIT, URL_LIMIT, DESCRIPTION_LIMIT = 80, 300, 120
SCREENSHOTS = {"screenshot.png": "png", "screenshot.jpg": "jpeg", "screenshot.jpeg": "jpeg",
               "screenshot.webp": "webp"}
LOGIN_RE = re.compile(r"^[a-z0-9](?:[a-z0-9]|-(?=[a-z0-9])){0,38}$")
ENTRY_FIELDS = {"name", "url", "description"}

TIMEOUT = 10
MAX_REDIRECTS = 5
READ_LIMIT = 1024 * 1024
PHRASE_WINDOW = 64 * 1024
USER_AGENT = "portfolio-gallery showcase check (+https://github.com/Waqas01CP/portfolio-gallery)"
# Hosts whose business is parking or selling domains, a judgement made with
# emmabostian/developer-portfolios' parking check as precedent (read
# 2026-10-19). Hosts that also serve real sites, such as a site builder's,
# are left out: a false alarm costs a contributor more than a miss.
PARKING_HOSTS = {"sedoparking.com", "sedo.com", "parkingcrew.net", "bodis.com", "above.com",
                 "dan.com", "afternic.com", "hugedomains.com", "undeveloped.com",
                 "buydomains.com", "domainmarket.com"}
PARKING_PHRASES = ("domain is for sale", "domain for sale", "buy this domain", "make an offer",
                   "parked domain", "domain has expired", "this domain may be for sale")
LOCAL_HOSTS = {"127.0.0.1", "localhost"}
LABELS = {"ok": "ok  ", "fail": "FAIL", "unchecked": "CANNOT CHECK"}
GPS_XMP = re.compile(rb"GPS(?:Latitude|Longitude|Altitude|Coordinates|Position)|exif:GPS")


# The screenshot.

class ImageError(Exception):
    pass


def tiff_has_gps(tiff: bytes) -> bool:
    """Whether a TIFF structure, as EXIF holds one, points to GPS data."""
    order = {b"II": "<", b"MM": ">"}.get(tiff[:2])
    if order is None or len(tiff) < 8:
        raise ImageError("its EXIF block cannot be read")
    offset = struct.unpack(order + "I", tiff[4:8])[0]
    if offset + 2 > len(tiff):
        raise ImageError("its EXIF block cannot be read")
    count = struct.unpack(order + "H", tiff[offset:offset + 2])[0]
    for k in range(count):
        entry = offset + 2 + 12 * k
        if entry + 12 > len(tiff):
            raise ImageError("its EXIF block cannot be read")
        if struct.unpack(order + "H", tiff[entry:entry + 2])[0] == 0x8825:
            return True
    return False


def exif_has_gps(block: bytes) -> bool:
    return tiff_has_gps(block[6:] if block.startswith(b"Exif\0\0") else block)


def png_facts(data: bytes) -> dict:
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ImageError("its bytes are not a PNG image")
    width, height = struct.unpack(">II", data[16:24])
    facts = {"width": width, "height": height, "animated": False, "gps": False}
    pos = 8
    while pos + 8 <= len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        if len(body) < length:
            raise ImageError("its PNG chunks run past its end")
        if kind == b"acTL":
            facts["animated"] = True
        elif kind == b"eXIf":
            facts["gps"] |= exif_has_gps(body)
        elif kind in (b"tEXt", b"zTXt", b"iTXt"):
            keyword, _, rest = body.partition(b"\0")
            try:
                if kind == b"zTXt":
                    text = zlib.decompress(rest[1:])
                elif kind == b"iTXt":
                    compressed = rest[:1] == b"\1"
                    text = rest[2:].split(b"\0", 2)[-1]
                    text = zlib.decompress(text) if compressed else text
                else:
                    text = rest
            except zlib.error:
                raise ImageError("a text block in it cannot be read") from None
            if keyword.lower().startswith(b"raw profile type"):
                digits = re.sub(rb"[^0-9a-fA-F]", b"", text.split(b"\n", 3)[-1])
                try:
                    profile = bytes.fromhex(digits.decode("ascii"))
                except ValueError:
                    raise ImageError("a metadata block in it cannot be read") from None
                if b"Exif\0\0" in profile[:16]:
                    facts["gps"] |= exif_has_gps(profile[profile.index(b"Exif\0\0"):])
            facts["gps"] |= bool(GPS_XMP.search(text))
        elif kind == b"IEND":
            break
        pos += 12 + length
    return facts


SOF = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}


def jpeg_facts(data: bytes) -> dict:
    if data[:3] != b"\xff\xd8\xff":
        raise ImageError("its bytes are not a JPEG image")
    facts = {"width": None, "height": None, "animated": False, "gps": False}
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            raise ImageError("its JPEG segments cannot be read")
        marker = data[pos + 1]
        if marker == 0xFF:
            pos += 1
            continue
        if marker == 0xD8 or 0xD0 <= marker <= 0xD7 or marker == 0x01:
            pos += 2
            continue
        if marker == 0xD9:
            break
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        body = data[pos + 4:pos + 2 + length]
        if marker in SOF and len(body) >= 5:
            facts["height"], facts["width"] = struct.unpack(">HH", body[1:5])
        elif marker == 0xE1:
            if body.startswith(b"Exif\0\0"):
                facts["gps"] |= exif_has_gps(body)
            facts["gps"] |= bool(GPS_XMP.search(body))
        if marker == 0xDA:
            break
        pos += 2 + length
    if not facts["width"]:
        raise ImageError("its JPEG header gives no size")
    return facts


def webp_facts(data: bytes) -> dict:
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ImageError("its bytes are not a WebP image")
    facts = {"width": None, "height": None, "animated": False, "gps": False}
    canvas = None
    pos = 12
    while pos + 8 <= len(data):
        kind, length = struct.unpack("<4sI", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        if kind == b"VP8X" and len(body) >= 10:
            facts["animated"] |= bool(body[0] & 0x02)
            canvas = (1 + int.from_bytes(body[4:7], "little"), 1 + int.from_bytes(body[7:10], "little"))
        elif kind == b"VP8 " and len(body) >= 10 and body[3:6] == b"\x9d\x01\x2a":
            facts["width"] = struct.unpack("<H", body[6:8])[0] & 0x3FFF
            facts["height"] = struct.unpack("<H", body[8:10])[0] & 0x3FFF
        elif kind == b"VP8L" and len(body) >= 5 and body[0] == 0x2F:
            bits = int.from_bytes(body[1:5], "little")
            facts["width"], facts["height"] = (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
        elif kind in (b"ANIM", b"ANMF"):
            facts["animated"] = True
        elif kind == b"EXIF":
            facts["gps"] |= exif_has_gps(body)
        elif kind == b"XMP ":
            facts["gps"] |= bool(GPS_XMP.search(body))
        pos += 8 + length + (length & 1)
    if canvas:
        facts["width"], facts["height"] = canvas
    if not facts["width"]:
        raise ImageError("its WebP header gives no size")
    return facts


READERS = {"png": png_facts, "jpeg": jpeg_facts, "webp": webp_facts}


def screenshot_problems(path: Path, kind: str) -> list[str]:
    data = path.read_bytes()
    problems = []
    if len(data) > MAX_BYTES:
        problems.append(f"{len(data):,} bytes, over the {MAX_BYTES // 1024} KB limit: save it as "
                        f"JPEG, or at about 1280 pixels wide (docs/how-to/add-to-the-showcase.md)")
    try:
        facts = READERS[kind](data)
    except (ImageError, struct.error) as error:
        return problems + [str(error) if isinstance(error, ImageError) else "its header cannot be read"]
    width, height = facts["width"], facts["height"]
    if facts["animated"]:
        problems.append("it is animated; a screenshot is one still frame")
    if width <= height:
        problems.append(f"{width} by {height} pixels is not landscape; take the first screen "
                        f"of a desktop browser window")
    if width < MIN_WIDTH:
        problems.append(f"{width} pixels wide, under the {MIN_WIDTH}-pixel minimum")
    if width > MAX_WIDTH:
        problems.append(f"{width} pixels wide, over the {MAX_WIDTH}-pixel maximum: make it about "
                        f"1280 pixels wide (docs/how-to/add-to-the-showcase.md)")
    if facts["gps"]:
        problems.append("its metadata holds a location (GPS); save it again without it")
    return problems


# The files.

def site_key(url: str) -> str:
    parts = urlsplit(url)
    host = (parts.hostname or "").lower().removeprefix("www.")
    return host + parts.path.rstrip("/").lower()


def https_address(value) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"https://[^\s/]+\.[^\s/]+(/\S*)?", value):
        return False
    parts = urlsplit(value)
    return not (parts.username or parts.password or parts.port)


def load_entry(folder: Path, problems: list[str]) -> dict | None:
    where = f"showcase/{folder.name}/entry.json"
    path = folder / "entry.json"
    if not path.is_file() or path.is_symlink():
        problems.append(f"{where}: missing")
        return None
    if path.stat().st_size > ENTRY_BYTES:
        problems.append(f"{where}: over {ENTRY_BYTES // 1024} KB")
        return None
    try:
        entry = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        problems.append(f"{where}: not valid JSON: {error}")
        return None
    if not isinstance(entry, dict):
        problems.append(f"{where}: must be an object with name, url and an optional description")
        return None
    unknown = sorted(set(entry) - ENTRY_FIELDS)
    if unknown:
        problems.append(f"{where}: fields the format does not define: {', '.join(unknown)}")
    name, url, description = entry.get("name"), entry.get("url"), entry.get("description")
    if not (isinstance(name, str) and name.strip() and len(name) <= NAME_LIMIT and "\n" not in name):
        problems.append(f"{where}: name must be your name, one line of at most {NAME_LIMIT} characters")
    if not (https_address(url) and len(url) <= URL_LIMIT):
        problems.append(f"{where}: url must be your site's https:// address, at most {URL_LIMIT} "
                        f"characters, with no user name, password or port")
    if description is not None and not (isinstance(description, str) and description.strip()
                                        and len(description) <= DESCRIPTION_LIMIT
                                        and "\n" not in description):
        problems.append(f"{where}: description, if given, is one line of at most "
                        f"{DESCRIPTION_LIMIT} characters")
    return entry


def entries() -> list[Path]:
    return sorted(p for p in SHOWCASE.iterdir()) if SHOWCASE.is_dir() else []


def check_files() -> tuple[list[str], list[dict]]:
    """Every problem in showcase/ and the designs' in_use, and the sites to
    fetch: {"where", "url", "login"}."""
    problems: list[str] = []
    sites: list[dict] = []
    seen: dict[str, str] = {}
    for folder in entries():
        where = f"showcase/{folder.name}"
        if folder.is_symlink() or not folder.is_dir():
            problems.append(f"{where}: showcase/ holds only folders, one per person "
                            f"(docs/how-to/add-to-the-showcase.md)")
            continue
        if not LOGIN_RE.match(folder.name):
            problems.append(f"{where}/: the folder is named by your GitHub login, in lower case")
        files = sorted(p.name for p in folder.iterdir())
        shots = [n for n in files if n in SCREENSHOTS]
        for name in files:
            path = folder / name
            if path.is_symlink() or not path.is_file():
                problems.append(f"{where}/{name}: not a regular file")
            elif name != "entry.json" and name not in SCREENSHOTS:
                problems.append(f"{where}/{name}: a showcase folder holds entry.json and one "
                                f"screenshot.png, .jpg, .jpeg or .webp, and nothing else")
        if len(shots) != 1:
            problems.append(f"{where}/: {len(shots)} screenshots; it needs exactly one")
        for name in shots:
            if (folder / name).is_file() and not (folder / name).is_symlink():
                problems += [f"{where}/{name}: {p}" for p in
                             screenshot_problems(folder / name, SCREENSHOTS[name])]
        entry = load_entry(folder, problems)
        if entry and https_address(entry.get("url")):
            key = site_key(entry["url"])
            if key in seen:
                problems.append(f"{where}: lists the same site as {seen[key]}; one entry per site")
            seen[key] = where
            sites.append({"where": where, "url": entry["url"], "login": folder.name,
                          "files": f"{where}/"})
    for meta_path in sorted(DESIGNS.glob("*/design.json")):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue  # tools/check_design.py reports it
        if isinstance(meta, dict) and "in_use" in meta:
            where = f"designs/{meta_path.parent.name}/design.json"
            if https_address(meta["in_use"]):
                sites.append({"where": f"{where}, in_use", "url": meta["in_use"], "login": None,
                              "files": where})
            else:
                problems.append(f"{where}: in_use must be the https:// address of the author's "
                                f"own live site built with this design")
    return problems, sites


# The responses.

class NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirects, urllib.request.ProxyHandler({}))


class Profile(HTMLParser):
    def __init__(self, login: str) -> None:
        super().__init__(convert_charrefs=True)
        self.login, self.found = login.lower(), False

    def handle_starttag(self, tag, attrs):
        if tag not in ("a", "link", "area"):
            return
        href = (dict(attrs).get("href") or "").strip()
        parts = urlsplit(href)
        if (parts.scheme in ("http", "https") and (parts.hostname or "") in ("github.com", "www.github.com")
                and parts.path.rstrip("/").lower() == "/" + self.login):
            self.found = True


def bare(host: str) -> str:
    return host.lower().removeprefix("www.")


def parked(host: str) -> bool:
    host = host.lower().rstrip(".")
    return any(host == h or host.endswith("." + h) for h in PARKING_HOSTS)


def address_problem(host: str, port: int, test_local: bool) -> str | None:
    local = test_local and host in LOCAL_HOSTS
    try:
        literal = ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        literal = None
    if literal is not None and not (local and literal.is_loopback):
        return f"{host} is an IP address; a site is listed by its domain name"
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except (socket.gaierror, UnicodeError):
        return f"{host} does not resolve"
    for info in infos:
        address = ipaddress.ip_address(info[4][0].split("%")[0])
        if local and address.is_loopback:
            continue
        if not address.is_global:
            return f"{host} resolves to {address}, a private, loopback or reserved address"
    return None


def read_bounded(response, deadline: float) -> bytes:
    chunks, size = [], 0
    while size <= READ_LIMIT:
        if time.monotonic() > deadline:
            raise TimeoutError("the answer took too long")
        chunk = response.read(64 * 1024)
        if not chunk:
            break
        chunks.append(chunk)
        size += len(chunk)
    return b"".join(chunks)[:READ_LIMIT]


def fetch(url: str, login: str | None, test_local: bool = False, timeout: float = TIMEOUT) -> tuple[str, str]:
    """("ok" | "fail" | "unchecked", what was found)."""
    first_host = urlsplit(url).hostname or ""
    current = url
    for hop in range(MAX_REDIRECTS + 1):
        parts = urlsplit(current)
        host = parts.hostname or ""
        via = f" (reached by a redirect from {url})" if hop else ""
        local_http = test_local and parts.scheme == "http" and host in LOCAL_HOSTS
        if parts.scheme != "https" and not local_http:
            return "fail", f"{current} is not https{via}"
        if not host or parts.username or parts.password:
            return "fail", f"{current} is not an address the check can fetch{via}"
        if parked(host):
            return "fail", f"{current}: {host} is a domain parking or sale service{via}"
        problem = address_problem(host, parts.port or (443 if parts.scheme == "https" else 80), test_local)
        if problem:
            return "fail", f"{current}: {problem}{via}"
        request = urllib.request.Request(current, headers={
            "User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.1"})
        deadline = time.monotonic() + timeout
        try:
            response = OPENER.open(request, timeout=timeout)
        except urllib.error.HTTPError as error:
            error.close()
            if error.code in (301, 302, 303, 307, 308):
                location = error.headers.get("Location")
                if not location:
                    return "fail", f"{current} answered {error.code} with no address to go to"
                current = urljoin(current, location.strip())
                continue
            if error.code in (403, 429):
                return "unchecked", (f"{current} answered {error.code}, as bot protection often "
                                     f"answers a runner; open it by hand")
            return "fail", f"{current} answered {error.code}"
        except urllib.error.URLError as error:
            reason = error.reason
            if isinstance(reason, ssl.SSLCertVerificationError):
                return "fail", f"{current}: its certificate does not verify ({reason.verify_message})"
            if isinstance(reason, (TimeoutError, socket.timeout)):
                return "fail", f"{current} did not answer within {timeout:g} s"
            return "fail", f"{current}: {reason}"
        except (TimeoutError, socket.timeout):
            return "fail", f"{current} did not answer within {timeout:g} s"
        except (OSError, http.client.HTTPException) as error:
            return "fail", f"{current}: {error}"
        try:
            with response:
                status = response.status
                kind = response.headers.get_content_type()
                charset = response.headers.get_content_charset() or "utf-8"
                body = read_bounded(response, deadline)
        except (TimeoutError, socket.timeout):
            return "fail", f"{current} did not finish answering within {timeout:g} s"
        except (OSError, http.client.HTTPException) as error:
            return "fail", f"{current}: {error}"
        break
    else:
        return "fail", f"{url} redirects more than {MAX_REDIRECTS} times"
    if status != 200:
        return "fail", f"{current} answered {status}"
    if kind not in ("text/html", "application/xhtml+xml"):
        return "fail", f"{current} is {kind}, not a web page"
    try:
        text = body.decode(charset, "replace")
    except LookupError:
        text = body.decode("utf-8", "replace")
    if bare(urlsplit(current).hostname or "") != bare(first_host):
        window = text[:PHRASE_WINDOW].lower()
        for phrase in PARKING_PHRASES:
            if phrase in window:
                return "fail", f"{url} leads to {current}, which says \"{phrase}\""
    if login:
        profile = Profile(login)
        profile.feed(text)
        profile.close()
        if not profile.found:
            return "fail", (f"{current} links nowhere to https://github.com/{login}: the home page "
                            f"links to its author's GitHub profile (docs/how-to/add-to-the-showcase.md)")
    return "ok", f"{current} answers 200 with a web page" + (f" linking to github.com/{login}" if login else "")


def changed_paths(rev: str) -> list[str]:
    out = subprocess.run(["git", "diff", "--name-only", rev, "HEAD"], cwd=ROOT,
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"git diff {rev} HEAD failed: {out.stderr.strip()}")
    return [line.strip() for line in out.stdout.splitlines() if line.strip()]


def summary(lines: list[str]) -> None:
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with open(target, "a", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the showcase's files, and its sites' responses.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--fetch-all", action="store_true", help="fetch every site and in_use link")
    mode.add_argument("--fetch-changed", metavar="REV", help="fetch the sites changed since REV")
    mode.add_argument("--fetch-url", metavar="URL", help="fetch one address and nothing else")
    parser.add_argument("--login", help="with --fetch-url: the GitHub login the page must link to")
    parser.add_argument("--test-local", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--timeout", type=float, default=TIMEOUT, help=argparse.SUPPRESS)
    sys.stdout.reconfigure(errors="backslashreplace")
    args = parser.parse_args(argv)

    if args.fetch_url:
        state, message = fetch(args.fetch_url, args.login, args.test_local, args.timeout)
        print(f"{LABELS[state]} {message}")
        return 1 if state == "fail" else 0

    problems, sites = check_files()
    count = sum(1 for p in entries() if p.is_dir())
    print(f"Showcase: {count} entr{'y' if count == 1 else 'ies'}; "
          f"{sum(1 for s in sites if s['login'] is None)} design in_use link(s).")
    for problem in problems:
        print(f"  FAIL {problem}")
    if args.fetch_changed:
        changed = changed_paths(args.fetch_changed)
        sites = [s for s in sites if any(p.startswith(s["files"]) for p in changed)]
    flagged, unchecked = [], []
    if args.fetch_all or args.fetch_changed:
        print(f"\nResponses: {len(sites)} address(es), fetched and never rendered.")
        for site in sites:
            state, message = fetch(site["url"], site["login"])
            print(f"  {LABELS[state]} {site['where']}: {message}")
            if state == "fail":
                flagged.append(site)
            elif state == "unchecked":
                unchecked.append(site)
    failed = bool(problems or flagged)
    if failed or unchecked:
        # Only the repository's own words and addresses: nothing a site sent.
        summary(["## Showcase check", ""]
                + [f"- Fails: `{s['where']}`, {s['url']}" for s in flagged]
                + [f"- Could not be checked, open by hand: `{s['where']}`, {s['url']}" for s in unchecked]
                + ([f"- {len(problems)} problem(s) in the files; the log lists them"] if problems else []))
    print("\nFAIL" if failed else "\nPASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
