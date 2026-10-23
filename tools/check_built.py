"""Check a built site or gallery as files, without a browser.

  python tools/check_built.py [_site] [--previews]

Reads every .html and .css file in the built folder and checks what can be
seen without running anything:

  - every page carries the build's Content-Security-Policy meta tag, before
    anything it loads (ADR-0006, layer 3), a language, a title and a
    viewport;
  - nothing a page or a stylesheet loads comes from another origin: every
    src, stylesheet, preload, image and url() is a relative path that
    stays inside the folder and names a file that exists, letter for letter
    (GitHub Pages matches names by case; Windows and macOS do not);
  - no inline script, no inline style, no event-handler attribute, and no
    iframe, object, embed, form or base element: the page is the engine's
    and loads only its own files (scope floor lines 2 and 6);
  - links that leave the page are http(s) or mailto, never javascript:;
    links within it name an id that exists, and ids are unique;
  - inside the sections, anything hidden in the markup is also aria-hidden,
    so a screen reader at load does not read it while a section skips its
    layout (base.css; tools/check_browser.py checks the page as it runs);
  - a site page's colour-scheme tag agrees with its Dark switch: "light
    dark" with the switch, for a design that offers dark, or "light"
    without it, for one that does not (design.json's dark; ADR-0006,
    Changes, 2026-10-18). The gallery's own page, which is no design's,
    is not held to this;
  - the footer's credit, where a page has one, links this project, then
    the design's author (ADR-0016, D2);
  - in the gallery, every link to another site in a showcase card or a
    design's "In use" line carries rel="ugc nofollow", and every
    showcase picture loads lazily (ADR-0016);
  - every showcase picture has its width and height in the HTML, so its
    box is reserved before it loads (ADR-0009), and that shape is within
    the limits, at most SHOWCASE_TALL times as tall as it is wide and
    SHOWCASE_WIDE times as wide as it is tall: a screenshot beyond them is
    shown within them, with bands (ADR-0016, Changes, 2026-10-20);
  - with --previews, every design in a gallery has its preview image, the
    gallery its own picture at the root, which the README shows (ADR-0017,
    Changes, 2026-10-23), and every showcase card its served copies, each
    card's copy the very size its HTML reserves; without it, a missing one
    is not reported, because the screenshot job makes them after the build.

Exit 0 when everything passes; 1 when anything fails, each printed with
its file; 2 when the folder holds no built page. Standard library only.
"""

from __future__ import annotations

import os
import re
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build import (CSP, PREVIEW_FILE, PROJECT_URL, SHOWCASE_CARD, SHOWCASE_FULL,  # noqa: E402
                   SHOWCASE_TALL, SHOWCASE_WIDE)
from check_design import CSSError, tokens  # noqa: E402

RESOURCE_ATTRS = {"src", "srcset", "poster", "data", "action", "formaction", "background",
                  "imagesrcset", "manifest", "ping", "xlink:href"}
REFUSED_ELEMENTS = {"iframe", "object", "embed", "form", "base", "frame", "frameset",
                    "applet", "portal", "fencedframe"}
