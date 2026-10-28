"""The standing checks that need a browser, run in headless Chrome.

  python tools/check_browser.py [_site] [--quick] [--axe FILE] [--only NAME[,NAME]]
                                [--designs NAME[,NAME]] [--skip-gallery-page]

Serves a built site or gallery on 127.0.0.1 and checks every page in
headless Chrome, each in a fresh browsing context of a browser with its
own empty profile (tools/cdp.py). Every check is listed in
docs/reference/standing-checks.md with the case built to defeat it.

  tree        In full accessibility mode, as a screen reader switches it on,
              the tree at load equals the tree of the same page without the
              layout-skipping rule in base.css: at 360 and 1366 px, light and
              dark, scripts on and off. In default mode it holds no node the
              page without the rule lacks. Exactly one "Sections" navigation
              is exposed at each width.
  keyboard    Each "In depth" panel: Tab reaches its control, Enter opens it
              and its text enters the tree, Tab moves into it, Close closes
              it and focus returns to the control, and the control closes it
              too. A Tab walk through the page never stops inside
              aria-hidden content.
  joins       No two words a screen reader would read as one: NVDA's lines
              modelled from the tree, every section laid out, at 360 and
              1366 px (docs/reference/standing-checks.md).
  anchors     Every in-page link target, reached by its link and by its
              address with the #, scripts on and off, at 360 and 1366 px,
              lands within 3 px of its scroll margin or at the page's end.
  words       Gallery only: every design shows the same words as the page
              with no design at all, so a design can neither hide content
              nor add text of its own through CSS.
  requests    Nothing is requested from another origin, the page breaks no
              rule of its Content-Security-Policy, and no script error is
              thrown. Checked on every load the other checks make.
  motion      Under reduced motion, no animation frame is requested and no
              animation runs, over 3 seconds.
  packing     Gallery only, the showcase's cards (ADR-0016, Changes,
              2026-10-20), at 390 and 1366 px, light and dark, packed by
              static/gallery.js, by Chrome's own grid-lanes (switched on
              with its experimental features, as Safari ships them), and
              with scripts off: every picture's box is its reserved size
              before it loads and stays so after, within the shape limits;
              no card sits above the one before it by more than 1em, the
              tolerance grid-lanes itself allows, so the eye meets the
              cards in folder order; Tab reaches them in folder order; and,
              packed, no gap is left under a card. With scripts off and no
              grid-lanes the cards sit in rows, gaps allowed.
  overlay     Gallery only, the showcase's larger copy (Brief 13, Addendum
              1; ADR-0016, Changes, 2026-10-23), at 390 and 1366 px, light
              and dark. At load the closed overlay is not in the tree. Tab
              to the first card and Enter: the page's dialog opens as a
              modal, named, focus inside it, with a visible Close button
              of at least 24 px named "Close", and the card's own picture
              loaded, whole within the window and in its own proportions,
              never enlarged; with --axe, axe-core's default rules with it
              open and closed. Escape, the Close button and a click
              outside the picture each close it and put focus back on the
              card's link. With scripts off, nothing opens: Enter on the
              card opens the picture itself, as a plain link.
  axe         With --axe FILE, axe-core's default rules at 360 and 1366 px,
              light, device dark and switched dark, panels closed and open.
              The checks workflow fetches axe.min.js by exact version and
              checks its SHA-512 first (ADR-0011); locally, fetch it as
              docs/reference/commands.md says. Without --axe this check is
              not run, and the report says so.

--quick runs one load per cell and the narrow width only where a check
allows it, for iterating; a pass with --quick is not a pass of the
standing checks.

--designs checks only the named designs' demos in a gallery, and
--skip-gallery-page leaves out the gallery page's own checks: tools/ci.py
passes them when a run looks only at what a change alters (ADR-0019). A
name the gallery lacks is a usage error, so a typo cannot check nothing.

Exit 0 when every check run passes; 1 when any fails, each failure printed
with its page and cell; 2 when the folder holds no built page. Chrome
missing is exit 1, naming where it was looked for (gate D).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build import SHOWCASE_TALL, SHOWCASE_WIDE  # noqa: E402
from cdp import CDPError, Chrome, MissingTool, Server  # noqa: E402

WIDTHS = ((360, 780), (1366, 900))
RULE_LINES = (".page > .sec { content-visibility: auto;",
              "html:has(:target) .page > .sec { content-visibility: visible; }")
LAYOUT_ALL = ".page > .sec { content-visibility: visible !important }"
READ_AFTER = 1.5

# Injected before any page script, in the page's own world: counts
# animation frames requested, keeps script errors for the report, and
# counts the idle callbacks still to run.
INSTRUMENT = """
window.__pg = { frames: 0, errors: [], idle: 0 };
const __raf = window.requestAnimationFrame.bind(window);
window.requestAnimationFrame = (fn) => { window.__pg.frames += 1; return __raf(fn); };
window.addEventListener('error', (e) => window.__pg.errors.push(String(e.message)));
if (window.requestIdleCallback) {
  const __ric = window.requestIdleCallback.bind(window);
  window.requestIdleCallback = (fn, options) => {
    window.__pg.idle += 1;
    return __ric((deadline) => { window.__pg.idle -= 1; fn(deadline); }, options);
  };
}
"""
# site.js starts the page, the strip and its pause button among it, from
# an idle callback with a 1.5 s timeout, the same 1.5 s the tree is read
# after. On the first load in a newly started Chrome the start came after
# the read in 1 of 15 tries (2,273 ms; 2026-10-23), and the tree check
# failed on a page that was right. So the tree is read once every idle
# callback has run, waiting at most this long.
STARTED_WITHIN = 10.0


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.notes: list[str] = []
        self.counts: dict[str, int] = {}

    def fail(self, check: str, page: str, message: str) -> None:
        self.failures.append(f"[{check}] {page}: {message}")

    def ran(self, check: str, n: int = 1) -> None:
        self.counts[check] = self.counts.get(check, 0) + n


# The served variants.

def make_variants(root: Path, work: Path) -> dict[str, Path]:
    """The page as built; without the layout-skipping rule; and bare, with no
    design stylesheet at all (and without the rule, so every section has its
    layout)."""
    variants = {"built": root}
    norule = work / "norule"
    shutil.copytree(root, norule)
    base = norule / "static" / "base.css"
    text = base.read_text(encoding="utf-8")
    kept = [line for line in text.splitlines() if not line.strip().startswith(RULE_LINES)]
    if not any(line.strip().startswith(RULE_LINES[0]) for line in text.splitlines()):
        raise SystemExit("base.css no longer holds the layout-skipping rule this check "
                         "removes; update RULE_LINES in tools/check_browser.py")
    base.write_text("\n".join(kept) + "\n", encoding="utf-8")
    variants["norule"] = norule
    bare = work / "bare"
    shutil.copytree(norule, bare)
    for css in bare.rglob("design.css"):
        css.write_text("", encoding="utf-8")
    variants["bare"] = bare
    return variants


# Reading the accessibility tree.

def walk(nodes: list[dict]):
    """The tree's nodes in document order, from the root."""
    by_id = {n["nodeId"]: n for n in nodes}
    roots = [n for n in nodes if not n.get("parentId")]
    stack = list(reversed(roots[:1]))
    while stack:
        node = stack.pop()
        yield node
        stack.extend(by_id[c] for c in reversed(node.get("childIds", [])) if c in by_id)


