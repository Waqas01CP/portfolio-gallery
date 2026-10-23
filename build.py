"""Build a portfolio site, or the gallery of every design, from structured content.

Reads content/config.json (the settings), content/site.json (the text that
belongs to the page rather than to one item) and content/items.json (every
dated item). Checks them against the schema in docs/reference/content.md,
computes the timeline and the project grid, renders the templates in
src/templates/ and writes the result to _site/ (ADR-0004).

Run with the project venv active:

  python build.py                       the site, in the design config.json names
  python build.py --design plain        the site, in another design
  python build.py --gallery             the gallery: every design in designs/,
                                        each built on the same content, and a
                                        page showing them all, then the
                                        showcase of contributors' own sites
                                        in showcase/ (ADR-0016)
  python build.py --as-of YYYY-MM       as of a given month (default: this UTC month)
  python build.py --out DIR             write somewhere other than _site/

The as-of month is what `present` resolves to and the top of the timeline.
It is written into every page as <meta name="as-of">, so two builds with
the same month and the same source are byte-identical.

Every internal URL is relative to the page, so the same output works at
https://<user>.github.io/, at https://<user>.github.io/<repository>/ and
under a custom domain, with nothing to configure (ADR-0007).

Every check runs before anything is written, so a failed build exits 1 and
leaves the previous output untouched.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import os
import re
import shutil
import struct
import sys
import tempfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from importlib import metadata
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
CONFIG = CONTENT_DIR / "config.json"
SITE = CONTENT_DIR / "site.json"
ITEMS = CONTENT_DIR / "items.json"
TEMPLATES = ROOT / "src" / "templates"
STATIC_SRC = ROOT / "src" / "static"
DESIGNS = ROOT / "designs"
SHOWCASE = ROOT / "showcase"
REQUIREMENTS = ROOT / "requirements.txt"
DEFAULT_OUT = ROOT / "_site"

# Where the engine lives. The footer's credit links here, and a site may
# turn the credit off in config.json (ADR-0002).
PROJECT_NAME = "portfolio-gallery"
PROJECT_URL = "https://github.com/Waqas01CP/portfolio-gallery"

# Every page carries this policy in a meta tag, so a browser refuses
# scripts, styles, fonts and images from any other origin even if a check
# misses one (ADR-0006, layer 3). A meta tag cannot set frame-ancestors,
# report-uri or sandbox; those need a response header, which GitHub Pages
# does not let a site set. data: images cover the empty favicon below.
CSP = ("default-src 'none'; script-src 'self'; style-src 'self'; "
       "img-src 'self' data:; font-src 'self'; worker-src 'self'; "
       "base-uri 'none'; form-action 'none'")

# The design every gallery lists first, and the one config.json starts with.
DEFAULT_DESIGN = "default"
# A gallery demo is served from designs/<name>/, two folders below the
# gallery's root, so its URLs to the shared files climb two folders.
DEMO_ROOT = "../" * len(("designs", "<name>"))

# Timeline scale: four layout units per month (the stylesheet sets a unit's
# size). The axis runs from the as-of month at the top down to its start,
# which config.json may set and otherwise is January of the earliest
# year any item outside the degree band starts in.
UNITS_PER_MONTH = 4

LANE_LABELS = {
    "builds": "Projects",
    "work": "Work",
    "certifications": "Certifications",
    "band": "Degree",
}
# The timeline's columns, left to right: projects left of the spine, work
# and certifications right of it. The degree band is drawn behind them all.
TIMELINE_LANES = ("builds", "work", "certifications")

# The sections in page order. A section with nothing to show is left out,
# and so is its menu entry.
SECTIONS = (
    ("intro", "Intro"),
    ("projects", "Projects"),
    ("timeline", "Timeline"),
    ("work", "Work"),
    ("education", "Education"),
    ("certifications", "Certifications"),
    ("skills", "Skills"),
    ("contact", "Contact"),
)

# Element ids the page uses itself, and the prefixes it builds ids from. An
# item id equal to one of these would silently break an anchor.
RESERVED_IDS = {"main", "top"} | {section_id for section_id, _ in SECTIONS}
RESERVED_PREFIXES = ("depth-", "toggle-", "tl-", "tlx-", "h-")

COMMON = ("id", "lane", "title", "start", "end", "source")
PROOF_ROUTES = ("proof", "no_proof")
LANE_FIELDS = {
    # lane: (required, optional)
    "builds": (("tier", "stack", "layer1", "bullets"), ("status", "layer2", "detail", "date_style")),
    "work": (("org", "location", "bullets"), ("org_short", "date_style", "detail")),
    "band": (("org",), ("org_short", "grade", "coursework", "date_style")),
    "certifications": ((), ("org", "date_style")),
}
CONFIG_FIELDS = {"design", "cv_pdf", "cv_source", "content_trace", "credit", "timeline_start"}
DATE_STYLES = ("compact", "full", "long")
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DESIGN_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
YM_RE = re.compile(r"^(\d{4})-(0[1-9]|1[0-2])$")
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
MONTHS_LONG = ("January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December")

# The project grid: tier 1 takes a full row; the rest flow three to a row
# on a wide screen and two on a medium one, and a short last row shares its
# width. Columns of a six-column grid, so 2, 3 or 6 per card.
GRID_COLUMNS = 6

# The gallery's preview images, made by tools/screenshots.py after the
# build: the first screen at 1366 by 900 CSS pixels, saved at half size.
PREVIEW_FILE = "preview.webp"
PREVIEW_SIZE = (683, 450)
# A showcase entry's screenshot, supplied by its author as their tool saved
# it (ADR-0016, D1; Changes, 2026-10-20). It is never published itself:
# tools/screenshots.py makes two served copies from it, WebP with no
# metadata, never enlarged, each shaped by showcase_shapes() below: the
# card's and the full view's, which a click on the card opens.
# The screenshot keeps the name its tool gave it, such as "Screenshot
# 2026-10-20 at 11.30.12.png": any name ending .png, .jpg, .jpeg or .webp,
# in any case, with no folder, no control character, not hidden, at most
# about 120 characters. tools/check_showcase.py and tools/scope_check.py
# hold the same rule.
SHOWCASE_IMAGE_RE = re.compile(r"[^/\\.\x00-\x1f\x7f][^/\\\x00-\x1f\x7f]{0,115}\.(?:png|jpe?g|webp)", re.IGNORECASE)
SHOWCASE_CARD, SHOWCASE_FULL = "card.webp", "full.webp"
SHOWCASE_QUALITY = 0.82
# A card's picture takes its screenshot's own shape, at the card's full
# width, whole, between two limits (the owner's decision of 2026-10-20,
# ADR-0016, Changes): at most SHOWCASE_TALL times as tall as it is wide,
# and at most SHOWCASE_WIDE times as wide as it is tall. Both are 2.4, a
# 21:9 screen's shape, the most elongated first screen measured on
# 2026-10-21 either way: an ultrawide monitor's 3440x1440 is 2.39 wide,
# and the tallest common phones, 20:9 at 2.22 and 21:9 at 2.33, are below
# it. Beyond a limit, as a whole page or a 32:9 monitor's snip is, the
# picture box stops at the limit and shows the picture whole inside it,
# shrunk, with bands: transparent pixels in card.webp, so the card's own
# colour shows through them in either theme. Nothing is refused for its
# shape. The card's copy is at most SHOWCASE_CARD_WIDTH pixels wide, three
# times a desktop column's 345 CSS pixels; the full view's fits 2560 by
# 2560 with no bands.
SHOWCASE_TALL = 2.4
SHOWCASE_WIDE = 2.4
SHOWCASE_CARD_WIDTH = 1024
SHOWCASE_FULL_FIT = 2560


def showcase_shapes(width: int, height: int) -> dict[str, dict]:
    """Each served copy's size and the rectangle its picture is drawn in
    (x, y, width, height), from the screenshot's size as a browser shows
    it. Never enlarged; the card's bands, if any, split evenly."""
    full = min(1.0, SHOWCASE_FULL_FIT / width, SHOWCASE_FULL_FIT / height)
    full_size = (max(1, round(width * full)), max(1, round(height * full)))
    # The height whole, so a box at the tall limit is no wider than the card.
    scale = min(1.0, SHOWCASE_CARD_WIDTH / width, math.floor(SHOWCASE_CARD_WIDTH * SHOWCASE_TALL) / height)
    picture = (max(1, round(width * scale)), max(1, round(height * scale)))
    box = picture
    if picture[1] > picture[0] * SHOWCASE_TALL:
        box = (math.ceil(picture[1] / SHOWCASE_TALL), picture[1])
    elif picture[0] > picture[1] * SHOWCASE_WIDE:
        box = (picture[0], math.ceil(picture[0] / SHOWCASE_WIDE))
    return {SHOWCASE_CARD: {"size": box, "at": ((box[0] - picture[0]) // 2, (box[1] - picture[1]) // 2,
                                                *picture)},
            SHOWCASE_FULL: {"size": full_size, "at": (0, 0, *full_size)}}


