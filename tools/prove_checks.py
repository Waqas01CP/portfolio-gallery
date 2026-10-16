"""Prove the checks can fail: run each one on the case built to defeat it.

  python tools/prove_checks.py            the file checks, about a minute
  python tools/prove_checks.py --browser  also the browser checks, longer
  python tools/prove_checks.py --browser --axe FILE
                                          also axe, with axe.min.js

A check that cannot fail is worse than no check. For each case this copies
the repository's tracked files to a temporary folder, plants the defect,
runs the check there, and passes only if the check exits non-zero and
names what failed. Each case also has its control: the same check on the
unchanged copy passes. Nothing in this repository is touched.

Exit 0 when every check failed on its defeat case and passed its control;
1 when any check let its defeat through (an unproven check) or failed its
control; the report names each. Standard library only; needs the venv.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True)
    names = [p for p in out.stdout.decode().split("\0") if p]
    # Files written for this session but not yet staged are part of the
    # working tree being proven; include every file git does not ignore.
    other = subprocess.run(["git", "ls-files", "-z", "--others", "--exclude-standard"],
                           cwd=ROOT, capture_output=True, check=True)
    return sorted(set(names) | {p for p in other.stdout.decode().split("\0") if p})


def fresh_copy(work: Path) -> Path:
    copy = work / "repo"
    if copy.exists():
        shutil.rmtree(copy)
    for name in tracked():
        source = ROOT / name
        if source.is_file():
            target = copy / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    return copy


def run(copy: Path, *args) -> tuple[int, str]:
    result = subprocess.run([PY, *map(str, args)], cwd=copy, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"prove_checks: {path.name} no longer holds {old[:60]!r}; update the case")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def new_design(copy: Path, name: str, css: str = "body { color: #111; }\n", extra: dict | None = None) -> Path:
    folder = copy / "designs" / name
    folder.mkdir(parents=True)
    (folder / "design.css").write_text(css, encoding="utf-8")
    meta = {"name": "Test", "author": "Tester", "author_url": "https://example.com/",
            "description": "A test design.", "assets": [], **(extra or {})}
    (folder / "design.json").write_text(json.dumps(meta), encoding="utf-8")
    return folder


def build_site(copy: Path, *mode: str) -> Path:
    out = copy / "_out"
    code, text = run(copy, "build.py", "--as-of", "2026-10", *mode, "--out", out)
    if code:
        raise SystemExit(f"prove_checks: the unchanged copy does not build:\n{text}")
    return out


# Each case: (label, plant(copy) -> command args, expected text in output).

def file_cases():
    def design(css=None, files=(), meta=None, drop=None):
        def plant(copy):
            folder = new_design(copy, "probe", css or "body { color: #111; }\n", meta)
            for rel, data in files:
                (folder / rel).parent.mkdir(parents=True, exist_ok=True)
                (folder / rel).write_bytes(data)
            if drop:
                data = json.loads((folder / "design.json").read_text())
                data.pop(drop)
                (folder / "design.json").write_text(json.dumps(data))
            return ["tools/check_design.py", "probe"]
        return plant

    yield "design: a .js file", design(files=[("script.js", b"alert(1)")]), "only design.css and design.json"
    yield "design: a .js file in fonts/", design(files=[("fonts/x.js", b"alert(1)")]), "not an allowed file"
    yield "design: an .svg image", design(files=[("img/logo.svg", b"<svg/>")]), "not an allowed file"
    yield "design: @import", design(css="@import url(fonts/a.css);\n"), "@import is not allowed"
    yield "design: an escaped @import", design(css="@\\69mport 'x.css';\n"), "@import is not allowed"
    yield ("design: url() to another origin", design(css="body { background: url(https://example.org/x.png); }\n"),
           "must point at a file")
    yield ("design: url() climbing out", design(css="body { background: url(../plain/design.css); }\n"),
           "must point at a file")
    yield ("design: an escaped url()", design(css="body { background: u\\72l(https://example.org/x.png); }\n"),
           "must point at a file")
    yield ("design: image-set()", design(css="body { background: image-set('https://example.org/x.png' 1x); }\n"),
           "image-set() is not allowed")
    yield "design: over the size limit", design(css="/*" + "x" * 103_000 + "*/\n"), "over the 100 KB limit"
    yield "design: design.json without author_url", design(drop="author_url"), "author_url"
    yield ("design: a renamed file", design(files=[("img/photo.png", b"<svg onload=alert(1)>")],
                                            meta={"assets": [{"file": "img/photo.png", "licence": "CC0-1.0",
                                                              "source": "own work"}]}),
           "its content is not a .png file")
    yield ("design: a font with no licence", design(files=[("fonts/a.woff2", b"wOF2" + b"\0" * 20)]),
           "must be listed in assets")
    yield ("design: an unclosed comment", design(css="body { color: red; } /* never closed\n"),
           "cannot be read safely")

    def scope(lines):
        def plant(copy):
            (copy / "_scope.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
            return ["tools/scope_check.py", "--files", "_scope.tsv"]
        return plant

    yield "scope: a file in tools/", scope(["modified\ttools/check_design.py"]), "outside designs/"
    yield ("scope: a workflow", scope(["added\tdesigns/a/design.css", "modified\t.github/workflows/scope.yml"]),
           "outside designs/")
    yield "scope: two designs", scope(["added\tdesigns/a/design.css", "added\tdesigns/b/design.css"]), "one pull request carries one design"
    yield "scope: a .js file in a design", scope(["added\tdesigns/a/design.js"]), "not a file a design may hold"
    yield "scope: a maintained design", scope(["modified\tdesigns/default/design.css"]), "maintained by the project"
    yield ("scope: a rename out of a design", scope(["renamed\ttools/x.py\tdesigns/a/design.css"]),
           "outside designs/")

    def built(old, new, page="index.html"):
        def plant(copy):
            out = build_site(copy)
            edit(out / page, old, new)
            return ["tools/check_built.py", out]
        return plant

    yield ("built: a request to another origin", built("</main>", '<img src="https://example.org/x.png" alt=""></main>'),
           "loads from another origin")
    yield "built: a root-relative path", built('src="static/site.js"', 'src="/static/site.js"'), "root-relative"
    yield "built: a wrongly cased path", built('src="static/site.js"', 'src="Static/site.js"'), "GitHub Pages matches names"
    yield ("built: hidden without aria-hidden", built('<p class="tl-empty" data-tl-empty hidden aria-hidden="true">',
                                                      '<p class="tl-empty" data-tl-empty hidden>'),
           "not aria-hidden")
    yield "built: an inline script", built("</main>", "<script>alert(1)</script></main>"), "inline <script>"
    yield "built: no policy tag", built('<meta http-equiv="Content-Security-Policy"', '<meta name="x"'), "no Content-Security-Policy"
    yield "built: a link to a missing id", built('href="#main"', 'href="#nowhere"'), "names no id"

    def no_previews(copy):
        return ["tools/check_built.py", build_site(copy, "--gallery"), "--previews"]

    yield "built: a gallery without its previews, with --previews", no_previews, "no preview.webp"

    def trace(old, new, where="page"):
        def plant(copy):
            out = build_site(copy)
            if where == "page":
                edit(out / "index.html", old, new)
            else:
                edit(copy / "content" / "items.json", old, new)
                out = build_site(copy)
            return ["tools/check_content.py", "--page", out / "index.html"]
        return plant

    yield "trace: a number changed on the page", trace("212 automated tests", "213 automated tests"), "NOT TRACED"
    yield ("trace: a source naming no entry", trace('"source": "Projects / Reading List: a static reading log"',
                                                    '"source": "Projects / Reading Log"', where="items"),
           "NO SUCH ENTRY")
    yield ("trace: a CV line missing from the page", trace('"date_style": "full",\n    "source": "Projects / Reading List',
                                                           '"source": "Projects / Reading List', where="items"),
           "MISSING: Jun 2025 to Jul 2025")

    def assemble(extra=None, big=False):
        def plant(copy):
            site = build_site(copy, "--gallery")
            shots = copy / "_shots"
            for name in ("default", "plain"):
                (shots / name).mkdir(parents=True)
                data = b"RIFF\0\0\0\0WEBPVP8 " + (b"\0" * (310_000 if big and name == "plain" else 64))
                (shots / name / "preview.webp").write_bytes(data)
            if extra:
                (shots / extra[0]).parent.mkdir(parents=True, exist_ok=True)
                (shots / extra[0]).write_bytes(extra[1])
            return ["tools/ci.py", "assemble", "--site", site, "--shots", shots]
        return plant

    yield "assemble: a script among the previews", assemble(("default/site.js", b"alert(1)")), "not <name>/preview.webp"
    yield "assemble: a preview over 300 KB", assemble(big=True), "over 300 KB"
    yield ("assemble: a fake image", assemble(("plain/preview.webp", b"<svg onload=alert(1)>")),
           "not a WebP image")

    def build_case(old, new):
        def plant(copy):
            edit(copy / "content" / "items.json", old, new)
            return ["build.py", "--as-of", "2026-10", "--out", copy / "_out"]
        return plant

    yield ("build: layer1 not a cut", build_case('"layer1": "Wrote 212 automated tests',
                                                 '"layer1": "Wrote 213 automated tests'), "not a cut")
    yield ("build: tier out of order", build_case('"tier": 3,', '"tier": 1,'), "tier must not decrease")
    yield ("build: no proof route", build_case('"no_proof": "Checked with the university on request."', '"grade2": "x"'),
           "no proof link")

    def twice(copy):
        edit(copy / "build.py", '        (staging / ".nojekyll").write_text("", encoding="utf-8")',
             '        (staging / ".nojekyll").write_text(str(__import__("time").time_ns()), encoding="utf-8")')
        return ["tools/ci.py", "checks", "--quick"]

    yield "build twice: output that depends on the clock", twice, "two builds of the site differ"


def axe_file(argv: list[str]) -> Path | None:
    if "--axe" not in argv:
        return None
    at = argv.index("--axe") + 1
    if at >= len(argv) or not Path(argv[at]).is_file():
        raise SystemExit("prove_checks: --axe needs the path of axe.min.js")
    return Path(argv[at]).resolve()


def browser_cases(axe: Path | None):
    def gallery(plant_fn, only):
        def plant(copy):
            plant_fn(copy)
            out = build_site(copy, "--gallery")
            return ["tools/check_browser.py", out, "--only", only, "--quick"]
        return plant

    # A panel hidden by the script without aria-hidden was not exposed at
    # load on this engine and sample page in Chrome 154 (2026-10-12), though
    # it was on the operator's site at 0403c68; markup hidden without
    # aria-hidden in a section that skips its layout is.
    yield ("tree: markup hidden without aria-hidden in a skipped section", gallery(lambda c: edit(
        c / "src/templates/timeline.html.j2", '<p class="tl-empty" data-tl-empty hidden aria-hidden="true">',
        '<p class="tl-empty" data-tl-empty hidden>'), "tree"), "differs from the page without the rule")
    yield ("words: a design adding text", gallery(lambda c: edit(
        c / "designs/plain/design.css", "/* Footer. */", '.foot-name::after { content: " for hire"; }\n/* Footer. */'),
        "words"), "changes the page's words")
    yield ("words: a design hiding a section", gallery(lambda c: edit(
        c / "designs/plain/design.css", "/* Footer. */", "#skills { display: none; }\n/* Footer. */"), "words"),
           "changes the page's words")
    yield ("requests: a design loading from another origin", gallery(lambda c: edit(
        c / "src/templates/footer.html.j2", "</footer>", '<img src="https://example.org/x.png" alt=""></footer>'),
        "motion"), "from another origin")
    yield ("motion: an animation forced past reduced motion", gallery(lambda c: edit(
        c / "designs/plain/design.css", "/* Footer. */",
        "@keyframes spin { to { transform: rotate(1turn); } }\n.foot-name { animation: spin 2s infinite !important; }\n/* Footer. */"),
        "motion"), "animations running under reduced motion")
    yield ("keyboard: Close not returning focus", gallery(lambda c: edit(
        c / "src/static/site.js", "toggle.focus({ preventScroll: true });", ""), "keyboard"),
           "after Close, focus is on")
    # Not quick: the misplacement shows with scripts off, which quick skips.
    def anchors_full(copy):
        edit(copy / "src/static/base.css", "html:has(:target) .page > .sec { content-visibility: visible; }", "")
        return ["tools/check_browser.py", build_site(copy, "--gallery"), "--only", "anchors"]

    yield "anchors: base.css without its :target rule", anchors_full, "[anchors]"
    yield ("joins: the hidden spaces removed", gallery(lambda c: edit(
        c / "src/templates/macros.html.j2", '{% macro sp() %}<span class="vh"> </span>{% endmacro %}',
        "{% macro sp() %}{% endmacro %}"), "joins"), "join(s)")

    if axe:
        def faint(copy):
            edit(copy / "designs/plain/design.css", "/* Footer. */", ".lede { color: #eee; }\n/* Footer. */")
            edit(copy / "src/templates/footer.html.j2", "</footer>",
                 '<img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" width="10" height="10"></footer>')
            return ["tools/check_browser.py", build_site(copy, "--gallery"), "--only", "axe", "--axe", axe]

        yield "axe: faint text and an image without alt", faint, ("color-contrast", "image-alt")


def main(argv: list[str]) -> int:
    # Page text can hold characters the console cannot write, as on Windows;
    # write them escaped rather than stop the report.
    sys.stdout.reconfigure(errors="backslashreplace")
    cases = list(file_cases())
    axe = axe_file(argv)
    if "--browser" in argv:
        cases += list(browser_cases(axe))
    work = Path(tempfile.mkdtemp(prefix="pg-prove-"))
    unproven, ran = [], 0
    try:
        # Controls: every check passes on the unchanged copy.
        copy = fresh_copy(work)
        out = build_site(copy)
        gallery_out = copy / "_gallery"
        run(copy, "build.py", "--as-of", "2026-10", "--gallery", "--out", gallery_out)
        (copy / "_scope.tsv").write_text("added\tdesigns/probe/design.css\nadded\tdesigns/probe/design.json\n")
        shots = copy / "_shots"
        for name in ("default", "plain"):
            (shots / name).mkdir(parents=True)
            (shots / name / "preview.webp").write_bytes(b"RIFF\0\0\0\0WEBPVP8 " + b"\0" * 64)
        controls = [("design", ["tools/check_design.py"]),
                    ("assemble", ["tools/ci.py", "assemble", "--site", gallery_out, "--shots", shots]),
                    ("scope", ["tools/scope_check.py", "--files", "_scope.tsv"]),
                    ("built", ["tools/check_built.py", out]),
                    ("built, gallery", ["tools/check_built.py", gallery_out]),
                    ("trace", ["tools/check_content.py", "--page", out / "index.html"])]
        if "--browser" in argv:
            controls.append(("browser", ["tools/check_browser.py", gallery_out, "--quick"]))
            if axe:
                controls.append(("axe", ["tools/check_browser.py", gallery_out, "--only", "axe", "--axe", axe]))
        for label, args in controls:
            code, text = run(copy, *args)
            print(f"{'ok  ' if code == 0 else 'FAIL'} control: {label} passes on the unchanged copy")
            if code:
                unproven.append(f"control {label} failed:\n{text[-1500:]}")
        for label, plant, expected in cases:
            copy = fresh_copy(work)
            args = plant(copy)
            code, text = run(copy, *args)
            ran += 1
            # A case may name several texts; each must be in the output.
            wanted = expected if isinstance(expected, tuple) else (expected,)
            caught = code != 0 and all(piece in text for piece in wanted)
            print(f"{'ok  ' if caught else 'FAIL'} {label}: exit {code}"
                  f"{'' if caught else f', expected {wanted!r} in the output'}")
            if not caught:
                unproven.append(f"{label}: exit {code}\n{text[-1200:]}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"\n{ran} defeat case(s); {len(unproven)} unproven")
    for item in unproven:
        print(f"\nUNPROVEN {item}")
    return 1 if unproven else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
