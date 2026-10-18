"""Check design folders against the design format (ADR-0006).

  python tools/check_design.py            every folder in designs/
  python tools/check_design.py NAME ...   the named designs only

A design is CSS on the engine's fixed HTML, and nothing that runs. Its
folder may hold exactly:

  design.css            the stylesheet
  design.json           its name, author, author URL, description,
                        whether it offers a dark theme, the fonts to
                        preload, and each asset's licence
  fonts/*.woff2         fonts, each listed in design.json with its licence
  fonts/*.txt           each font's licence text
  img/*.png, *.webp, *.jpg, *.jpeg
                        images, each listed in design.json with its licence

No SVG (it can carry script), no HTML, no JavaScript, no templates, no
subfolders beyond fonts/ and img/, no symbolic links, and no preview: the
deploy workflow takes the gallery's previews itself. Each file's first
bytes must match its type, so a renamed file is caught.

The stylesheet is read token by token, after CSS escapes are resolved, so
`@\\69mport` is read as `@import`. It may not use @import; every url() must
point at a file in the design's own fonts/ or img/; image-set(), src(),
element() and expression(), which load or run things, are refused, and so
are the old script hooks `behavior` and `-moz-binding`. An unclosed
comment or string is refused rather than guessed at, because two parsers
that disagree about where a string ends are how filters are got around.

Limits, set from the default design's own files with room to spare: the
stylesheet at most 100 KB, each font at most 200 KB, each image at most
300 KB, each licence text at most 16 KB, the folder at most 600 KB and 40
files.

Exit 0 when every design passes; 1 when one fails, each problem printed
with its design and file; 2 on a usage error. Standard library only.
"""

from __future__ import annotations

import json
import re
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGNS = ROOT / "designs"

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FILE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,80}$")
KB = 1024
LIMITS = {".css": 100 * KB, ".json": 8 * KB, ".woff2": 200 * KB, ".txt": 16 * KB,
          ".png": 300 * KB, ".webp": 300 * KB, ".jpg": 300 * KB, ".jpeg": 300 * KB}
FOLDER_LIMIT = 600 * KB
FILE_COUNT_LIMIT = 40
ROOT_FILES = {"design.css", "design.json"}
SUBFOLDERS = {"fonts": {".woff2", ".txt"}, "img": {".png", ".webp", ".jpg", ".jpeg"}}
MAGIC = {
    ".woff2": lambda b: b[:4] == b"wOF2",
    ".png": lambda b: b[:8] == b"\x89PNG\r\n\x1a\n",
    ".webp": lambda b: b[:4] == b"RIFF" and b[8:12] == b"WEBP",
    ".jpg": lambda b: b[:3] == b"\xff\xd8\xff",
    ".jpeg": lambda b: b[:3] == b"\xff\xd8\xff",
}
LICENCES = {"OFL-1.1", "Apache-2.0", "MIT", "CC0-1.0"}
LICENCE_TEXT = {"OFL-1.1": ("SIL Open Font License", "Version 1.1"),
                "Apache-2.0": ("Apache License", "Version 2.0"),
                "MIT": ("Permission is hereby granted",)}
META_FIELDS = {"name", "author", "author_url", "description", "dark", "preload", "assets"}
ASSET_FIELDS = {"file", "licence", "licence_file", "source"}

REFUSED_FUNCTIONS = {"image-set", "-webkit-image-set", "src", "element", "-moz-element",
                     "expression"}
REFUSED_IDENTS = {"behavior", "-moz-binding"}
URL_TARGET_RE = re.compile(r"^(fonts|img)/[A-Za-z0-9][A-Za-z0-9._-]{0,80}$")


class CSSError(Exception):
    """CSS this check will not guess at."""


# A CSS tokenizer, enough of CSS Syntax Level 3 to find at-rules, function
# names, url() targets and identifiers with every escape resolved.

def _is_name_char(c: str) -> bool:
    return c.isalnum() or c in "-_" or ord(c) >= 0x80