def _value(node: dict, key: str) -> str:
    return str((node.get(key) or {}).get("value") or "")


def tree_lists(nodes: list[dict]) -> tuple[list[str], list[str]]:
    """The tree as two lists: text nodes' text, and every other named node
    as role and name, whitespace collapsed, lower case, empty entries
    dropped."""
    texts, named = [], []
    for node in walk(nodes):
        if node.get("ignored"):
            continue
        role, name = _value(node, "role"), re.sub(r"\s+", " ", _value(node, "name")).strip().lower()
        if role in ("InlineTextBox", "RootWebArea") or not name:
            continue
        if role == "StaticText":
            texts.append(name)
        else:
            named.append(f"{role}: {name}")
    return texts, named


def first_difference(a: list[str], b: list[str]) -> str:
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return f"entry {i + 1}: {x!r} where the reference has {y!r}"
    longer, which = (a, "the page") if len(a) > len(b) else (b, "the reference")
    return f"{which} has {abs(len(a) - len(b))} more entries, from {longer[min(len(a), len(b))]!r}"


def page_errors(chrome: Chrome, page, origin: str) -> list[str]:
    """Requests to another origin, policy violations and script errors seen
    on this tab since the last call."""
    problems = []
    for event in chrome.take_events("Network.requestWillBeSent", page.session):
        url = event["request"]["url"]
        if not (url.startswith(origin + "/") or url.startswith(("data:", "about:", "blob:"))):
            problems.append(f"requested {url}, from another origin")
    for event in chrome.take_events("Log.entryAdded", page.session):
        text = event["entry"].get("text", "")
        if "Content Security Policy" in text or "Content-Security-Policy" in text:
            problems.append(f"broke its policy: {text[:200]}")
    for event in chrome.take_events("Runtime.exceptionThrown", page.session):
        details = event["exceptionDetails"]
        text = (details.get("exception") or {}).get("description") or details.get("text")
        problems.append(f"a script error: {str(text)[:200]}")
    return problems


def open_page(chrome: Chrome, origin: str, path: str, width: int, height: int, *, dark=False,
              reduced=False, scripts=True, settle=READ_AFTER, hash_=""):
    page = chrome.new_page(width, height, dark=dark, reduced=reduced, scripts=scripts)
    page.send("Page.addScriptToEvaluateOnNewDocument", {"source": INSTRUMENT})
    page.goto(f"{origin}/{path}{hash_}", settle=settle)
    return page


def wait_started(page) -> None:
    """Until the page's idle callbacks have all run, its start-up with them."""
    end = time.monotonic() + STARTED_WITHIN
    while time.monotonic() < end and not page.evaluate("!window.__pg || window.__pg.idle === 0"):
        time.sleep(0.05)


def lay_out_all(page) -> None:
    """Every section laid out, through the page's own stylesheet: the
    policy refuses an injected <style>, and must."""
    page.evaluate(f"""(() => {{
      const sheet = [...document.styleSheets].find((s) => s.href && s.href.endsWith('static/base.css'));
      if (!sheet) return false;  // the gallery page: no sections to lay out
      sheet.insertRule({json.dumps(LAYOUT_ALL)}, sheet.cssRules.length); return true; }})()""")


# The checks.

def check_tree(pages, origins, report, loads, quick) -> None:
    widths = WIDTHS[:1] if quick else WIDTHS
    for full in (True, False):
        mode = "full" if full else "default"
        with Chrome(accessibility=full) as chrome:
            for path in pages:
                for width, height in widths:
                    for dark in (False, True):
                        for scripts in (True, False):
                            cell = (f"{width}px {'dark' if dark else 'light'} scripts "
                                    f"{'on' if scripts else 'off'}, {mode} mode")
                            for _ in range(loads if full else 1):
                                lists = {}
                                for variant in ("built", "norule"):
                                    page = open_page(chrome, origins[variant], path, width, height,
                                                     dark=dark, scripts=scripts)
                                    if scripts:
                                        wait_started(page)
                                    lists[variant] = tree_lists(page.ax_tree())
                                    if variant == "built":
                                        navs = [n for n in walk(page.ax_tree()) if not n.get("ignored")
                                                and _value(n, "role") == "navigation"
                                                and _value(n, "name") == "Sections"]
                                        if len(navs) != 1:
                                            report.fail("tree", path, f"{cell}: {len(navs)} "
                                                        f"'Sections' navigations exposed; one is right")
                                        for problem in page_errors(chrome, page, origins[variant]):
                                            report.fail("requests", path, f"{cell}: {problem}")
                                    page.close()
                                report.ran("tree")
                                (text, named), (ref_text, ref_named) = lists["built"], lists["norule"]
                                if full:
                                    if text != ref_text:
                                        report.fail("tree", path, f"{cell}: text differs from the page "
                                                    f"without the rule, {first_difference(text, ref_text)}")
                                    if named != ref_named:
                                        report.fail("tree", path, f"{cell}: names differ from the page "
                                                    f"without the rule, {first_difference(named, ref_named)}")
                                else:
                                    extra = (set(text) - set(ref_text)) | (set(named) - set(ref_named))
                                    if extra:
                                        report.fail("tree", path, f"{cell}: holds what the page without "
                                                    f"the rule lacks: {sorted(extra)[:5]}")


