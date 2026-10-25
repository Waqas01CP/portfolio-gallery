"""Trace every piece of text on the built page to your CV, and back.

  python tools/check_content.py [--cv content/cv.md] [--page _site/index.html]
                                [--content samples/<design>]

Your CV is the source of truth for what your site claims. This reads it,
in the Markdown shape docs/reference/cv-format.md describes, and the built
page (not the content files, because the page is what a reader and a
crawler see), and checks both directions. By default it reads the CV that
content/config.json names and the page `python build.py` writes.

  Trace. The page is split into blocks of text: every paragraph, heading,
  list item, summary and button, plus what a crawler also reads (the
  title, the meta description, alt text and aria-label). Each block must
  be one of:
    - a cut of one CV paragraph: the same words in the same order, some
      left out, with every number still followed by the word that follows
      it in the CV, so "212 automated tests" cannot become "12 automated
      tests";
    - a run of such cuts from one CV entry, split where the page's own
      markup splits it, such as a timeline entry's dates, then its title;
    - interface text: the engine's own labels ("In depth", "Back to top"),
      and the words site.json and items.json give the page's controls
      rather than claims (contact labels, lines and buttons, and proof link
      labels), each listed in the report so none passes unseen.
  Anything else fails, with the block printed.

  Coverage. Every CV bullet, the summary and the intro, every sentence of
  every project's italic line, every skills line, every course, every
  certificate with its link, every entry's title and dates, and each line
  of the header must appear on the page whole, in the CV's word order; and
  every link that ends a project's italic line must be on the page as a
  link, with its label and its address.

  Sources. Every item's `source` in items.json must name an entry the CV
  has, as "<section> / <entry>".

A failure names the CV file and its line: for text the CV lacks, the
nearest CV line, when one is close; for CV text the page lacks, the line
it is on. It ends with what to do: change the page's content files to
match the CV, or the CV to match the page. Editing site.json or items.json
alone is the usual cause.

Exit 0 when all pass, 1 when any fails, 2 when the CV or the page is
missing. Content trace off in config.json is exit 0 with a line saying so,
never a silent pass. Standard library only.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
PAGE = ROOT / "_site" / "index.html"

LONG_MONTHS = {"january": "jan", "february": "feb", "march": "mar", "april": "apr",
               "june": "jun", "july": "jul", "august": "aug", "september": "sep",
               "october": "oct", "november": "nov", "december": "dec"}
MONTHS = set(LONG_MONTHS.values()) | {"may"}
WORD_RE = re.compile(r"\d+(?:[.,]\d+)*%?|[^\W\d_]+")
NUMBER_RE = re.compile(r"^\d")
YEAR_RE = re.compile(r"^(19|20)\d\d$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
LINK_GROUP_RE = re.compile(r"\s*\(((?:\[[^\]]+\]\([^)]+\)\s*(?:\|\s*)?)+)\)\s*$")

# The engine's own words: what the page says about itself rather than about
# its owner. Removed from a block only when the block fails as it stands.
ENGINE_TEXT = [
    "Skip to main content", "Sections menu", "Sections", "Dark theme", "Dark",
    "Intro", "Projects", "Timeline", "Work", "Education", "Certifications", "Skills",
    "Contact", "Degree", "Results", "Stack", "Close in depth", "In depth", "Close",
    "View credential", "Go to full entry", "Show or hide lanes", "Months to scale",
    "No lanes selected", "Back to top", "Pause the moving strip", "Pause", "Play",
    "Download CV (PDF)", "Relevant coursework", "Built with", "portfolio-gallery",
]
# Section and item numbers beside the real name, decoration, dropped by
# their markup rather than by a pattern, which would also drop a figure.
ORDINAL_CLASSES = {"sec-n", "mnav-n", "mnav-num", "depth-n", "skill-n"}

BLOCK_TAGS = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "div", "section", "article",
              "header", "footer", "nav", "main", "ul", "ol", "summary", "details", "button",
              "title", "body", "html", "head", "dl", "dt", "dd", "figure", "figcaption"}
TEXT_ATTRIBUTES = ("alt", "aria-label", "title")


def words(text: str) -> list[str]:
    return [LONG_MONTHS.get(w, w) for w in WORD_RE.findall(html.unescape(text).lower())]


def sentences(text: str) -> list[list[str]]:
    """The words of each sentence or clause, split at a full stop, colon or
    semicolon followed by a space."""
    return [words(part) for part in re.split(r"(?<=[.:;])\s+", html.unescape(text))]


def is_subsequence(part: list[str], source: list[str]) -> bool:
    remaining = iter(source)
    return all(word in remaining for word in part)


def numbers_hold(text: str, source: list[str]) -> bool:
    """Every number in the text that has a next word in its own sentence
    keeps that next word, as in the source."""
    pairs = set(zip(source, source[1:]))
    return all((a, b) in pairs for part in sentences(text)
               for a, b in zip(part, part[1:]) if NUMBER_RE.match(a))


# The CV.

def plain(line: str) -> str:
    """A CV line as text: emphasis dropped, a link kept as its text."""
    text = LINK_RE.sub(r"\1", line)
    return text.replace("**", "").replace("*", "").removeprefix("- ").strip()


def comparable(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text)).strip().lower()


class CV:
    """The CV read as sections (##), entries (### or, in a section without
    them, each line) and paragraphs, with the raw lines kept for links and
    every line's number kept for the report."""

    def __init__(self, text: str) -> None:
        # A comment becomes as many line breaks as it held, so line numbers hold.
        text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group().count("\n"), text, flags=re.S)
        self.name = ""
        self.name_at = 0
        self.header: list[str] = []
        self.header_at: list[int] = []
        self.sections: dict[str, list[dict]] = {}
        self.lines: list[tuple[int, str]] = []
        section = entry = None
        for number, raw in enumerate(text.splitlines(), 1):
            line = raw.strip()
            if not line:
                continue
            self.lines.append((number, line))
            if line.startswith("# "):
                self.name, self.name_at = line[2:].strip(), number
                continue
            if line.startswith("## "):
                section = line[3:].strip()
                self.sections[section] = []
                entry = None
                continue
            if line.startswith("### "):
                heading = line[4:].strip()
                title, _, dates = heading.partition(" | ")
                entry = {"heading": title.strip(), "dates": dates.strip(), "raw": [], "at": number, "raw_at": []}
                self.sections.setdefault(section or "", []).append(entry)
                continue
            if section is None:
                self.header.append(line)
                self.header_at.append(number)
            elif entry is not None:
                entry["raw"].append(line)
                entry["raw_at"].append(number)
            else:
                self.sections[section].append({"heading": "", "dates": "", "raw": [line],
                                               "at": number, "raw_at": [number]})
        # Every paragraph: each line on its own, the heading, the header.
        self.entries: list[list[list[str]]] = []
        self.paragraphs: list[list[str]] = [words(self.name)] + [words(plain(l)) for l in self.header]
        self.entries.append(list(self.paragraphs))
        for entries in self.sections.values():
            for e in entries:
                lines = [words(e["heading"]), words(e["dates"])] + [words(plain(l)) for l in e["raw"]]
                lines = [l for l in lines if l]
                self.paragraphs += lines
                self.entries.append(lines)

    def entry_names(self) -> set[str]:
        """What an item's source may name: '<section> / <entry heading>', or
        in a section of plain lines, '<section> / <the line's link text, or
        its words before a colon>'."""
        names = set()
        for section, entries in self.sections.items():
            names.add(section)
            for e in entries:
                if e["heading"]:
                    names.add(f"{section} / {e['heading']}")
                else:
                    links = LINK_RE.findall(e["raw"][0])
                    label = links[0][0] if links else plain(e["raw"][0]).split(":")[0]
                    names.add(f"{section} / {label}")
        return names

    def nearest(self, text: str) -> tuple[int, str] | None:
        """The CV line most like the text, by the share of the text's
        characters it holds in runs of three or more, when that share is at
        least half: the line a user most likely meant to match."""
        target = comparable(text)
        if not target:
            return None
        best, best_key = None, (0.0, 0.0)
        for number, line in self.lines:
            other = comparable(plain(line.lstrip("#")))
            matcher = SequenceMatcher(None, target, other, autojunk=False)
            shared = sum(b.size for b in matcher.get_matching_blocks() if b.size >= 3)
            key = (shared / len(target), matcher.ratio())
            if key[0] >= 0.5 and (best is None or key > best_key):
                best, best_key = (number, line), key
        return best


