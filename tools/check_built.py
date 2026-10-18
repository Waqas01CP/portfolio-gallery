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
  - with --previews, every design in a gallery has its preview image;
    without it, a missing preview is not reported, because the previews
    are taken after the build.

Exit 0 when everything passes; 1 when anything fails, each printed with
its file; 2 when the folder holds no built page. Standard library only.
"""

from __future__ import annotations

import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build import CSP, PREVIEW_FILE  # noqa: E402
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
        if inside and "hidden" in a and a.get("aria-hidden") != "true":
            name = a.get("id") or a.get("class") or tag
            self.problems.append(f"<{tag}> '{name}' is hidden inside a section but not "
                                 f"aria-hidden=\"true\"")

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        while self.stack:
            open_tag = self.stack.pop()
            self.in_section.pop()
            if open_tag == tag:
                break

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
    for url in page.loads:
        # A gallery's previews are taken after the build, by the screenshot
        # job (tools/screenshots.py); --previews requires them, and the
        # deploy workflow passes it once they are in.
        if not previews and re.fullmatch(rf"designs/[a-z0-9-]+/{re.escape(PREVIEW_FILE)}", url):
            continue
        _, problem = resolve(path.parent, root, url)
        if problem:
            problems.append(problem)
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
        else:
            _, problem = resolve(path.parent, root, href.split("#", 1)[0])
            if problem:
                problems.append(f"the link {problem}")
    return problems


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
        for demo in sorted((root / "designs").glob("*/index.html")):
            if not (demo.parent / PREVIEW_FILE).is_file():
                print(f"FAIL designs/{demo.parent.name}: no {PREVIEW_FILE}; run tools/screenshots.py")
                failures += 1
    print(f"\n{len(pages)} page(s), {failures} problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