class BuildError(Exception):
    """A failure the build reports by name and exits non-zero on."""


# Dates. Pure functions with no template knowledge, so they can be tested
# directly by importing this module.

def month_index(ym: str) -> int:
    """Count of months since year 0 for a YYYY-MM string."""
    match = YM_RE.match(ym)
    if not match:
        raise ValueError(f"'{ym}' is not a YYYY-MM date")
    return int(match[1]) * 12 + int(match[2]) - 1


def month_name(index: int, long: bool = False) -> str:
    return (MONTHS_LONG if long else MONTHS)[index % 12]


def grid_position(start: str, end: str, lane: str, as_of: str,
                  axis_start: str) -> tuple[int, int, bool]:
    """Return (start row, row span, starts before the axis) for one entry.

    Newest at the top: row 1 is the as-of month, each month is
    UNITS_PER_MONTH rows going down, and the axis ends at axis_start. An
    entry's row is set by its end month and its span by its length, so
    moving an end date by a month moves only that entry's top edge, by four
    rows. `present` resolves to as_of. Only the degree band may start before
    the axis, or end after the as-of month; it is clipped to the axis and
    flagged so it can be drawn running past the bottom edge.
    """
    first = month_index(start)
    last = month_index(as_of if end == "present" else end)
    top, axis = month_index(as_of), month_index(axis_start)
    if last < first:
        raise ValueError(f"ends {end} before it starts {start}")
    if first > top:
        raise ValueError(f"starts {start}, after the as-of month {as_of}")
    if last > top:
        if lane != "band":
            raise ValueError(f"ends {end}, after the as-of month {as_of}")
        last = top
    before_axis = first < axis
    if before_axis:
        if lane != "band":
            raise ValueError(f"starts {start}, before the timeline opens at "
                             f"{axis_start}; only the degree band may")
        if last < axis:
            raise ValueError(f"ends {end}, before the timeline opens at {axis_start}")
        first = axis
    row = (top - last) * UNITS_PER_MONTH + 1
    span = (last - first + 1) * UNITS_PER_MONTH
    return row, span, before_axis


def date_phrase(start: str, end: str, style: str = "compact") -> dict:
    """The dates as parts, so the template can wrap each date in <time>.

    compact: "Feb 2025", "Nov to Dec 2025", "Aug 2024 to Jan 2025",
             "Feb 2026 to Present". The default, and the timeline's form.
    full:    "Jan 2024 to Feb 2024": both years always.
    long:    "June 2026 to July 2026": month names in full.
    """
    long = style == "long"

    def label(ym: str, with_year: bool = True) -> str:
        year, month = ym.split("-")
        name = month_name(int(month) - 1, long)
        return f"{name} {year}" if with_year else name

    if end == "present":
        return {"start": start, "start_text": label(start), "end": None, "end_text": "Present"}
    if end == start:
        return {"start": start, "start_text": label(start), "end": None, "end_text": None}
    same_year = start[:4] == end[:4] and style == "compact"
    return {"start": start, "start_text": label(start, not same_year),
            "end": end, "end_text": label(end)}