# The page.

class Blocks(HTMLParser):
    """Blocks of text, each with the pieces its inline markup splits it into."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[tuple[str, list[str]]] = []
        self.links: list[tuple[str, str]] = []
        self._pieces: list[str] = [""]
        self._skip = 0
        self._ordinal = False
        self._link: list | None = None

    def _flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self._pieces)).strip()
        if text:
            self.blocks.append((text, [p.strip() for p in self._pieces if p.strip()]))
        self._pieces = [""]

    def _attribute(self, text: str) -> None:
        if text.strip():
            self.blocks.append((text.strip(), [text.strip()]))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self._skip += 1
        if tag == "span" and ORDINAL_CLASSES & set((attrs.get("class") or "").split()):
            self._ordinal = True
        if tag in BLOCK_TAGS:
            self._flush()
        elif tag == "br":
            self._pieces.append(" ")
        else:
            self._pieces.append("")
        for name in TEXT_ATTRIBUTES:
            self._attribute(attrs.get(name) or "")
        if tag == "meta" and attrs.get("name") == "description":
            self._attribute(attrs.get("content") or "")
        if tag == "a" and attrs.get("href"):
            self._link = [attrs["href"], ""]

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1
        if tag == "span":
            self._ordinal = False
        if tag == "a" and self._link:
            self.links.append((self._link[0], re.sub(r"\s+", " ", self._link[1]).strip()))
            self._link = None
        if tag in BLOCK_TAGS:
            self._flush()
        else:
            self._pieces.append("")

    def handle_data(self, data):
        if self._ordinal and re.fullmatch(r"\d{2}", data.strip()):
            return
        if not self._skip:
            self._pieces[-1] += data
            if self._link is not None:
                self._link[1] += data


class Tracer:
    def __init__(self, cv: CV, interface: list[str]) -> None:
        self.cv = cv
        self.interface = sorted(set(interface), key=len, reverse=True)

    def strip_interface(self, text: str) -> str:
        for phrase in self.interface:
            text = re.sub(r"(?<![\w'])" + re.escape(phrase) + r"(?![\w'])", " ", text, flags=re.I)
        return text

    def is_cut(self, text: str, paragraphs: list[list[str]]) -> bool:
        block = words(text)
        return bool(block) and any(is_subsequence(block, p) and numbers_hold(text, p)
                                   for p in paragraphs)

    def interface_only(self, text: str) -> bool:
        remainder = words(self.strip_interface(text))
        return not remainder or all(w in MONTHS or YEAR_RE.match(w) for w in remainder)

    def joined(self, pieces: list[str]) -> bool:
        """Every piece the markup splits a block into is interface text or a
        cut of a paragraph, all from one CV entry. The split points are the
        page's, never chosen here, so words cannot be gathered from anywhere."""
        for entry in self.cv.entries:
            if all(self.interface_only(piece) or self.is_cut(piece, entry)
                   or self.is_cut(self.strip_interface(piece), entry) for piece in pieces):
                return True
        return False

    def trace(self, text: str, pieces: list[str]) -> str | None:
        paragraphs = self.cv.paragraphs
        if self.is_cut(text, paragraphs):
            return "cut"
        if self.interface_only(text):
            return "interface"
        if self.is_cut(self.strip_interface(text), paragraphs):
            return "cut"
        if self.joined(pieces):
            return "joined"
        return None