LINK_RELS_LOADING = {"stylesheet", "preload", "modulepreload", "prefetch", "icon",
                     "manifest", "preconnect", "dns-prefetch", "prerender", "apple-touch-icon"}


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.problems: list[str] = []
        self.loads: list[str] = []
        self.anchors: list[str] = []
        self.ids: list[str] = []
        self.csp_at: int | None = None
        self.first_load_at: int | None = None
        self.count = 0
        self.lang = None
        self.title = False
        self.viewport = False
        self.section_depth = 0
        self.color_scheme: str | None = None
        self.theme_switches = 0
        self.nav = False
        self.stack: list[str] = []
        self.in_section: list[bool] = []
        self.credit_links: list[list[str]] = []
        self.in_credit = False
        self.contributed: str | None = None  # "site" in a showcase card, "in_use" in its line
        self.sized: list[tuple[str, int, int]] = []  # each showcase picture's src and reserved size

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
            "source", "track", "wbr"}

    def handle_starttag(self, tag, attrs):
        self.count += 1
        a = {k.lower(): (v or "") for k, v in attrs}
        inside = bool(self.in_section and self.in_section[-1]) or "data-section" in a
        if tag not in self.VOID:
            self.stack.append(tag)
            self.in_section.append(inside)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self.title = True
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
        if tag == "meta" and a.get("name") == "color-scheme":
            self.color_scheme = " ".join(a.get("content", "").split())
        if "data-theme-switch" in a:
            self.theme_switches += 1
        if "data-nav-box" in a:
            self.nav = True
        if tag == "meta" and a.get("http-equiv", "").lower() == "content-security-policy":
            if a.get("content") != CSP:
                self.problems.append("the Content-Security-Policy meta tag is not the build's policy")
            elif self.csp_at is None:
                self.csp_at = self.count
        if tag in REFUSED_ELEMENTS:
            self.problems.append(f"<{tag}> is not allowed")
        if tag == "style":
            self.problems.append("an inline <style> element is not allowed")
        if tag == "script":
            if not a.get("src"):
                self.problems.append("an inline <script> is not allowed")
            else:
                self._load(a["src"])
        for name, value in a.items():
            if name.startswith("on"):
                self.problems.append(f"an event-handler attribute is not allowed: {name}")
            if name == "style":
                self.problems.append(f"an inline style attribute is not allowed: <{tag} style>")
            if name in RESOURCE_ATTRS and value:
                for part in value.split(","):
                    self._load(part.strip().split(" ")[0])
            if name == "id":
                self.ids.append(value)
        if tag == "link" and a.get("href"):
            rels = set(a.get("rel", "").lower().split())
            if rels & LINK_RELS_LOADING:
                if a["href"] != "data:,":
                    self._load(a["href"])
            else:
                self.problems.append(f"<link rel=\"{a.get('rel')}\"> is not one the build makes")
        if tag == "a" and "href" in a:
            self.anchors.append(a["href"])
        classes = set(a.get("class", "").split())
        if tag == "p" and "foot-credit" in classes:
            self.in_credit = True
            self.credit_links.append([])
        if tag == "a" and self.in_credit:
            self.credit_links[-1].append(a.get("href", ""))
        # What contributors supply: a showcase card, and a design's "In use"
        # line (ADR-0016). Their links to other sites are marked as such, so
        # an entry earns its author no search ranking from this page, and a
        # card's picture loads only as it scrolls into view.
        if tag == "li" and "g-site" in classes:
            self.contributed = "site"
        if tag == "p" and "g-inuse" in classes:
            self.contributed = "in_use"
        if self.contributed and tag == "a" and urlsplit(a.get("href", "")).scheme in ("http", "https"):
            if not {"ugc", "nofollow"} <= set(a.get("rel", "").lower().split()):
                self.problems.append(f"a link to {a.get('href')} in a contributor's "
                                     f"{'showcase card' if self.contributed == 'site' else 'In use line'} "
                                     f"lacks rel=\"ugc nofollow\"")
        if self.contributed == "site" and tag == "img" and a.get("loading") != "lazy":
            self.problems.append(f"the showcase picture {a.get('src')} does not load lazily "
                                 f"(loading=\"lazy\")")
        if self.contributed == "site" and tag == "img":
            self._sized(a)
        if inside and "hidden" in a and a.get("aria-hidden") != "true":
            name = a.get("id") or a.get("class") or tag
            self.problems.append(f"<{tag}> '{name}' is hidden inside a section but not "
                                 f"aria-hidden=\"true\"")

    def handle_endtag(self, tag):
        if tag == "p":
            self.in_credit = False
            if self.contributed == "in_use":
                self.contributed = None
        if tag == "li" and self.contributed == "site":
            self.contributed = None
        if tag in self.VOID:
            return
        while self.stack:
            open_tag = self.stack.pop()
            self.in_section.pop()
            if open_tag == tag:
                break

    def _sized(self, a: dict) -> None:
        src = a.get("src", "")
        if not (a.get("width", "").isdigit() and a.get("height", "").isdigit()
                and int(a["width"]) and int(a["height"])):
            self.problems.append(f"the showcase picture {src} has no width and height, so the page "
                                 f"would shift as it loads (ADR-0009)")
            return
        width, height = int(a["width"]), int(a["height"])
        if height > width * SHOWCASE_TALL or width > height * SHOWCASE_WIDE:
            self.problems.append(f"the showcase picture {src} is {width}x{height}, beyond the shape "
                                 f"limits of {SHOWCASE_TALL} either way: a screenshot beyond them is shown "
                                 f"within them, with bands (build.py, showcase_shapes)")
        self.sized.append((src, width, height))

    def _load(self, url: str) -> None:
        if self.first_load_at is None:
            self.first_load_at = self.count
        self.loads.append(url)