def _escape(css: str, i: int) -> tuple[str, int]:
    """Read the escape that starts at css[i] == '\\'. Returns (char, next)."""
    if i + 1 >= len(css) or css[i + 1] == "\n":
        raise CSSError("a backslash at the end of a line or file")
    j = i + 1
    hex_digits = ""
    while j < len(css) and len(hex_digits) < 6 and css[j] in "0123456789abcdefABCDEF":
        hex_digits += css[j]
        j += 1
    if hex_digits:
        if j < len(css) and css[j] in " \t\n":
            j += 1
        code = int(hex_digits, 16)
        return (chr(code) if 0 < code <= 0x10FFFF and not 0xD800 <= code <= 0xDFFF
                else "�"), j
    return css[j], j + 1


def _name(css: str, i: int) -> tuple[str, int]:
    out = ""
    while i < len(css):
        if css[i] == "\\":
            char, i = _escape(css, i)
            out += char
        elif _is_name_char(css[i]):
            out += css[i]
            i += 1
        else:
            break
    return out, i


def _starts_name(css: str, i: int) -> bool:
    if i >= len(css):
        return False
    c = css[i]
    if c == "\\":
        return i + 1 < len(css) and css[i + 1] != "\n"
    if c == "-":
        return i + 1 < len(css) and (_is_name_char(css[i + 1]) or css[i + 1] == "\\")
    return c.isalpha() or c == "_" or ord(c) >= 0x80


def _string(css: str, i: int) -> tuple[str, int]:
    quote, i, out = css[i], i + 1, ""
    while i < len(css):
        c = css[i]
        if c == quote:
            return out, i + 1
        if c == "\n":
            raise CSSError("a string broken by a new line")
        if c == "\\":
            if i + 1 < len(css) and css[i + 1] == "\n":
                i += 2
                continue
            char, i = _escape(css, i)
            out += char
            continue
        out += c
        i += 1
    raise CSSError("a string that is never closed")


def tokens(css: str):
    """Yield (kind, value, line): kind is 'at', 'function', 'url', 'ident' or
    'string'. Everything else is skipped."""
    i, n = 0, len(css)
    while i < n:
        line = css.count("\n", 0, i) + 1
        if css.startswith("/*", i):
            end = css.find("*/", i + 2)
            if end < 0:
                raise CSSError(f"line {line}: a comment that is never closed")
            i = end + 2
        elif css[i] in "\"'":
            value, i = _string(css, i)
            yield "string", value, line
        elif css[i] == "@" and _starts_name(css, i + 1):
            value, i = _name(css, i + 1)
            yield "at", value.lower(), line
        elif _starts_name(css, i):
            value, i = _name(css, i)
            if i < n and css[i] == "(":
                i += 1
                if value.lower() == "url":
                    while i < n and css[i] in " \t\n":
                        i += 1
                    if i < n and css[i] in "\"'":
                        target, i = _string(css, i)
                    else:
                        start = i
                        while i < n and css[i] not in ") \t\n\"'(\\":
                            i += 1
                        target = css[start:i]
                        if i < n and css[i] in "\"'(\\":
                            raise CSSError(f"line {line}: an unquoted url() holding a quote, "
                                           f"bracket or backslash")
                    while i < n and css[i] in " \t\n":
                        i += 1
                    if i >= n or css[i] != ")":
                        raise CSSError(f"line {line}: a url() that is never closed")
                    i += 1
                    yield "url", target, line
                else:
                    yield "function", value.lower(), line
            else:
                yield "ident", value.lower(), line
        else:
            i += 1


def css_problems(css: str, files: set[str]) -> list[str]:
    problems = []
    try:
        for kind, value, line in tokens(css):
            if kind == "at" and value == "import":
                problems.append(f"line {line}: @import is not allowed; one stylesheet per design")
            elif kind == "function" and value in REFUSED_FUNCTIONS:
                problems.append(f"line {line}: {value}() is not allowed; it can load from "
                                f"elsewhere or run code")
            elif kind == "ident" and value in REFUSED_IDENTS:
                problems.append(f"line {line}: '{value}' is not allowed; it was a way to run script")
            elif kind == "url":
                if not URL_TARGET_RE.match(value):
                    problems.append(f"line {line}: url({value!r}) must point at a file in this "
                                    f"design's fonts/ or img/, such as url(\"fonts/name.woff2\")")
                elif value not in files:
                    problems.append(f"line {line}: url({value!r}) names a file the design does "
                                    f"not have")
    except CSSError as error:
        problems.append(f"the stylesheet cannot be read safely: {error}")
    return problems