def date_plain(phrase: dict) -> str:
    text = phrase["start_text"]
    return f"{text} to {phrase['end_text']}" if phrase["end_text"] else text


# Cuts. Text shortened from a longer source is stored as written, and the
# build refuses any that is not a cut of it: the same words in the same
# order with some left out. A number changed in one place and not the other
# fails here, so each fact keeps one authority.

WORD_RE = re.compile(r"\d+(?:[.,]\d+)*%?|[^\W\d_]+")
TAG_RE = re.compile(r"<[^>]+>")


def plain(fragment: str) -> str:
    return html.unescape(TAG_RE.sub("", fragment))


def words(text: str) -> list[str]:
    return WORD_RE.findall(plain(text).lower())


def is_cut(part: str, source: str) -> bool:
    remaining = iter(words(source))
    return all(word in remaining for word in words(part))


# Fragments.

class _FragmentCheck(HTMLParser):
    """Accepts <strong> and <a href> only, properly nested. Bullets are
    rendered unescaped, so this is what stands between the content file and
    arbitrary markup in the page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.problems: list[str] = []
        self.hrefs: list[str] = []
        self._open: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "strong" and not attrs:
            self._open.append(tag)
        elif tag == "a" and len(attrs) == 1 and attrs[0][0] == "href" and attrs[0][1]:
            self._open.append(tag)
            self.hrefs.append(attrs[0][1])
        else:
            names = "".join(f" {name}" for name, _ in attrs)
            self.problems.append(f"<{tag}{names}> is not allowed; only <strong> and <a href>")

    def handle_startendtag(self, tag, attrs):
        self.problems.append(f"<{tag}/> is not allowed; only <strong> and <a href>")

    def handle_endtag(self, tag):
        if self._open and self._open[-1] == tag:
            self._open.pop()
        else:
            self.problems.append(f"</{tag}> closes nothing that is open")

    def handle_comment(self, data):
        self.problems.append("an HTML comment is not allowed")

    def handle_decl(self, decl):
        self.problems.append("a declaration is not allowed")

    def handle_pi(self, data):
        self.problems.append("a processing instruction is not allowed")

    def unknown_decl(self, data):
        self.problems.append("a declaration is not allowed")

    def close(self):
        super().close()
        self.problems.extend(f"<{tag}> is never closed" for tag in self._open)


def fragment_problems(fragment: str) -> list[str]:
    checker = _FragmentCheck()
    checker.feed(fragment)
    checker.close()
    return checker.problems + [p for p in map(url_problem, checker.hrefs) if p]


def url_problem(url: str, mail: bool = True) -> str | None:
    """Why a link target is not allowed, or None if it is. Links leave the
    site when a visitor follows them, so they may point anywhere on the web;
    they may not run anything (javascript:) or be relative, which would
    break when the page moves."""
    parts = urlsplit(url)
    if mail and parts.scheme == "mailto" and parts.path:
        return None
    if parts.scheme not in ("http", "https") or not parts.hostname:
        allowed = "an absolute http(s) URL" + (" or a mailto: address" if mail else "")
        return f"'{url}' is not {allowed}"
    return None


def _filled(value) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    return value not in (None, [], {})


def _text(value) -> bool:
    return isinstance(value, str) and _filled(value)


def _text_list(value) -> bool:
    return isinstance(value, list) and bool(value) and all(_text(v) for v in value)


# Items.

def check_item(raw, position: int, as_of: str, axis_start: str) -> dict:
    """Check one raw item and return it normalised for the templates.

    Raises BuildError naming the item, by id where it has one."""
    name = raw.get("id") if isinstance(raw, dict) and _filled(raw.get("id")) else f"#{position}"

    def fail(message: str):
        raise BuildError(f"item '{name}': {message}")

    if not isinstance(raw, dict):
        fail("is not a JSON object")

    # Checked first, so they report even on an item broken in other ways.
    if not _filled(raw.get("source")):
        fail("has no source. Every item names the part of your CV it comes from, "
             "as '<section> / <entry>' (docs/reference/content.md)")
    routes = [route for route in PROOF_ROUTES if _filled(raw.get(route))]
    if len(routes) > 1:
        fail("has both proof and no_proof. Give exactly one")
    if not routes:
        fail("has no proof link and no no_proof reason. Give exactly one: a link a "
             "reader can check, or the reason there is none")

    lane = raw.get("lane")
    if lane not in LANE_FIELDS:
        fail(f"lane must be one of: {', '.join(LANE_FIELDS)}")
    required, optional = LANE_FIELDS[lane]
    allowed = set(COMMON) | set(PROOF_ROUTES) | set(required) | set(optional)
    unknown = sorted(set(raw) - allowed)
    if unknown:
        fail(f"has fields the schema does not define for the {lane} lane: {', '.join(unknown)}")
    missing = [field for field in COMMON + required if field not in raw]
    if missing:
        fail(f"is missing required fields: {', '.join(missing)}")

    for field in ("id", "title", "source", "org", "org_short", "location", "layer1",
                  "layer2", "status", "detail", "no_proof", "grade"):
        if field in raw and not _text(raw[field]):
            fail(f"{field} must be non-empty text")
    for field in ("stack", "bullets", "coursework"):
        if field in raw and not _text_list(raw[field]):
            fail(f"{field} must be a non-empty list of non-empty text")
    if not ID_RE.match(raw["id"]):
        fail("id must be a lowercase slug: letters, digits and single hyphens")
    if raw["id"] in RESERVED_IDS or raw["id"].startswith(RESERVED_PREFIXES):
        fail(f"id '{raw['id']}' is already used, or reserved, by the page itself")
    if "tier" in raw and (type(raw["tier"]) is not int or raw["tier"] not in (1, 2, 3)):
        fail("tier must be 1, 2 or 3")
    style = raw.get("date_style", "compact")
    if style not in DATE_STYLES:
        fail(f"date_style must be one of: {', '.join(DATE_STYLES)}")
    if not (isinstance(raw["end"], str) and (raw["end"] == "present" or YM_RE.match(raw["end"]))):
        fail("end must be YYYY-MM or present")
    if not (isinstance(raw["start"], str) and YM_RE.match(raw["start"])):
        fail("start must be YYYY-MM")
    try:
        row, span, before_axis = grid_position(raw["start"], raw["end"], lane, as_of, axis_start)
    except ValueError as error:
        fail(str(error))

    proof = raw.get("proof")
    if "proof" in routes:
        if not isinstance(proof, list):
            fail("proof must be a list of {label, url}")
        for link in proof:
            if not (isinstance(link, dict) and set(link) == {"label", "url"}
                    and all(_text(link[k]) for k in link)):
                fail("each proof entry must be exactly {label, url}, both non-empty text")
            if problem := url_problem(link["url"], mail=False):
                fail(f"proof link {problem}")
    if lane == "certifications" and "proof" not in routes:
        fail("a certificate's card is its credential link, so it needs proof")

    bullets = raw.get("bullets", [])
    for number, bullet in enumerate(bullets, start=1):
        if problems := fragment_problems(bullet):
            fail(f"bullet {number}: {'; '.join(problems)}")

    # Shortened text must be a cut of the item's own text.
    if "layer1" in raw and not any(is_cut(raw["layer1"], b) for b in bullets):
        fail("layer1 is not a cut of any of its bullets: the same words in the same "
             "order with some left out")
    if lane == "builds" and len(bullets) == 1:
        # One bullet renders no "In depth" panel, so the visible layers must
        # carry all of it.
        shown = words(raw.get("layer2", "")) + words(raw["layer1"])
        if shown != words(bullets[0]):
            fail("has one bullet and so no 'In depth' panel: layer2 then layer1 must "
                 "carry the whole bullet, word for word")
    if "detail" in raw:
        sources = [f"{raw.get('status', '')} {raw.get('layer2', '')}", raw.get("layer1", "")] + bullets
        if not any(is_cut(raw["detail"], s) for s in sources if s.strip()):
            fail("detail is not a cut of its status and layer2, its layer1 or a bullet")
    if "org_short" in raw and not is_cut(raw["org_short"], raw["org"]):
        fail("org_short is not a cut of org")

    title_name, _, title_sub = raw["title"].partition(": ")
    phrase = date_phrase(raw["start"], raw["end"], style)
    compact = date_phrase(raw["start"], raw["end"])
    first = month_index(raw["start"])
    last = month_index(as_of if raw["end"] == "present" else raw["end"])
    return {
        **{k: raw.get(k) for k in ("id", "lane", "title", "source", "tier", "status", "org",
                                   "location", "layer1", "layer2", "detail", "grade")},
        "name": title_name,
        "sub": title_sub or None,
        "org_short": raw.get("org_short") or raw.get("org"),
        "stack": raw.get("stack", []),
        "bullets": bullets,
        "coursework": raw.get("coursework", []),
        "proof": proof if "proof" in routes else [],
        "lane_label": LANE_LABELS[lane],
        "start": raw["start"],
        "end": raw["end"],
        "when": phrase,
        "when_text": date_plain(phrase),
        "when_compact": compact,
        "when_compact_text": date_plain(compact),
        "months": last - first + 1,
        "first": first,
        "last": last,
        "row": row,
        "span": span,
        "before_axis": before_axis,
        "has_depth": len(bullets) > 1,
    }


def load_json(path: Path, kind: type):
    shown = path.relative_to(ROOT).as_posix()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise BuildError(f"file not found: {shown}") from None
    except json.JSONDecodeError as error:
        raise BuildError(f"{shown} is not valid JSON: {error}") from None
    if not isinstance(data, kind) or not data:
        raise BuildError(f"{shown} must be a non-empty JSON {kind.__name__}")
    return data


def axis_start_for(raw_items: list, config: dict) -> str:
    """The month the timeline's axis ends at, at its bottom."""
    if config.get("timeline_start"):
        return config["timeline_start"]
    starts = [i["start"] for i in raw_items if isinstance(i, dict) and i.get("lane") != "band"
              and isinstance(i.get("start"), str) and YM_RE.match(i["start"])]
    return f"{min(starts)[:4]}-01" if starts else "2000-01"