KEYBOARD_STATE = """(() => {
  const a = document.activeElement;
  return { id: a ? a.id : '', tag: a ? a.tagName : '', text: a ? (a.textContent || '').trim().slice(0, 60) : '',
           hidden: !!(a && a.closest('[aria-hidden="true"]')),
           selfHidden: !!(a && a.getAttribute('aria-hidden') === 'true'),
           inFooter: !!(a && a.closest('footer')),
           close: a && a.dataset ? (a.dataset.depthClose || '') : '',
           panel: a && a.closest('[data-depth]') ? a.closest('[data-depth]').id : '' };
})()"""


def check_keyboard(pages, origin, report, quick) -> None:
    widths = WIDTHS[:1] if quick else WIDTHS
    with Chrome(accessibility=True) as chrome:
        for path in pages:
            for width, height in widths:
                cell = f"{width}px"
                page = open_page(chrome, origin, path, width, height, reduced=True)
                toggles = page.evaluate("[...document.querySelectorAll('[data-depth-toggle]')]"
                                        ".filter((t) => !t.hidden).map((t) => t.id)") or []
                # The walk: from the top to the footer, never resting in
                # aria-hidden content.
                stops, seen = 0, set()
                while stops < 400:
                    page.key("Tab")
                    stops += 1
                    state = page.evaluate(KEYBOARD_STATE)
                    if state["hidden"] or state["selfHidden"]:
                        report.fail("keyboard", path, f"{cell}: Tab stopped on <{state['tag']}> "
                                    f"'{state['text']}', inside aria-hidden content")
                    if state["inFooter"] or (state["id"], state["text"]) in seen and stops > 5:
                        break
                    seen.add((state["id"], state["text"]))
                for toggle in toggles:
                    report.ran("keyboard")
                    panel_id = toggle.replace("toggle-", "depth-", 1)
                    page.evaluate("document.activeElement && document.activeElement.blur(); "
                                  "window.scrollTo(0, 0); true")
                    reached = False
                    for _ in range(400):
                        page.key("Tab")
                        if page.evaluate(KEYBOARD_STATE)["id"] == toggle:
                            reached = True
                            break
                    if not reached:
                        report.fail("keyboard", path, f"{cell}: Tab never reached {toggle}")
                        continue
                    page.key("Enter")
                    chrome.drain(0.2)
                    state = page.evaluate(f"""(() => {{ const t = document.getElementById('{toggle}');
                      const p = document.getElementById('{panel_id}');
                      return {{ expanded: t.getAttribute('aria-expanded'), hidden: p.hidden,
                               ariaHidden: p.getAttribute('aria-hidden'),
                               heading: p.querySelector('h3').textContent.trim() }}; }})()""")
                    if state["expanded"] != "true" or state["hidden"] or state["ariaHidden"]:
                        report.fail("keyboard", path, f"{cell}: Enter on {toggle} did not open its panel")
                        continue
                    names = {_value(n, "name").strip() for n in page.ax_tree() if not n.get("ignored")}
                    if state["heading"] not in names:
                        report.fail("keyboard", path, f"{cell}: {panel_id}'s text did not enter the tree")
                    page.key("Tab")
                    if page.evaluate(KEYBOARD_STATE)["panel"] != panel_id:
                        report.fail("keyboard", path, f"{cell}: Tab after opening {toggle} did not "
                                    f"move into its panel")
                    for _ in range(20):
                        if page.evaluate(KEYBOARD_STATE)["close"]:
                            break
                        page.key("Tab")
                    page.key("Enter")
                    chrome.drain(0.2)
                    after = page.evaluate(f"""(() => {{ const p = document.getElementById('{panel_id}');
                      return {{ hidden: p.hidden, ariaHidden: p.getAttribute('aria-hidden'),
                               focus: document.activeElement.id }}; }})()""")
                    if not after["hidden"] or after["ariaHidden"] != "true":
                        report.fail("keyboard", path, f"{cell}: Close did not close {panel_id}, "
                                    f"or left it without aria-hidden")
                    if after["focus"] != toggle:
                        report.fail("keyboard", path, f"{cell}: after Close, focus is on "
                                    f"'{after['focus']}', not {toggle}")
                    page.key("Enter")
                    page.key("Enter")
                    again = page.evaluate(f"document.getElementById('{panel_id}').hidden")
                    if not again:
                        report.fail("keyboard", path, f"{cell}: {toggle} did not close its own panel")
                for problem in page_errors(chrome, page, origin):
                    report.fail("requests", path, f"{cell}: {problem}")
                page.close()


def snapshot_display(page) -> dict[int, str]:
    snap = page.send("DOMSnapshot.captureSnapshot", {"computedStyles": ["display"]})
    strings = snap["strings"]
    display = {}
    for doc in snap["documents"]:
        backend = doc["nodes"]["backendNodeId"]
        for node_index, styles in zip(doc["layout"]["nodeIndex"], doc["layout"]["styles"]):
            if styles:
                display[backend[node_index]] = strings[styles[0]]
    return display