def resolve(base: Path, root: Path, url: str) -> tuple[Path | None, str | None]:
    """The file a relative URL loads, or why it cannot be loaded from here."""
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or url.startswith("//"):
        return None, f"'{url}' loads from another origin or scheme; only relative paths are allowed"
    if url.startswith("/"):
        return None, (f"'{url}' is root-relative, which breaks when the site is served from "
                      f"/<repository>/; write it relative to the page (ADR-0007)")
    if not parts.path:
        return None, f"'{url}' names no file"
    target = PurePosixPath(base.relative_to(root).as_posix()) / unquote(parts.path)
    resolved: list[str] = []
    for piece in target.parts:
        if piece == "..":
            if not resolved:
                return None, f"'{url}' climbs out of the built folder"
            resolved.pop()
        elif piece != ".":
            resolved.append(piece)
    folder = root
    for piece in resolved:
        try:
            names = os.listdir(folder)
        except OSError:
            return None, f"'{url}' does not exist"
        if piece not in names:
            near = [n for n in names if n.lower() == piece.lower()]
            return None, (f"'{url}' does not exist" +
                          (f"; the file is named '{near[0]}', and GitHub Pages matches names "
                           f"by case" if near else ""))
        folder = folder / piece
    if not folder.is_file():
        return None, f"'{url}' is not a file"
    return folder, None


def check_html(path: Path, root: Path, previews: bool = False) -> list[str]:
    page = Page()
    page.feed(path.read_text(encoding="utf-8"))
    page.close()
    problems = list(page.problems)
    if page.csp_at is None:
        problems.append("no Content-Security-Policy meta tag")
    elif page.first_load_at is not None and page.first_load_at < page.csp_at:
        problems.append("something loads before the Content-Security-Policy meta tag")
    if not page.lang:
        problems.append("the <html> element names no language")
    if not page.title:
        problems.append("no <title>")
    if not page.viewport:
        problems.append("no viewport meta tag")
    if page.nav:
        # A site page, in one design: the tag and the switch say the same.
        if page.color_scheme == "light" and page.theme_switches:
            problems.append("the colour-scheme tag says light only, yet the page has a Dark switch")
        elif page.color_scheme == "light dark" and not page.theme_switches:
            problems.append("the colour-scheme tag offers dark, yet the page has no Dark switch")
        elif page.color_scheme not in ("light", "light dark"):
            problems.append(f"the colour-scheme tag must be 'light' or 'light dark', not "
                            f"{page.color_scheme!r}")
    for links in page.credit_links:
        # The credit names this project and the design's author, each
        # linked (ADR-0016, D2); config.json may leave it out altogether.
        # The author's link is the second; Plain's author is the project.
        if len(links) < 2 or links[0] != PROJECT_URL or urlsplit(links[1]).scheme != "https":
            problems.append("the footer credit does not link both portfolio-gallery and the "
                            "design's author (ADR-0016, D2)")
    for url in page.loads:
        # A gallery's previews, and its showcase's served copies, are made
        # after the build, by the screenshot job (tools/screenshots.py);
        # --previews requires them, and the deploy workflow passes it once
        # they are in.
        if not previews and later_picture(url):
            continue
        _, problem = resolve(path.parent, root, url)
        if problem:
            problems.append(problem)
    if previews and page.sized:
        # The card's copy is the size its box was reserved at; the reader
        # is the showcase check's, which exists while the showcase does.
        from check_showcase import ImageError, webp_facts
        for src, width, height in page.sized:
            file, problem = resolve(path.parent, root, src)
            if problem:
                continue
            try:
                facts = webp_facts(file.read_bytes())
            except (ImageError, struct.error) as error:
                problems.append(f"the showcase picture {src} cannot be read: {error or 'its header'}")
                continue
            if (facts["width"], facts["height"]) != (width, height):
                problems.append(f"the showcase picture {src} is reserved at {width}x{height} but is "
                                f"{facts['width']}x{facts['height']}, so the page would shift as it loads")
    ids = set(page.ids)
    for duplicate in sorted({i for i in page.ids if page.ids.count(i) > 1}):
        problems.append(f"id '{duplicate}' is used more than once")
    for href in page.anchors:
        parts = urlsplit(href)
        if href.startswith("#"):
            if href[1:] not in ids:
                problems.append(f"the link '{href}' names no id on the page")
        elif parts.scheme in ("http", "https") and parts.netloc:
            continue
        elif parts.scheme == "mailto" and parts.path:
            continue
        elif parts.scheme:
            problems.append(f"the link '{href}' uses the {parts.scheme}: scheme; only http(s) "
                            f"and mailto are allowed")
        elif not previews and later_picture(href.split("#", 1)[0]):
            continue
        else:
            _, problem = resolve(path.parent, root, href.split("#", 1)[0])
            if problem:
                problems.append(f"the link {problem}")
    return problems