# The folder.

def check(name: str) -> list[str]:
    folder = DESIGNS / name
    problems: list[str] = []

    def fail(where: str, message: str) -> None:
        problems.append(f"designs/{name}/{where}: {message}" if where else
                        f"designs/{name}: {message}")

    if not NAME_RE.match(name) or len(name) > 40:
        fail("", "the folder name must be a lowercase slug of letters, digits and single "
                 "hyphens, at most 40 characters")
    try:
        mode = folder.lstat().st_mode
    except FileNotFoundError:
        fail("", "no such design")
        return problems
    if not stat.S_ISDIR(mode):
        fail("", "is not a folder")
        return problems

    files: dict[str, Path] = {}
    total = 0
    for path in sorted(folder.rglob("*")):
        relative = path.relative_to(folder).as_posix()
        mode = path.lstat().st_mode
        parts = relative.split("/")
        if stat.S_ISLNK(mode):
            fail(relative, "a symbolic link is not allowed")
            continue
        if stat.S_ISDIR(mode):
            if len(parts) != 1 or parts[0] not in SUBFOLDERS:
                fail(relative, f"only the folders {', '.join(sorted(SUBFOLDERS))} are allowed")
            continue
        if not stat.S_ISREG(mode):
            fail(relative, "not a regular file")
            continue
        suffix = path.suffix
        if not all(FILE_RE.match(p) for p in parts):
            fail(relative, "file names may hold only letters, digits, dots, hyphens and "
                           "underscores")
        elif len(parts) == 1:
            if relative == "preview.webp":
                fail(relative, "previews are taken by the deploy workflow; remove this file")
            elif relative not in ROOT_FILES:
                fail(relative, "only design.css and design.json may sit at the top of a design; "
                               "fonts go in fonts/, images in img/")
        elif len(parts) != 2 or parts[0] not in SUBFOLDERS or suffix not in SUBFOLDERS[parts[0]]:
            allowed = "; ".join(f"{f}/: {', '.join(sorted(s))}" for f, s in sorted(SUBFOLDERS.items()))
            fail(relative, f"not an allowed file. Allowed: design.css, design.json; {allowed}")
        else:
            files[relative] = path
        size = path.stat().st_size
        total += size
        limit = LIMITS.get(suffix)
        if limit and size > limit:
            fail(relative, f"{size} bytes, over the {limit // KB} KB limit for {suffix} files")
        if suffix in MAGIC:
            with path.open("rb") as handle:
                head = handle.read(16)
            if not MAGIC[suffix](head):
                fail(relative, f"its content is not a {suffix} file")
    count = len(list(folder.rglob("*")))
    if count > FILE_COUNT_LIMIT:
        fail("", f"{count} entries, over the limit of {FILE_COUNT_LIMIT}")
    if total > FOLDER_LIMIT:
        fail("", f"{total} bytes in all, over the {FOLDER_LIMIT // KB} KB limit")

    for required in sorted(ROOT_FILES):
        if not (folder / required).is_file():
            fail(required, "missing")
    texts = {}
    for relative in ("design.css", "design.json", *[f for f in files if f.endswith(".txt")]):
        path = folder / relative
        if path.is_file() and not path.is_symlink():
            data = path.read_bytes()
            try:
                if b"\0" in data:
                    raise UnicodeDecodeError("utf-8", data, 0, 1, "NUL byte")
                texts[relative] = data.decode("utf-8")
            except UnicodeDecodeError:
                fail(relative, "must be UTF-8 text")

    if "design.json" in texts:
        problems += meta_problems(name, texts, files)
    if "design.css" in texts:
        problems += [f"designs/{name}/design.css: {p}" for p in css_problems(texts["design.css"], set(files))]
    return problems


def _https(value) -> bool:
    return isinstance(value, str) and re.match(r"^https://[^\s/]+\.[^\s/]+(/\S*)?$", value) is not None