def model_lines(nodes: list[dict], display: dict[int, str]) -> list[list[dict]]:
    """NVDA's lines, as modelled: the text pieces of the tree in order, with
    a line break at the start and the end of every non-ignored node whose
    element is not laid out inline. Ignored nodes, such as plain spans,
    never break a line, even when laid out as blocks; that is how two
    separate boxes come to be read as one word."""
    by_id = {n["nodeId"]: n for n in nodes}
    lines: list[list[dict]] = [[]]

    def visit(node):
        role = _value(node, "role")
        if role == "InlineTextBox":
            return
        breaks = (not node.get("ignored") and role != "StaticText" and
                  display.get(node.get("backendDOMNodeId"), "inline") not in ("inline", "contents"))
        if breaks and lines[-1]:
            lines.append([])
        if role == "StaticText" and not node.get("ignored"):
            lines[-1].append(node)
        for child in node.get("childIds", []):
            if child in by_id:
                visit(by_id[child])
        if breaks and lines[-1]:
            lines.append([])

    roots = [n for n in nodes if not n.get("parentId")]
    if roots:
        visit(roots[0])
    return lines


def check_joins(pages, origin, report, quick) -> None:
    widths = WIDTHS[1:] if quick else WIDTHS
    with Chrome(accessibility=True) as chrome:
        for path in pages:
            for width, height in widths:
                report.ran("joins")
                page = open_page(chrome, origin, path, width, height, reduced=True)
                lay_out_all(page)
                chrome.drain(0.5)
                page.send("DOM.getDocument", {"depth": -1})
                display = snapshot_display(page)
                lines = model_lines(page.ax_tree(), display)
                joins = []
                for line in lines:
                    for a, b in zip(line, line[1:]):
                        ta, tb = _value(a, "name"), _value(b, "name")
                        if not ta or not tb or ta[-1].isspace() or tb[0].isspace():
                            continue
                        if not (a.get("backendDOMNodeId") and b.get("backendDOMNodeId")):
                            continue
                        first = page.send("DOM.resolveNode", {"backendNodeId": a["backendDOMNodeId"]})
                        second = page.send("DOM.resolveNode", {"backendNodeId": b["backendDOMNodeId"]})
                        between = page.send("Runtime.callFunctionOn", {
                            "objectId": first["object"]["objectId"],
                            "functionDeclaration": "function (b) { const r = document.createRange();"
                                                   " r.setStartAfter(this); r.setEndBefore(b);"
                                                   " return r.toString(); }",
                            "arguments": [{"objectId": second["object"]["objectId"]}],
                            "returnByValue": True})["result"].get("value", "")
                        if re.search(r"\s", between or ""):
                            joins.append(f"{ta[-30:]!r} + {tb[:30]!r}")
                if joins:
                    report.fail("joins", path, f"{width}px: {len(joins)} join(s), such as "
                                + "; ".join(joins[:4]))
                page.close()


ANCHOR_STATE = """(() => {
  const t = document.getElementById(%s);
  if (!t) return null;
  const margin = parseFloat(getComputedStyle(t).scrollMarginTop) || 0;
  const atEnd = Math.ceil(scrollY + innerHeight) >= document.documentElement.scrollHeight - 1;
  return { top: t.getBoundingClientRect().top, margin, atEnd };
})()"""


def check_anchors(pages, origin, report, quick) -> None:
    widths = WIDTHS[:1] if quick else WIDTHS
    with Chrome() as chrome:
        for path in pages:
            for width, height in widths:
                for scripts in ((True,) if quick else (True, False)):
                    cell = f"{width}px scripts {'on' if scripts else 'off'}"
                    page = open_page(chrome, origin, path, width, height, reduced=True, scripts=scripts)
                    targets = page.send("Runtime.evaluate", {"expression":
                        "[...new Set([...document.querySelectorAll('a[href^=\"#\"]')]"
                        ".map((a) => a.getAttribute('href').slice(1)))]", "returnByValue": True})
                    targets = targets["result"]["value"]
                    page.close()
                    for target in targets:
                        report.ran("anchors")
                        # A fresh load with the address. A design's web fonts can
                        # arrive after the browser has jumped, and with
                        # font-display: swap they move the text above the target:
                        # the default design, with swap, missed by 16 to 40 px on
                        # about 1 load in 100 (2026-10-12 and 13); with optional,
                        # as it now ships, none in 272. So a miss is
                        # loaded once more, and fails only if it misses again; a
                        # single miss is reported as a note. Only a miss of a line
                        # or so, at most 32 px, gets the second load: without the
                        # :target rule in base.css, single misses of 100 to 860 px
                        # came right on a reload (2026-10-12), so a larger miss
                        # fails at once.
                        misses = []
                        for _ in range(2):
                            page = open_page(chrome, origin, path, width, height, reduced=True,
                                             scripts=scripts, hash_=f"#{target}", settle=0.8)
                            state = page.send("Runtime.evaluate", {"expression": ANCHOR_STATE % json.dumps(target),
                                                                   "returnByValue": True})["result"].get("value")
                            page.close()
                            if state is not None and (abs(state["top"] - state["margin"]) <= 3 or state["atEnd"]):
                                break
                            misses.append(f"{state and round(state['top'])} px")
                            if state is None or abs(state["top"] - state["margin"]) > 32:
                                misses.append("no second load, the miss being over 32 px")
                                break
                        if len(misses) == 2:
                            report.fail("anchors", path, f"{cell}: #{target} by its address lands at "
                                        f"{'; then '.join(misses)}; its margin is "
                                        f"{state and state['margin']} px")
                        elif misses:
                            report.notes.append(f"anchors: {path} {cell}: #{target} by its address landed "
                                                f"at {misses[0]} on one load and right on the next")
                    if scripts:
                        page = open_page(chrome, origin, path, width, height, reduced=True)
                        for target in targets:
                            page.evaluate("window.scrollTo(0, 0); true")
                            page.evaluate(f"(document.querySelector('a[href=\"#{target}\"]:not([hidden])') "
                                          f"|| document.querySelector('a[href=\"#{target}\"]')).click(); true")
                            chrome.drain(0.4)
                            state = page.evaluate(ANCHOR_STATE % json.dumps(target))
                            if state is None or not (abs(state["top"] - state["margin"]) <= 3 or state["atEnd"]):
                                report.fail("anchors", path, f"{cell}: #{target} by its link lands at "
                                            f"{state and round(state['top'])} px, its margin is "
                                            f"{state and state['margin']} px")
                        page.close()