def load_items(path: Path, as_of: str, config: dict) -> tuple[list[dict], str]:
    """Read and check every item. Reports every failing item, not only the first."""
    raw_items = load_json(path, list)
    axis_start = axis_start_for(raw_items, config)
    items, problems, seen = [], [], set()
    for position, raw in enumerate(raw_items, start=1):
        try:
            item = check_item(raw, position, as_of, axis_start)
        except BuildError as error:
            problems.append(str(error))
            continue
        if item["id"] in seen:
            problems.append(f"item '{item['id']}': id is used by an earlier item")
        seen.add(item["id"])
        items.append(item)

    bands = [item for item in items if item["lane"] == "band"]
    if len(bands) > 1:
        problems.append("more than one item is in the band lane; the timeline draws one "
                        "degree band (a known limit, docs/reference/content.md)")

    # Tier is an assertion about the content file's order, never a second
    # order: down the file, tier must not decrease. Sorting by tier instead
    # would let the file and the page disagree silently.
    highest = None
    for item in (item for item in items if item["lane"] == "builds"):
        if highest and item["tier"] < highest["tier"]:
            problems.append(f"item '{highest['id']}' (tier {highest['tier']}) is above "
                            f"item '{item['id']}' (tier {item['tier']}) in Projects; "
                            f"tier must not decrease down the content file")
        if highest is None or item["tier"] > highest["tier"]:
            highest = item
    if problems:
        raise BuildError("\n".join(problems))
    return items, axis_start