def meta_problems(name: str, texts: dict[str, str], files: dict[str, Path]) -> list[str]:
    problems = []

    def fail(message: str) -> None:
        problems.append(f"designs/{name}/design.json: {message}")

    try:
        meta = json.loads(texts["design.json"])
    except json.JSONDecodeError as error:
        fail(f"not valid JSON: {error}")
        return problems
    if not isinstance(meta, dict):
        fail("must be a JSON object")
        return problems
    unknown = sorted(set(meta) - META_FIELDS)
    if unknown:
        fail(f"fields the format does not define: {', '.join(unknown)}")
    for field, most in (("name", 40), ("author", 60), ("description", 280)):
        value = meta.get(field)
        if not (isinstance(value, str) and value.strip() and len(value) <= most and "\n" not in value):
            fail(f"{field} must be one line of text, at most {most} characters")
    if not _https(meta.get("author_url")):
        fail("author_url must be an https:// address, such as your GitHub profile")
    if not isinstance(meta.get("dark"), bool):
        fail("dark must be true or false: true if the design styles a dark theme, which gives "
             "the page the Dark switch; false keeps it light on every device")
    fonts = sorted(f for f in files if f.endswith(".woff2"))
    images = sorted(f for f in files if f.startswith("img/"))
    licence_texts = sorted(f for f in files if f.endswith(".txt"))
    preload = meta.get("preload", [])
    if not (isinstance(preload, list) and all(p in fonts for p in preload)
            and len(set(preload)) == len(preload)):
        fail("preload must list fonts in this design's fonts/, each once")
    assets = meta.get("assets")
    if not isinstance(assets, list):
        fail("assets must be a list, empty when the design has no fonts or images")
        return problems
    listed, used_texts = [], set()
    for number, asset in enumerate(assets, start=1):
        where = f"asset {number}"
        if not (isinstance(asset, dict) and {"file", "licence", "source"} <= set(asset) <= ASSET_FIELDS):
            fail(f"{where} must be {{file, licence, source}}, with licence_file for a font")
            continue
        file, licence, source = asset["file"], asset["licence"], asset["source"]
        if file not in fonts and file not in images:
            fail(f"{where}: {file!r} is not a font or image in this design")
            continue
        listed.append(file)
        if licence not in LICENCES:
            fail(f"{where}: licence {licence!r} is not one of {', '.join(sorted(LICENCES))}")
        if not (_https(source) or source == "own work"):
            fail(f"{where}: source must be the https:// address it came from, or \"own work\"")
        licence_file = asset.get("licence_file")
        if file in fonts and not licence_file:
            fail(f"{where}: a font needs licence_file, its licence text in fonts/")
        if licence_file is not None:
            if licence_file not in licence_texts:
                fail(f"{where}: licence_file {licence_file!r} is not a .txt file in fonts/")
                continue
            used_texts.add(licence_file)
            text = texts.get(licence_file, "")
            for phrase in LICENCE_TEXT.get(licence, ()):
                if phrase not in text:
                    fail(f"{where}: {licence_file} does not read as the {licence} licence "
                         f"(no {phrase!r})")
            # Not a failure: a font that reserves its name may ship only
            # unmodified, which no program can tell from the file. The
            # review checks it (CONTRIBUTING.md).
            if re.search(r"with Reserved Font Name", text, re.I):
                print(f"NOTE designs/{name}/{licence_file}: the font reserves its name, so "
                      f"{file} must be the unmodified original; the review checks this")
    for file in fonts + images:
        if listed.count(file) != 1:
            fail(f"{file} must be listed in assets exactly once, with its licence")
    for text_file in licence_texts:
        if text_file not in used_texts:
            fail(f"{text_file} is not any asset's licence_file")
    return problems


def main(argv: list[str]) -> int:
    # Page text can hold characters the console cannot write, as on Windows;
    # write them escaped rather than stop the report.
    sys.stdout.reconfigure(errors="backslashreplace")
    if any(a.startswith("-") for a in argv):
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    names = argv or sorted(p.name for p in DESIGNS.iterdir() if p.is_dir() or p.is_symlink())
    problems = []
    for name in names:
        found = check(name)
        problems += found
        print(f"{'FAIL' if found else 'ok  '} designs/{name}")
    for problem in problems:
        print(f"  {problem}")
    print(f"\n{len(names)} design(s), {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