def content_texts(nodes: list[dict]) -> list[str]:
    """The words of the page's main content and footer, as a reader meets
    them: StaticText under the main and contentinfo landmarks, leaving out
    buttons, whose words are the engine's, and list markers, which a design
    may draw or not."""
    by_id = {n["nodeId"]: n for n in nodes}
    texts = []

    def visit(node, inside):
        role = _value(node, "role")
        if role in ("button", "ListMarker"):
            return
        if not node.get("ignored"):
            if role in ("main", "contentinfo"):
                inside = True
            if inside and role == "StaticText":
                text = re.sub(r"\s+", " ", _value(node, "name")).strip().lower()
                if text:
                    texts.append(text)
        for child in node.get("childIds", []):
            if child in by_id:
                visit(by_id[child], inside)

    roots = [n for n in nodes if not n.get("parentId")]
    if roots:
        visit(roots[0], False)
    return texts


def check_words(demos, origins, report) -> None:
    """Scripts off, so every panel is open; every disclosure opened through
    the DOM; every section laid out (both variants lack the rule)."""
    with Chrome(accessibility=True) as chrome:
        for path in demos:
            for width, height in WIDTHS:
                report.ran("words")
                lists = {}
                for variant in ("norule", "bare"):
                    page = open_page(chrome, origins[variant], path, width, height, scripts=False)
                    root = page.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
                    for node_id in page.send("DOM.querySelectorAll", {"nodeId": root,
                                                                      "selector": "details"})["nodeIds"]:
                        page.send("DOM.setAttributeValue", {"nodeId": node_id, "name": "open", "value": ""})
                    chrome.drain(0.5)
                    lists[variant] = content_texts(page.ax_tree())
                    page.close()
                if lists["norule"] != lists["bare"]:
                    report.fail("words", path, f"{width}px: the design changes the page's words, "
                                f"{first_difference(lists['norule'], lists['bare'])} (the reference "
                                f"is the page with no design)")


def check_motion(pages, origin, report) -> None:
    with Chrome() as chrome:
        for path in pages:
            report.ran("motion")
            page = open_page(chrome, origin, path, 1366, 900, reduced=True, settle=3.0)
            state = page.evaluate("({ frames: window.__pg.frames, errors: window.__pg.errors,"
                                  " running: document.getAnimations().filter((a) => a.playState === 'running')"
                                  ".map((a) => a.animationName || a.constructor.name) })")
            if state["frames"]:
                report.fail("motion", path, f"{state['frames']} animation frame(s) requested under "
                            f"reduced motion")
            if state["running"]:
                report.fail("motion", path, f"animations running under reduced motion: "
                            f"{state['running'][:5]}")
            for problem in page_errors(chrome, page, origin) + [f"a script error: {e}" for e in state["errors"]]:
                report.fail("requests", path, f"reduced motion: {problem}")
            page.close()
            # And with motion allowed, the page runs without an error.
            page = open_page(chrome, origin, path, 1366, 900, settle=2.0)
            for problem in page_errors(chrome, page, origin):
                report.fail("requests", path, f"motion on: {problem}")
            page.close()


# The showcase's cards as laid out, relative to the list's top.
PACKING = """(() => {
  const list = document.querySelector('[data-pack]');
  if (!list) return null;
  const style = getComputedStyle(list);
  const top = list.getBoundingClientRect().top;
  return { display: style.display, em: parseFloat(style.fontSize), rowGap: parseFloat(style.rowGap) || 0,
    cards: [...list.children].map((li) => {
      const b = li.getBoundingClientRect();
      const img = li.querySelector('img');
      const i = img ? img.getBoundingClientRect() : { width: 0, height: 0 };
      return { name: (li.querySelector('h3') || li).textContent.trim().slice(0, 40),
               left: b.left, top: b.top - top, bottom: b.bottom - top, iw: i.width, ih: i.height,
               aw: img ? Number(img.getAttribute('width')) : 0, ah: img ? Number(img.getAttribute('height')) : 0 };
    }) };
})()"""
# Every showcase picture loaded and decoded, or false after 20 s: a picture
# that never decodes is reported as not loaded, never left to hang the run.
LOAD_ALL = """Promise.race([
  Promise.all([...document.querySelectorAll('[data-pack] img')].map((img) => {
    img.loading = 'eager';
    return img.decode().then(() => true, () => false);
  })).then((done) => done.every(Boolean)),
  new Promise((resolve) => setTimeout(() => resolve(false), 20000)),
])"""
FOCUSED_CARD = """(() => { const a = document.activeElement;
  const li = a && a.closest('[data-pack] > li');
  return { card: li ? [...li.parentNode.children].indexOf(li) : -1, footer: !!(a && a.closest('footer')) };
})()"""
PACKING_MODES = (("script", (), True), ("grid-lanes", ("--enable-experimental-web-platform-features",), True),
                 ("scripts off", (), False))
PACKING_WIDTHS = ((390, 844), (1366, 900))