def coverage(cv: CV, page: Blocks) -> dict[str, list[tuple[str, bool, int]]]:
    """Each group's CV text, whether the page holds it, and its CV line."""
    page_words = words(" ".join(text for text, _ in page.blocks))
    page_text = " " + " ".join(page_words) + " "
    hrefs = {href for href, _ in page.links}
    link_pairs = {(href, label) for href, label in page.links}

    def present(text: str) -> bool:
        w = words(text)
        return bool(w) and (" " + " ".join(w) + " ") in page_text

    def link_present(label: str, url: str) -> bool:
        return url in hrefs and any(h == url and words(label) and
                                    is_subsequence(words(label), words(text))
                                    for h, text in link_pairs)

    groups: dict[str, list[tuple[str, bool, int]]] = {}

    def add(group: str, at: int, text: str, ok: bool | None = None) -> None:
        groups.setdefault(group, []).append((text, present(text) if ok is None else ok, at))

    add("name", cv.name_at, cv.name)
    for at, line in zip(cv.header_at, cv.header):
        links = LINK_RE.findall(line)
        if links:
            for label, url in links:
                add("header links", at, f"{label} ({url})", link_present(label, url) or present(label))
        else:
            for part in line.split(" | "):
                add("header", at, part)
    for section, entries in cv.sections.items():
        key = section.lower()
        for e in entries:
            if e["heading"]:
                title = e["heading"].split(": ")[0].split(", ")[0]
                add("entry titles", e["at"], title)
                if e["dates"]:
                    add("entry dates", e["at"], e["dates"])
            for at, raw in zip(e["raw_at"], e["raw"]):
                line = plain(raw)
                if raw.startswith("- ") and key == "certifications":
                    for label, url in LINK_RE.findall(raw):
                        add("certificates", at, f"{label} ({url})", present(label) and url in hrefs)
                    match = re.search(r"\(([^()]*\d{4})\)\s*$", raw)
                    if match:
                        add("certificate dates", at, match[1])
                elif raw.startswith("- ") and key == "skills":
                    add("skills lines", at, line)
                elif raw.startswith("- "):
                    add("bullets", at, line)
                elif raw.startswith("*") and not raw.startswith("**"):
                    italic = raw
                    tail = LINK_GROUP_RE.search(raw)
                    if tail:
                        for label, url in LINK_RE.findall(tail.group(1)):
                            add("project links", at, f"{label} ({url})", link_present(label, url))
                        italic = raw[:tail.start()]
                    for sentence in re.split(r"(?<=\.) ", plain(italic)):
                        add("italic-line sentences", at, sentence)
                elif re.match(r"^relevant coursework:", line, re.I):
                    for course in line.split(":", 1)[1].split(","):
                        add("courses", at, course)
                elif re.match(r"^[A-Z][\w ]{0,30}: ", line):
                    add("labelled lines", at, line.split(": ", 1)[1])
                else:
                    add("paragraphs and lines", at, line)
    return groups


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Trace the built page to your CV, and back.")
    parser.add_argument("--cv", type=Path, help="your CV; default: config.json's cv_source")
    parser.add_argument("--page", type=Path, default=PAGE, help="the built page; default _site/index.html")
    parser.add_argument("--content", type=Path, default=CONTENT,
                        help="the content folder the page was built from; default content/. "
                             "A sample person's is samples/<design>/ (ADR-0018)")
    # Page text can hold characters the console cannot write, as on Windows;
    # write them escaped rather than stop the report.
    sys.stdout.reconfigure(errors="backslashreplace")
    args = parser.parse_args(argv)
    folder = args.content
    config = json.loads((folder / "config.json").read_text(encoding="utf-8"))
    if args.cv is None:
        if not config.get("content_trace", True):
            print(f"Content trace is off in {folder.name}/config.json (content_trace: false); "
                  f"nothing was checked.")
            return 0
        args.cv = ROOT / config.get("cv_source", "")
    if not args.cv.is_file():
        print(f"no CV at {args.cv}", file=sys.stderr)
        return 2
    if not args.page.is_file():
        print(f"no built page at {args.page}; run python build.py first", file=sys.stderr)
        return 2

    try:
        shown = args.cv.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        shown = str(args.cv)
    cv = CV(args.cv.read_text(encoding="utf-8"))
    site = json.loads((folder / "site.json").read_text(encoding="utf-8"))
    items = json.loads((folder / "items.json").read_text(encoding="utf-8"))
    owned = [t for route in site.get("contact", []) for k in ("label", "line", "cta")
             if (t := route.get(k))]
    owned += [link["label"] for item in items for link in item.get("proof", [])]
    # The footer's credit names the design and its author (ADR-0016, D2).
    try:
        design = json.loads((ROOT / "designs" / config.get("design", "") / "design.json")
                            .read_text(encoding="utf-8"))
        owned.append(f"design {design['name']} by {design['author']}")
    except (OSError, ValueError, KeyError, TypeError):
        pass
    tracer = Tracer(cv, ENGINE_TEXT + owned)

    page = Blocks()
    page.feed(args.page.read_text(encoding="utf-8"))
    page.close()

    failures, counts = [], {"cut": 0, "joined": 0, "interface": 0}
    for text, pieces in page.blocks:
        if not words(text):
            continue
        how = tracer.trace(text, pieces)
        if how is None:
            failures.append((text, pieces))
        else:
            counts[how] += 1
    print(f"Content trace: the built page against your CV, {shown}, and back.\n")
    print(f"Trace: {sum(counts.values())} blocks traced, {len(failures)} not traced.")
    print(f"  cut of one CV paragraph:     {counts['cut']}")
    print(f"  pieces cut from one entry:   {counts['joined']}")
    print(f"  interface text only:         {counts['interface']}")
    print(f"  interface text from site.json and items.json, approved as labels: "
          f"{', '.join(sorted(set(owned))) or 'none'}")
    for text, pieces in failures:
        print(f"  NOT TRACED: {text[:160]}")
        # The pieces the markup splits the block into that fail on their
        # own, so a joined block points at the part that is new.
        alone = [p for p in pieces if words(p) and tracer.trace(p, [p]) is None] or [text]
        for piece in alone:
            what = "" if piece == text else f'"{piece[:80]}": '
            near = cv.nearest(piece)
            if near:
                print(f"    {what}nearest in {shown}, line {near[0]}: {plain(near[1])[:160]}")
            else:
                print(f"    {what}no line of {shown} is close")

    missing = 0
    print("\nCoverage: CV text found whole on the page, in the CV's word order.")
    for group, results in coverage(cv, page).items():
        found = sum(ok for _, ok, _ in results)
        missing += len(results) - found
        print(f"  {group}: {found} of {len(results)}")
        for text, ok, at in results:
            if not ok:
                print(f"    MISSING: {text[:160]} ({shown}, line {at})")

    names = cv.entry_names()
    unknown = [(i.get("id"), i.get("source")) for i in items if i.get("source") not in names]
    print(f"\nSources: {len(items) - len(unknown)} of {len(items)} items name a CV entry.")
    for item_id, source in unknown:
        print(f"  NO SUCH ENTRY: item '{item_id}' names '{source}'")

    passed = not failures and not missing and not unknown
    print("\nPASS" if passed else "\nFAIL")
    if not passed:
        print(f"\nWhat to do: the page and your CV, {shown}, must say the same things. The page's words "
              f"come from content/site.json and content/items.json, so a change to either usually needs "
              f"the same change in {shown}.")
        if failures:
            print(f"  NOT TRACED: the page says something {shown} does not. Add the text to {shown}, "
                  "or change site.json or items.json to match the CV line shown.")
        if missing:
            print(f"  MISSING: {shown} says something the page does not. Add it to site.json or "
                  f"items.json, or take it out of {shown}.")
        if unknown:
            print(f"  NO SUCH ENTRY: an item's \"source\" in items.json must name an entry of {shown}, "
                  "as \"<section> / <entry title>\".")
        print("  To publish without this check, set \"content_trace\": false in content/config.json "
              "(docs/reference/cv-format.md).")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