def load_config(path: Path) -> dict:
    config = load_json(path, dict)
    problems = []
    unknown = sorted(set(config) - CONFIG_FIELDS)
    if unknown:
        problems.append(f"config.json: unknown settings: {', '.join(unknown)}. "
                        f"Known: {', '.join(sorted(CONFIG_FIELDS))}")
    if not (_text(config.get("design")) and DESIGN_NAME_RE.match(config["design"])):
        problems.append("config.json: design must name a folder in designs/, such as \"default\"")
    for key in ("cv_pdf", "cv_source", "timeline_start"):
        if key in config and not isinstance(config[key], str):
            problems.append(f"config.json: {key} must be text (empty for none)")
    for key in ("content_trace", "credit"):
        if key in config and not isinstance(config[key], bool):
            problems.append(f"config.json: {key} must be true or false")
    if config.get("timeline_start") and not YM_RE.match(config["timeline_start"]):
        problems.append("config.json: timeline_start must be YYYY-MM, or empty")
    if config.get("content_trace", True) and not config.get("cv_source"):
        problems.append("config.json: content_trace is on, so cv_source must name your CV "
                        "file, such as \"content/cv.md\"; or set content_trace to false")
    for key in ("cv_pdf", "cv_source"):
        if config.get(key):
            if problem := repo_file_problem(config[key]):
                problems.append(f"config.json: {key}: {problem}")
    if problems:
        raise BuildError("\n".join(problems))
    return {"cv_pdf": "", "cv_source": "", "content_trace": True, "credit": True,
            "timeline_start": "", **config}


def repo_file_problem(relative: str) -> str | None:
    """Why a path from config.json cannot be used, or None. The name must
    match the file's own name letter for letter: Windows and macOS find a
    file whatever its case, GitHub Pages does not, so a link that works
    locally would fail live."""
    parts = relative.split("/")
    if relative.startswith("/") or "\\" in relative or ".." in parts or not relative:
        return f"'{relative}' must be a path inside the repository, written with /"
    folder = ROOT
    for part in parts:
        try:
            names = os.listdir(folder)
        except OSError:
            return f"'{relative}' does not exist"
        if part not in names:
            near = [n for n in names if n.lower() == part.lower()]
            hint = f"; the file is named '{near[0]}'" if near else ""
            return f"'{relative}' does not exist{hint}"
        folder = folder / part
    if not folder.is_file():
        return f"'{relative}' is not a file"
    return None


# Site-level content.

def resolve(ref: str, site: dict, by_id: dict) -> str:
    """The text a highlight is cut from: 'site/summary' or '<item>/bullets/<n>'."""
    if ref == "site/summary":
        return site["summary"]
    match = re.match(r"^([a-z0-9-]+)/bullets/(\d+)$", ref or "")
    if not match or match[1] not in by_id:
        raise BuildError(f"site.json: '{ref}' names no source; use site/summary or <item>/bullets/<n>")
    bullets = by_id[match[1]]["bullets"]
    number = int(match[2])
    if not 1 <= number <= len(bullets):
        raise BuildError(f"site.json: '{ref}': {match[1]} has {len(bullets)} bullet(s)")
    return bullets[number - 1]


def split_figure(figure: str) -> dict:
    """'24-node' becomes a number set large and a suffix set small; a figure
    with no digits, such as 'three', is set as a word."""
    match = re.match(r"^(\d+(?:[.,]\d+)*%?\+?)(.*)$", figure)
    if match:
        return {"number": match[1], "suffix": match[2], "word": None}
    return {"number": None, "suffix": "", "word": figure}


def load_site(path: Path, items: list[dict]) -> dict:
    site = load_json(path, dict)
    by_id = {item["id"]: item for item in items}
    problems = []

    def need(key, check, what):
        if not check(site.get(key)):
            problems.append(f"site.json: {key} must be {what}")

    for key in ("name", "location", "summary"):
        need(key, _text, "non-empty text")
    need("headline", _text_list, "a non-empty list of text")
    for key in ("availability", "intro"):
        if key in site and not _text(site[key]):
            problems.append(f"site.json: {key} must be non-empty text, or left out")
    skills = site.get("skills", [])
    if not (isinstance(skills, list) and all(
            isinstance(g, dict) and set(g) == {"label", "items"} and _text(g["label"])
            and _text_list(g["items"]) for g in skills)):
        problems.append("site.json: skills must be a list of {label, items}")
    contact = site.get("contact")
    if not (isinstance(contact, list) and contact):
        problems.append("site.json: contact must list at least one route, such as your email")
    else:
        for number, route in enumerate(contact, start=1):
            if not (isinstance(route, dict) and {"label", "url", "text"} <= set(route)
                    and set(route) <= {"label", "url", "text", "line", "cta"}
                    and all(_text(route[k]) for k in route)):
                problems.append(f"site.json: contact {number} must be {{label, url, text}}, "
                                f"with optional line and cta, all non-empty text")
            elif problem := url_problem(route["url"]):
                problems.append(f"site.json: contact {number}: {problem}")
    known = {"name", "headline", "location", "availability", "summary", "intro",
             "highlights", "feature", "skills", "contact"}
    unknown = sorted(set(site) - known)
    if unknown:
        problems.append(f"site.json: fields the schema does not define: {', '.join(unknown)}")
    if problems:
        raise BuildError("\n".join(problems))

    def cut_checked(where: str, entry: dict, parts: list[str]) -> str:
        if entry.get("item") not in by_id:
            raise BuildError(f"site.json: {where}: item '{entry.get('item')}' does not exist")
        source = resolve(entry.get("from", ""), site, by_id)
        for part in parts:
            if not is_cut(part, source):
                raise BuildError(f"site.json: {where}: '{part}' is not a cut of {entry['from']}")
        return by_id[entry["item"]]["name"]

    highlights = []
    for number, entry in enumerate(site.get("highlights", []), start=1):
        if not (isinstance(entry, dict) and _text(entry.get("figure")) and _text(entry.get("text"))):
            raise BuildError(f"site.json: highlight {number} must have item, from, figure and text")
        whole = " ".join(filter(None, (entry.get("before"), entry.get("figure"), entry.get("text"))))
        label = cut_checked(f"highlight {number}", entry, [whole])
        highlights.append({"before": None, **entry, "label": label,
                           "figure_parts": split_figure(entry["figure"])})
    feature = site.get("feature")
    if feature:
        try:
            parts = [feature["label"], f"{feature['figure']} {feature['text']}", feature["note"]]
            parts += [f"{p['figure']} {p['text']}" for p in feature.get("pairs", [])]
        except (KeyError, TypeError):
            raise BuildError("site.json: feature must have item, from, label, figure, text "
                             "and note, and may have pairs of {figure, text}") from None
        feature = {"pairs": [], **feature, "name": cut_checked("feature", feature, parts)}
    name = site["name"].strip()
    first, _, last = name.partition(" ")
    contact = [{"line": None, "cta": None, **route, "mail": route["url"].startswith("mailto:")}
               for route in contact]
    return {"availability": None, "intro": None, **site, "highlights": highlights,
            "feature": feature, "skills": skills, "contact": contact,
            "first_name": first, "last_name": last or None}