def packing_problems(state: dict, packed: bool) -> list[str]:
    """What is wrong with the cards' places and pictures, as laid out."""
    problems = []
    cards = state["cards"]
    for card in cards:
        if not (card["aw"] and card["ah"]) or abs(card["ih"] - card["iw"] * card["ah"] / card["aw"]) > 1:
            problems.append(f"{card['name']}: its picture's box is {card['iw']:.0f}x{card['ih']:.0f}, not "
                            f"its reserved {card['aw']}x{card['ah']} shape")
        elif card["ih"] > card["iw"] * SHOWCASE_TALL + 1 or card["iw"] > card["ih"] * SHOWCASE_WIDE + 1:
            problems.append(f"{card['name']}: its picture is shown {card['iw']:.0f}x{card['ih']:.0f}, beyond "
                            f"the shape limits of {SHOWCASE_TALL} either way")
    for before, after in zip(cards, cards[1:]):
        if after["top"] < before["top"] - state["em"]:
            problems.append(f"{after['name']} sits {before['top'] - after['top']:.0f} px above "
                            f"{before['name']}, before it in folder order and in focus order")
    if packed:
        columns: dict[int, list[dict]] = {}
        for card in cards:
            columns.setdefault(round(card["left"]), []).append(card)
        for column in columns.values():
            column.sort(key=lambda c: c["top"])
            if column[0]["top"] > 1:
                problems.append(f"{column[0]['name']}: a gap of {column[0]['top']:.0f} px above it")
            for above, below in zip(column, column[1:]):
                gap = below["top"] - above["bottom"]
                if abs(gap - state["rowGap"]) > 1:
                    problems.append(f"{below['name']}: {gap:.0f} px below {above['name']}, not the "
                                    f"{state['rowGap']:.0f} px gap")
    return problems


def check_packing(origin, report) -> None:
    for mode, flags, scripts in PACKING_MODES:
        with Chrome(flags=flags) as chrome:
            for width, height in PACKING_WIDTHS:
                for dark in (False, True):
                    cell = f"{mode}, {width}px {'dark' if dark else 'light'}"
                    page = open_page(chrome, origin, "index.html", width, height, dark=dark, scripts=scripts)
                    before = page.evaluate(PACKING)
                    if before is None:
                        report.notes.append("packing: the gallery has no showcase cards to check")
                        page.close()
                        return
                    report.ran("packing")
                    if mode == "grid-lanes" and before["display"] != "grid-lanes":
                        report.fail("packing", "index.html", f"{cell}: Chrome laid the showcase out as "
                                    f"'{before['display']}', not grid-lanes")
                    # Every column runs without gaps, but where rows of several
                    # columns are left with neither grid-lanes nor the script.
                    packed = scripts or width == PACKING_WIDTHS[0][0]
                    for problem in packing_problems(before, packed):
                        report.fail("packing", "index.html", f"{cell}, before the pictures load: {problem}")
                    if not page.evaluate(LOAD_ALL, await_promise=True):
                        report.fail("packing", "index.html", f"{cell}: a showcase picture did not load")
                    chrome.drain(0.5)
                    after = page.evaluate(PACKING)
                    for problem in packing_problems(after, packed):
                        report.fail("packing", "index.html", f"{cell}, loaded: {problem}")
                    moved = [a["name"] for a, b in zip(after["cards"], before["cards"])
                             if abs(a["top"] - b["top"]) > 1 or abs(a["bottom"] - b["bottom"]) > 1
                             or abs(a["left"] - b["left"]) > 1]
                    if moved:
                        report.fail("packing", "index.html", f"{cell}: cards moved as their pictures "
                                    f"loaded: {', '.join(moved)}")
                    # Tab, from the top, meets the cards in folder order.
                    page.evaluate("document.activeElement && document.activeElement.blur(); "
                                  "window.scrollTo(0, 0); true")
                    met: list[int] = []
                    for _ in range(600):
                        page.key("Tab")
                        state = page.evaluate(FOCUSED_CARD)
                        if state["footer"]:
                            break
                        if state["card"] >= 0 and (not met or met[-1] != state["card"]):
                            met.append(state["card"])
                    if met != list(range(len(after["cards"]))):
                        report.fail("packing", "index.html", f"{cell}: Tab met the cards in the order "
                                    f"{[i + 1 for i in met]}, not 1 to {len(after['cards'])}")
                    for problem in page_errors(chrome, page, origin):
                        report.fail("requests", "index.html", f"{cell}: {problem}")
                    page.close()


AXE_RUN = """axe.run(document, { resultTypes: ['violations'] }).then((r) =>
  r.violations.map((v) => v.id + ' (' + v.nodes.length + '): ' + v.nodes[0].target.join(' ')))"""

OVERLAY_STATE = """(() => { const d = document.querySelector('[data-view]'); const a = document.activeElement;
  const links = [...document.querySelectorAll('.g-site .g-frame')];
  const p = d ? d.querySelector('img') : null; const r = p ? p.getBoundingClientRect() : null;
  const c = d ? d.querySelector('[data-view-close]') : null; const cr = c ? c.getBoundingClientRect() : null;
  return { open: !!(d && d.open), modal: !!(d && d.matches(':modal')), inside: !!(d && d.contains(a)),
    card: links.indexOf(a), focus: a ? a.tagName + (a.className ? '.' + a.className : '') : 'nothing',
    href: links.length ? links[0].getAttribute('href') : null, path: location.pathname,
    close: c && c.offsetParent !== null ? { w: cr.width, h: cr.height } : null,
    picture: p ? { loaded: p.complete && p.naturalWidth > 0, src: p.getAttribute('src'), nw: p.naturalWidth,
                   nh: p.naturalHeight, w: r.width, h: r.height, left: r.left, top: r.top, right: r.right,
                   bottom: r.bottom } : null,
    vw: innerWidth, vh: innerHeight }; })()"""
PICTURE_LOADED = """(() => { const p = document.querySelector('[data-view] img');
  return p ? p.decode().then(() => true, () => false) : false; })()"""