def later_picture(url: str) -> bool:
    """A picture the screenshot job adds after the build."""
    return bool(re.fullmatch(rf"designs/[a-z0-9-]+/{re.escape(PREVIEW_FILE)}", url)
                or re.fullmatch(rf"showcase/[a-z0-9-]+/(?:{re.escape(SHOWCASE_CARD)}|"
                                rf"{re.escape(SHOWCASE_FULL)})", url))


def check_css(path: Path, root: Path) -> list[str]:
    problems = []
    try:
        for kind, value, line in tokens(path.read_text(encoding="utf-8")):
            if kind == "at" and value == "import":
                problems.append(f"line {line}: @import")
            elif kind == "url":
                _, problem = resolve(path.parent, root, value)
                if problem:
                    problems.append(f"line {line}: {problem}")
    except CSSError as error:
        problems.append(f"cannot be read safely: {error}")
    return problems


def main(argv: list[str]) -> int:
    # Page text can hold characters the console cannot write, as on Windows;
    # write them escaped rather than stop the report.
    sys.stdout.reconfigure(errors="backslashreplace")
    previews = "--previews" in argv
    args = [a for a in argv if a != "--previews"]
    root = Path(args[0] if args else "_site").resolve()
    pages = sorted(root.rglob("*.html"))
    if not pages:
        print(f"no built page in {root}; run python build.py first", file=sys.stderr)
        return 2
    failures = 0
    for path in pages + sorted(root.rglob("*.css")):
        found = check_html(path, root, previews) if path.suffix == ".html" else check_css(path, root)
        shown = path.relative_to(root).as_posix()
        print(f"{'FAIL' if found else 'ok  '} {shown}")
        for problem in found:
            print(f"  {shown}: {problem}")
        failures += len(found)
    if previews:
        demos = sorted((root / "designs").glob("*/index.html"))
        for demo in demos:
            if not (demo.parent / PREVIEW_FILE).is_file():
                print(f"FAIL designs/{demo.parent.name}: no {PREVIEW_FILE}; run tools/screenshots.py")
                failures += 1
        if demos and not (root / PREVIEW_FILE).is_file():
            print(f"FAIL the gallery page: no {PREVIEW_FILE} of its own; run tools/screenshots.py")
            failures += 1
    print(f"\n{len(pages)} page(s), {failures} problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