# Layout.

def sub_columns(entries: list[dict]) -> None:
    """Within one lane, give overlapping entries side-by-side columns, the
    longest placed first. Writes x and w, as percentages of the lane, onto
    each entry. Projects sit left of the spine, so their first column is
    the one nearest the spine, on the right."""
    def overlaps(a, b):
        return a["first"] <= b["last"] and b["first"] <= a["last"]

    columns: list[list[dict]] = []
    for entry in sorted(entries, key=lambda e: (-e["months"], -e["last"])):
        index = 0
        while index < len(columns) and any(overlaps(o, entry) for o in columns[index]):
            index += 1
        if index == len(columns):
            columns.append([])
        columns[index].append(entry)
        entry["column"] = index
    shares = [45, 55] if len(columns) == 2 else [100 / max(1, len(columns))] * len(columns)
    for entry in entries:
        entry["gl"] = entry["gr"] = 0
        if not any(o is not entry and overlaps(o, entry) for o in entries):
            entry["x"], entry["w"] = 0, 100
            continue
        start, width = sum(shares[:entry["column"]]), shares[entry["column"]]
        if entry["lane"] == "builds":
            start = 100 - start - width
        entry["x"], entry["w"] = round(start, 3), round(width, 3)
        # A 3px gutter on each side that meets a neighbouring column.
        entry["gl"] = 3 if start > 0 else 0
        entry["gr"] = 3 if start + width < 100 else 0