def overlay_problems(state: dict) -> list[str]:
    """What is wrong with the overlay as it stands open."""
    problems = []
    if not state["open"] or not state["modal"]:
        return [f"Enter on the card did not open the overlay as a modal dialog "
                f"(open: {state['open']}, modal: {state['modal']}); the page is at {state['path']}"]
    if not state["inside"]:
        problems.append(f"focus stayed on {state['focus']}, outside the overlay")
    if not state["close"] or state["close"]["w"] < 24 or state["close"]["h"] < 24:
        problems.append("the overlay has no visible Close button of at least 24 px")
    picture = state["picture"]
    if not picture or not picture["loaded"]:
        problems.append("the overlay's picture did not load")
    elif picture["src"] != state["href"]:
        problems.append(f"the overlay shows {picture['src']}, not the card's own {state['href']}")
    else:
        if (picture["left"] < -1 or picture["top"] < -1 or picture["right"] > state["vw"] + 1
                or picture["bottom"] > state["vh"] + 1):
            problems.append(f"the picture is not whole within the window: {picture['left']:.0f}, "
                            f"{picture['top']:.0f} to {picture['right']:.0f}, {picture['bottom']:.0f} in "
                            f"{state['vw']}x{state['vh']}")
        shape, natural = picture["w"] / picture["h"], picture["nw"] / picture["nh"]
        if abs(shape - natural) > natural * 0.01:
            problems.append(f"the picture is shown at {picture['w']:.0f}x{picture['h']:.0f}, not in its own "
                            f"proportions, {picture['nw']}x{picture['nh']}")
        if picture["w"] > picture["nw"] + 1:
            problems.append(f"the picture is enlarged past its own {picture['nw']} px")
    return problems


def check_overlay(origin, report, axe_source: str | None) -> None:
    def tab_to_card(page) -> bool:
        page.evaluate("document.activeElement && document.activeElement.blur(); window.scrollTo(0, 0); true")
        for _ in range(600):
            page.key("Tab")
            if page.evaluate(OVERLAY_STATE)["card"] == 0:
                return True
        return False

    def named(page, role: str, name: str | None = None) -> bool:
        return any(_value(n, "role") == role and (_value(n, "name").strip() if name is None else
                                                  _value(n, "name").strip() == name)
                   for n in page.ax_tree() if not n.get("ignored"))

    with Chrome(accessibility=True) as chrome:
        for width, height in PACKING_WIDTHS:
            for dark in (False, True):
                cell = f"{width}px {'dark' if dark else 'light'}"
                page = open_page(chrome, origin, "index.html", width, height, dark=dark, reduced=True)
                if page.evaluate(OVERLAY_STATE)["href"] is None:
                    report.notes.append("overlay: the gallery has no showcase cards to check")
                    page.close()
                    return
                report.ran("overlay")
                if named(page, "dialog") or named(page, "button", "Close"):
                    report.fail("overlay", "index.html", f"{cell}: the closed overlay is in the tree at load")
                if axe_source:
                    page.evaluate(axe_source + "\n;true")
                    for violation in page.evaluate(AXE_RUN, await_promise=True) or []:
                        report.fail("axe", "index.html", f"{cell}, the overlay closed: {violation}")
                if not tab_to_card(page):
                    report.fail("overlay", "index.html", f"{cell}: Tab never reached the first card's picture")
                    page.close()
                    continue
                # Escape, the Close button and a click outside the picture,
                # each from the overlay opened by Enter on the card.
                for way in ("Escape", "the Close button", "a click outside the picture"):
                    page.key("Enter")
                    chrome.drain(0.3)
                    page.evaluate(PICTURE_LOADED, await_promise=True)
                    state = page.evaluate(OVERLAY_STATE)
                    problems = overlay_problems(state)
                    for problem in problems:
                        report.fail("overlay", "index.html", f"{cell}: {problem}")
                    if not state["open"]:
                        break
                    if way == "Escape":
                        if not named(page, "button", "Close"):
                            report.fail("overlay", "index.html", f"{cell}: no button named 'Close' in the tree")
                        if not named(page, "dialog"):
                            report.fail("overlay", "index.html", f"{cell}: the overlay is not a named dialog "
                                        f"in the tree")
                        if axe_source:
                            for violation in page.evaluate(AXE_RUN, await_promise=True) or []:
                                report.fail("axe", "index.html", f"{cell}, the overlay open: {violation}")
                        page.key("Escape")
                    elif way == "the Close button":
                        page.evaluate("(() => { const c = document.querySelector('[data-view-close]');"
                                      " if (c) c.focus(); return true; })()")
                        page.key("Enter")
                    else:
                        for kind in ("mousePressed", "mouseReleased"):
                            page.send("Input.dispatchMouseEvent", {"type": kind, "x": 4, "y": 4,
                                                                  "button": "left", "clickCount": 1})
                    chrome.drain(0.3)
                    after = page.evaluate(OVERLAY_STATE)
                    if after["open"]:
                        report.fail("overlay", "index.html", f"{cell}: {way} did not close the overlay")
                        break
                    if after["card"] != 0:
                        report.fail("overlay", "index.html", f"{cell}: after {way}, focus is on "
                                    f"{after['focus']}, not the card's link")
                        break
                for problem in page_errors(chrome, page, origin):
                    report.fail("requests", "index.html", f"{cell}: {problem}")
                page.close()
                # Scripts off: the card is the plain link it always was.
                page = open_page(chrome, origin, "index.html", width, height, dark=dark, scripts=False)
                state = page.evaluate(OVERLAY_STATE)
                if state["open"]:
                    report.fail("overlay", "index.html", f"{cell}, scripts off: an overlay is open")
                elif tab_to_card(page):
                    page.key("Enter")
                    chrome.drain(1.0)
                    landed = page.evaluate("location.pathname")
                    if not landed.endswith(state["href"]):
                        report.fail("overlay", "index.html", f"{cell}, scripts off: Enter on the card led to "
                                    f"{landed}, not the picture {state['href']}")
                else:
                    report.fail("overlay", "index.html", f"{cell}, scripts off: Tab never reached the first "
                                f"card's picture")
                page.close()


def check_axe(pages, origin, report, axe_source: str) -> None:
    with Chrome() as chrome:
        for path in pages:
            for width, height in WIDTHS:
                for theme in ("light", "device dark", "switched dark"):
                    for opened in (False, True):
                        cell = f"{width}px {theme}, panels {'open' if opened else 'closed'}"
                        report.ran("axe")
                        page = open_page(chrome, origin, path, width, height, dark=theme == "device dark",
                                         reduced=True)
                        if theme == "switched dark":
                            page.evaluate("(() => { const s = [...document.querySelectorAll('[data-theme-switch]')]"
                                          ".find((b) => b.offsetParent); if (s) s.click(); return !!s; })()")
                            chrome.drain(3.0)
                        lay_out_all(page)
                        if opened:
                            page.evaluate("document.querySelectorAll('details').forEach((d) => { d.open = true; });"
                                          "document.querySelectorAll('[data-depth]').forEach((p) => {"
                                          " p.hidden = false; p.removeAttribute('aria-hidden'); }); true")
                        chrome.drain(0.5)
                        page.evaluate(axe_source + "\n;true")
                        violations = page.evaluate(AXE_RUN, await_promise=True)
                        for violation in violations or []:
                            report.fail("axe", path, f"{cell}: {violation}")
                        page.close()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="The standing checks that need a browser.")
    parser.add_argument("folder", nargs="?", default="_site")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--axe", type=Path, metavar="FILE", help="axe.min.js, to run axe-core")
    parser.add_argument("--only", help="comma-separated checks to run")
    parser.add_argument("--designs", metavar="NAME[,NAME]",
                        help="in a gallery, check only these designs' demos; empty for none")
    parser.add_argument("--skip-gallery-page", action="store_true",
                        help="in a gallery, leave out the gallery page's own checks")
    parser.add_argument("--loads", type=int, default=2, help="loads per cell in the tree check")
    # Page text can hold characters the console cannot write, as on Windows;
    # write them escaped rather than stop the report.
    sys.stdout.reconfigure(errors="backslashreplace")
    args = parser.parse_args(argv)
    root = Path(args.folder).resolve()
    if not (root / "index.html").is_file():
        print(f"no built page in {root}; run python build.py first", file=sys.stderr)
        return 2
    demos = sorted(p.relative_to(root).as_posix() for p in (root / "designs").glob("*/index.html"))
    gallery = bool(demos)
    report = Report()
    page = gallery
    # A run narrowed to the designs a change touches (tools/ci.py, ADR-0019).
    # A name the gallery lacks is refused, so a typo cannot check nothing.
    if args.designs is not None or args.skip_gallery_page:
        if not gallery:
            print("--designs and --skip-gallery-page apply to a built gallery only", file=sys.stderr)
            return 2
        names = [n for n in args.designs.split(",") if n] if args.designs is not None else None
        if names is not None:
            known = {d.split("/")[1] for d in demos}
            missing = sorted(set(names) - known)
            if missing:
                print(f"--designs names no design in this gallery: {', '.join(missing)}", file=sys.stderr)
                return 2
            left = sorted(known - set(names))
            demos = [d for d in demos if d.split("/")[1] in names]
            if left:
                report.notes.append(f"designs not checked, as asked: {', '.join(left)}")
        if args.skip_gallery_page:
            page = False
            report.notes.append("the gallery page not checked, as asked")
    sites = demos if gallery else ["index.html"]
    pages = sites + (["index.html"] if page else [])
    chosen = set(args.only.split(",")) if args.only else {
        "tree", "keyboard", "joins", "anchors", "words", "motion", "packing", "overlay", "axe"}
    loads = 1 if args.quick else args.loads
    started = time.monotonic()
    work = Path(tempfile.mkdtemp(prefix="pg-check-"))
    try:
        variants = make_variants(root, work)
        servers = {name: Server(folder) for name, folder in variants.items()}
        origins = {name: server.origin for name, server in servers.items()}
        try:
            with Chrome() as probe:
                print(f"{probe.version()}; pages: {', '.join(sites) or 'no design'}"
                      f"{' and the gallery page' if page else ''}")
            if "tree" in chosen:
                check_tree(sites, origins, report, loads, args.quick)
            if "keyboard" in chosen:
                check_keyboard(pages, origins["built"], report, args.quick)
            if "joins" in chosen:
                check_joins(sites, origins["built"], report, args.quick)
            if "anchors" in chosen:
                check_anchors(sites, origins["built"], report, args.quick)
            if "words" in chosen and gallery:
                check_words(demos, origins, report)
            if "motion" in chosen:
                check_motion(pages, origins["built"], report)
            if "packing" in chosen and page:
                check_packing(origins["built"], report)
            if "overlay" in chosen and page:
                check_overlay(origins["built"], report,
                              args.axe.read_text(encoding="utf-8") if args.axe and "axe" in chosen else None)
            if "axe" in chosen:
                if args.axe:
                    check_axe(pages, origins["built"], report,
                              args.axe.read_text(encoding="utf-8"))
                else:
                    report.notes.append("axe: not run; pass --axe FILE, axe.min.js fetched as "
                                        "docs/reference/commands.md says (ADR-0011)")
        finally:
            for server in servers.values():
                server.__exit__()
    except MissingTool as error:
        print(f"missing tool: {error}", file=sys.stderr)
        return 1
    except CDPError as error:
        print(f"the browser failed: {error}", file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
    for check, n in report.counts.items():
        print(f"  {check}: {n} run(s)")
    for note in report.notes:
        print(f"  NOTE {note}")
    for failure in report.failures:
        print(f"  FAIL {failure}")
    seconds = round(time.monotonic() - started)
    print(f"\n{'PASS' if not report.failures else 'FAIL'}: {len(report.failures)} failure(s) "
          f"in {seconds} s{' (quick: not the standing checks)' if args.quick else ''}")
    return 1 if report.failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