def timeline_layout(items: list[dict], as_of: str, axis_start: str) -> dict:
    """Everything the timeline template places: the entries newest first, the
    month and year marks on the axis, and the band."""
    top, axis = month_index(as_of), month_index(axis_start)
    order = {item["id"]: n for n, item in enumerate(items)}
    # Newest first by start month, then by end month; ties keep the content
    # file's order. This is the order of the list in the HTML.
    entries = sorted(items, key=lambda i: (-i["first"], -i["last"], order[i["id"]]))
    for lane in TIMELINE_LANES:
        sub_columns([e for e in entries if e["lane"] == lane])

    band = next((e for e in entries if e["lane"] == "band"), None)
    seen_years = set()
    for entry in entries:
        entry["year"] = entry["start"][:4]
        entry["year_mark"] = entry["lane"] != "band" and entry["year"] not in seen_years
        if entry["year_mark"]:
            seen_years.add(entry["year"])
        if band and entry is not band:
            entry["band_place"] = ("after-band" if entry["first"] > band["last"]
                                   else "in-band" if entry["last"] >= band["first"] else "before-band")
        else:
            entry["band_place"] = None

    months = top - axis + 1
    marks = [{"label": month_name(m), "row": (top - m) * UNITS_PER_MONTH + 1, "n": n}
             for n, m in enumerate(range(top, axis - 1, -1), start=1)]
    years = []
    for year in range(top // 12, axis // 12 - 1, -1):
        december = min(year * 12 + 11, top)
        years.append({"year": year, "row": (top - december) * UNITS_PER_MONTH + 1,
                      "line": december != top})
    return {"entries": entries, "band": band, "rows": months * UNITS_PER_MONTH,
            "months": months, "marks": marks, "years": years,
            "lanes": [{"key": k, "label": LANE_LABELS[k]} for k in TIMELINE_LANES
                      if any(e["lane"] == k for e in entries)],
            "band_start_text": date_plain(date_phrase(band["start"], band["start"])) if band else None}


def project_grid(projects: list[dict]) -> None:
    """How many of the six grid columns each project card spans, on a wide
    screen (three to a row) and a medium one (two to a row). Tier 1 takes a
    full row; in a short last row the cards share its width."""
    rest = [p for p in projects if p["tier"] != 1]
    for project in projects:
        project["span_wide"] = project["span_mid"] = GRID_COLUMNS
    for per_row, key in ((3, "span_wide"), (2, "span_mid")):
        for start in range(0, len(rest), per_row):
            row = rest[start:start + per_row]
            for project in row:
                project[key] = GRID_COLUMNS // len(row)


def _num(value) -> str:
    """A number as CSS writes it: 45, 33.333, never 45.0."""
    return f"{value:g}" if isinstance(value, float) else str(value)


def layout_css(projects: list[dict], timeline: dict) -> str:
    """The positions the content decides, as custom properties on element
    ids. They live in a stylesheet rather than in style attributes, so the
    page's policy can refuse every inline style (CSP above). Every design
    reads the same properties."""
    lines = ["/* Generated by build.py from the content: the project grid and the",
             "   timeline's positions. Do not edit; edit content/ and rebuild. */"]
    for p in projects:
        lines.append(f"#{p['id']} {{ --span-wide: {p['span_wide']}; --span-mid: {p['span_mid']}; }}")
    lines.append(f"#tlx-grid {{ --rows: {timeline['rows']}; }}")
    for mark in timeline["marks"]:
        lines.append(f"#tlx-m-{mark['n']} {{ --row: {mark['row']}; }}")
    for year in timeline["years"]:
        lines.append(f"#tlx-y-{year['year']}, #tlx-yl-{year['year']} {{ --row: {year['row']}; }}")
    for e in timeline["entries"]:
        if e["lane"] == "band":
            lines.append(f"#tl-{e['id']} {{ --row: {e['row']}; --span: {e['span']}; }}")
        else:
            lines.append(f"#tl-{e['id']} {{ --row: {e['row']}; --span: {e['span']}; "
                         f"--x: {_num(e['x'])}%; --w: {_num(e['w'])}%; "
                         f"--gl: {e['gl']}px; --gr: {e['gr']}px; }}")
    return "\n".join(lines) + "\n"


# Designs.

def design_names() -> list[str]:
    """Every design folder, the default first, then by name."""
    names = sorted(p.name for p in DESIGNS.iterdir() if p.is_dir())
    return sorted(names, key=lambda n: (n != DEFAULT_DESIGN, n))


def load_design(name: str) -> dict:
    """A design's metadata, for the page and the gallery. The full rules a
    design must meet are tools/check_design.py's; the build refuses only
    what would stop it rendering, and never copies a file the check would
    refuse to look at: anything that is not a regular file."""
    folder = DESIGNS / name
    if not DESIGN_NAME_RE.match(name) or not folder.is_dir():
        available = ", ".join(design_names())
        raise BuildError(f"design '{name}' is not a folder in designs/. Available: {available}")
    meta_path = folder / "design.json"
    if not (folder / "design.css").is_file() or not meta_path.is_file():
        raise BuildError(f"design '{name}' needs design.css and design.json")
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise BuildError(f"designs/{name}/design.json is not valid JSON: {error}") from None
    if not isinstance(meta, dict) or not all(_text(meta.get(k)) for k in
                                             ("name", "author", "author_url", "description")):
        raise BuildError(f"designs/{name}/design.json needs name, author, author_url and "
                         f"description (run tools/check_design.py for every rule)")
    # Whether the design offers a dark theme: the page's colour-scheme tag
    # and the Dark switch follow it (ADR-0006, Changes, 2026-10-18).
    if not isinstance(meta.get("dark"), bool):
        raise BuildError(f"designs/{name}/design.json: dark must be true or false, saying "
                         f"whether the design offers a dark theme")
    files = []
    for path in sorted(folder.rglob("*")):
        if path.is_symlink() or not (path.is_file() or path.is_dir()):
            raise BuildError(f"designs/{name}: {path.relative_to(folder).as_posix()} is not a "
                             f"regular file or folder")
        if path.is_file() and path.name != "design.json":
            files.append(path.relative_to(folder).as_posix())
    preload = meta.get("preload", [])
    if not (isinstance(preload, list) and all(isinstance(p, str) and p in files
                                              and p.endswith(".woff2") for p in preload)):
        raise BuildError(f"designs/{name}/design.json: preload must list .woff2 files in the design")
    # The author's own live site built with the design, shown as "In use"
    # on its gallery card (ADR-0016).
    in_use = meta.get("in_use")
    if in_use is not None and not (_text(in_use) and in_use.startswith("https://")
                                   and urlsplit(in_use).hostname):
        raise BuildError(f"designs/{name}/design.json: in_use must be an https:// address")
    return {"slug": name, "name": meta["name"], "author": meta["author"],
            "author_url": meta["author_url"], "description": meta["description"],
            "dark": meta["dark"], "preload": preload, "files": files, "in_use": in_use,
            "in_use_host": urlsplit(in_use).hostname if in_use else None}


# The showcase.

def load_showcase() -> list[dict]:
    """Contributors' own sites, one folder per person, by folder name. The
    full rules are tools/check_showcase.py's; the build refuses only what
    would stop it rendering a card."""
    if not SHOWCASE.is_dir():
        return []
    # Each screenshot's header gives its size, so the page reserves each
    # picture's box before it loads (ADR-0009). The reader is the showcase
    # check's, which the template cleanup removes with showcase/.
    sys.path.insert(0, str(ROOT / "tools"))
    from check_showcase import ImageError, shown_size
    entries = []
    for folder in sorted(p for p in SHOWCASE.iterdir() if p.is_dir() and not p.is_symlink()):
        where = f"showcase/{folder.name}"
        try:
            entry = json.loads((folder / "entry.json").read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise BuildError(f"{where}/entry.json cannot be read: {error}") from None
        if not (isinstance(entry, dict) and _text(entry.get("name"))
                and _text(entry.get("url")) and entry["url"].startswith("https://")
                and urlsplit(entry["url"]).hostname):
            raise BuildError(f"{where}/entry.json needs a name and an https:// url "
                             f"(run tools/check_showcase.py for every rule)")
        shots = [p.name for p in sorted(folder.iterdir())
                 if SHOWCASE_IMAGE_RE.fullmatch(p.name) and p.is_file() and not p.is_symlink()]
        if len(shots) != 1:
            raise BuildError(f"{where}/ needs exactly one screenshot, a .png, .jpg, .jpeg or "
                             f".webp file")
        try:
            width, height = shown_size(folder / shots[0])
        except (ImageError, KeyError, struct.error) as error:
            raise BuildError(f"{where}/{shots[0]} gives no size a browser would show: {error} "
                             f"(run tools/check_showcase.py for every rule)") from None
        shapes = showcase_shapes(width, height)
        description = entry.get("description")
        entries.append({"login": folder.name, "name": entry["name"], "url": entry["url"],
                        "host": urlsplit(entry["url"]).hostname,
                        "description": description if _text(description) else None,
                        "screenshot": f"{where}/{shots[0]}", "shown": (width, height), "shapes": shapes,
                        "card": f"{where}/{SHOWCASE_CARD}", "full": f"{where}/{SHOWCASE_FULL}",
                        "card_size": shapes[SHOWCASE_CARD]["size"], "full_size": shapes[SHOWCASE_FULL]["size"]})
    return entries


# Environment and output.

def check_environment() -> None:
    """Refuse to build outside a virtual environment or against a package
    version other than the pinned one. The output depends on the templating
    version, and a build that silently used another would differ from the
    expected output with no visible cause."""
    if sys.prefix == sys.base_prefix:
        raise BuildError("not running inside a virtual environment. "
                         "Create and activate .venv first; see docs/reference/commands.md")
    text = REQUIREMENTS.read_text(encoding="utf-8")
    # Join the continuation lines, then read each requirement's name and pin.
    for line in text.replace("\\\n", " ").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        requirement = line.split()[0]
        name, _, pinned = requirement.partition("==")
        if not pinned:
            raise BuildError(f"requirements.txt: '{requirement}' is not pinned with ==")
        try:
            installed = metadata.version(name)
        except metadata.PackageNotFoundError:
            raise BuildError(f"{name} is not installed in this environment. "
                             "Run: python -m pip install -r requirements.txt") from None
        if installed != pinned:
            raise BuildError(f"{name} {installed} is installed but requirements.txt pins {pinned}")


def environment():
    # Imported here, after check_environment, so a build outside the venv
    # reports that rather than a bare ImportError.
    import jinja2

    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES),
        # Always on. select_autoescape() keys on the file extension and would
        # leave these .html.j2 templates unescaped.
        autoescape=True,
        undefined=jinja2.StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def render(env, template: str, context: dict) -> str:
    import jinja2

    try:
        return env.get_template(template).render(**context)
    except jinja2.TemplateError as error:
        raise BuildError(f"template error in {template}: {error}") from None


def _year_month(value: str) -> str:
    if not YM_RE.match(value):
        raise argparse.ArgumentTypeError(f"'{value}' is not a YYYY-MM month")
    return value


def copy_design(design: dict, target: Path) -> None:
    for relative in design["files"]:
        if relative == PREVIEW_FILE:
            continue
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(DESIGNS / design["slug"] / relative, destination)


def build(out: Path, as_of: str, design_override: str | None, gallery: bool) -> str:
    config = load_config(CONFIG)
    items, axis_start = load_items(ITEMS, as_of, config)
    site = load_site(SITE, items)
    by_lane = {lane: [i for i in items if i["lane"] == lane] for lane in LANE_LABELS}
    project_grid(by_lane["builds"])
    timeline = timeline_layout(items, as_of, axis_start)
    shown = {"intro": True, "projects": bool(by_lane["builds"]), "timeline": bool(items),
             "work": bool(by_lane["work"]), "education": bool(by_lane["band"]),
             "certifications": bool(by_lane["certifications"]), "skills": bool(site["skills"]),
             "contact": True}
    sections = [{"id": sid, "label": label} for sid, label in SECTIONS if shown[sid]]
    for n, section in enumerate(sections, start=1):
        section["n"] = f"{n:02d}"
    cv_pdf = config["cv_pdf"] or None

    names = design_names() if gallery else [design_override or config["design"]]
    designs = [load_design(name) for name in names]
    showcase = load_showcase() if gallery else []
    env = environment()

    base = {
        "as_of": as_of,
        "site": site,
        "sections": sections,
        "section": {s["id"]: s for s in sections},
        "projects": by_lane["builds"],
        "work": by_lane["work"],
        "degree": by_lane["band"][0] if by_lane["band"] else None,
        "certifications": by_lane["certifications"],
        "timeline": timeline,
        "csp": CSP,
        "credit": config["credit"],
        "project_name": PROJECT_NAME,
        "project_url": PROJECT_URL,
    }
    pages: dict[str, str] = {}
    if gallery:
        for design in designs:
            pages[f"designs/{design['slug']}/index.html"] = render(env, "base.html.j2", {
                **base, "root": DEMO_ROOT, "design": design, "design_href": "",
                "cv": f"{DEMO_ROOT}{cv_pdf}" if cv_pdf else None, "demo": True})
        pages["index.html"] = render(env, "gallery.html.j2", {
            "as_of": as_of, "csp": CSP, "designs": designs, "project_name": PROJECT_NAME,
            "project_url": PROJECT_URL, "preview_file": PREVIEW_FILE,
            "preview_size": PREVIEW_SIZE, "sample_name": site["name"], "showcase": showcase})
    else:
        design = designs[0]
        pages["index.html"] = render(env, "base.html.j2", {
            **base, "root": "", "design": design, "design_href": "design/",
            "cv": cv_pdf, "demo": False})

    # Everything is rendered; now write, into a fresh folder that replaces
    # the old output only once it is complete.
    out.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".build-", dir=out.parent))
    try:
        for relative, text in pages.items():
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8", newline="\n")
        static = staging / "static"
        static.mkdir()
        for name in ("site.js", "knot.js", "base.css"):
            shutil.copyfile(STATIC_SRC / name, static / name)
        (static / "layout.css").write_text(layout_css(by_lane["builds"], timeline),
                                           encoding="utf-8", newline="\n")
        if gallery:
            for name in ("gallery.css", "gallery.js"):
                shutil.copyfile(STATIC_SRC / name, static / name)
            for design in designs:
                copy_design(design, staging / "designs" / design["slug"])
            # The showcase's served copies come later, from the screenshot
            # job, as the previews do; the authors' own files stay here.
        else:
            copy_design(designs[0], staging / "design")
        if cv_pdf:
            target = staging / cv_pdf
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / cv_pdf, target)
        # A file GitHub Pages reads: serve the files as they are, without
        # Jekyll. The deploy workflow uploads this folder as the site.
        (staging / ".nojekyll").write_text("", encoding="utf-8")
        if out.exists():
            shutil.rmtree(out)
        staging.rename(out)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    what = (f"the gallery of {len(designs)} design(s) and {len(showcase)} showcase site(s)" if gallery
            else f"the site in the '{designs[0]['slug']}' design")
    return (f"built {what}: {len(items)} item(s), as of {as_of}, "
            f"into {out.relative_to(ROOT).as_posix() if out.is_relative_to(ROOT) else out}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the site or the gallery into _site/.")
    parser.add_argument("--as-of", type=_year_month, metavar="YYYY-MM",
                        help="the month 'present' resolves to; default: the current UTC month")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--design", metavar="NAME", help="build the site in this design instead "
                                                       "of the one config.json names")
    mode.add_argument("--gallery", action="store_true",
                      help="build every design and the gallery page")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, metavar="DIR",
                        help="where to write; default: _site/")
    args = parser.parse_args(argv)
    as_of = args.as_of or datetime.now(timezone.utc).strftime("%Y-%m")
    try:
        check_environment()
        print(build(args.out.resolve(), as_of, args.design, args.gallery))
    except BuildError as error:
        print(f"build failed:\n{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
