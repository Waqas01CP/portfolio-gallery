"""Check that the README's prompt for an AI assistant agrees with the
repository (the owner's decision of 2026-10-21; ADR-0017).

  python tools/check_prompt.py [README]

The prompt restates the repository, so that an AI given it needs nothing
else; this holds it to what it restates. It reads the fenced block
between the README's prompt:start and prompt:end markers and checks:

  - every path it names exists: each one in backticks, and each one under
    .github/, content/, designs/, docs/, showcase/, src/ or tools/, a
    placeholder such as designs/<name>/ aside;
  - every fact it states equals its source: the screenshot formats, the
    cap and the entry's limits and fields (tools/check_showcase.py); the
    shape limits (build.py); a design's files, sizes, design.json fields
    and licences (tools/check_design.py); the settings it names
    (content/config.json); the scope marker (tools/scope_check.py); the
    pull request template's sections; the issue forms and whether blank
    issues are on (.github/ISSUE_TEMPLATE/); the first response's days
    (CONTRIBUTING.md); the Python version (docs/how-to/add-a-design.md);
  - every command it gives appears in docs/reference/commands.md or
    docs/how-to/add-a-design.md;
  - it carries its safety rules: explain each step first, never handle a
    secret, the person acts on GitHub, the public history, security
    reported privately.

A fact is found by the words the prompt states it in; a prompt reworded
so that a fact is no longer found fails, naming it, so the check and the
prompt change together. Exit 0 when everything agrees; 1 on any
disagreement, each printed; 2 when there is no prompt to check. Standard
library only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from build import SHOWCASE_TALL, SHOWCASE_WIDE  # noqa: E402
from check_design import FILE_COUNT_LIMIT, FOLDER_LIMIT, KB, LICENCES, LIMITS, META_FIELDS, SUBFOLDERS  # noqa: E402
from check_showcase import (DESCRIPTION_LIMIT, ENTRY_FIELDS, KINDS, MAX_BYTES,  # noqa: E402
                            NAME_LIMIT)
from scope_check import AS_CONTRIBUTOR  # noqa: E402

BLOCK = re.compile(r"<!-- prompt:start[^>]*-->\s*```text\n(.*?)\n```\s*<!-- prompt:end -->", re.S)
PATH = re.compile(r"(?<![\w/.-])((?:\.github|content|designs|docs|showcase|src|tools)/[A-Za-z0-9_./-]*)(?![\w<-])")
TICKED = re.compile(r"`([^`\s]+)`")
COMMAND = re.compile(r"^\s{3,}((?:python|\.venv)\S* .+?)\s*$", re.M)
NUMBERS = {1: "one", 2: "two", 3: "three", 4: "four"}
SAFETY = ("explain what it does", "Never ask for, accept or handle a password",
          "Never say you have done any of these", "stays in its public history",
          "privately, never in a public issue")


def flat(text: str) -> str:
    return " ".join(text.split())


def words(listed: str) -> set[str]:
    return {w.strip(" .") for w in re.split(r",\s*|\s+or\s+|\s+and\s+", listed) if w.strip(" .")}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def facts(prompt: str) -> list[tuple[str, object, object]]:
    """(what, what the prompt says, what the source says); None where the
    prompt's words for it are not found."""

    def find(pattern: str, cast=str):
        m = re.search(pattern, prompt)
        return cast(m.group(1)) if m else None

    template = read(".github/pull_request_template.md")
    sections = re.findall(r"^## (.+)$", template, re.M)
    forms = {}
    for form in sorted((ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.yml")):
        text = form.read_text(encoding="utf-8")
        m = re.search(r"^name:\s*(.+)$", text, re.M)
        if m:
            forms[m.group(1).strip().strip("\"'")] = form.name
    config_text = read(".github/ISSUE_TEMPLATE/config.yml")
    blank_off = bool(re.search(r"^blank_issues_enabled:\s*false\s*$", config_text, re.M))
    image_limits = {LIMITS[s] for s in SUBFOLDERS["img"]}
    stated_forms = find(r"The issue forms are (.+?)\. Blank")
    entry_json = find(r"(\{\"name\": .*?\})")
    meta = re.search(r"design\.json: (\"name\".*?)- Licences", prompt)
    settings = re.search(r"`content/config\.json` the settings: (.*?)\.", prompt)
    return [
        ("the screenshot formats", find(r"Screenshot formats: (.+?)\.", lambda s: {w.lower() for w in words(s)}),
         set(KINDS.values())),
        ("the screenshot's cap in MB", find(r"be at most (\d+) MB", int), MAX_BYTES // (1024 * 1024)),
        ("the tall shape limit", find(r"more than ([\d.]+) times as tall as it is wide", float), SHOWCASE_TALL),
        ("the wide shape limit", find(r"more than ([\d.]+) times as wide as it is tall", float), SHOWCASE_WIDE),
        ("the entry's name limit", find(r"The name is at most (\d+) characters", int), NAME_LIMIT),
        ("the entry's description limit", find(r"description optional and at most (\d+) characters", int),
         DESCRIPTION_LIMIT),
        ("the entry's fields", set(json.loads(entry_json)) if entry_json else None, set(ENTRY_FIELDS)),
        ("a design's stylesheet limit in KB", find(r"Files: design\.css \(at most (\d+) KB\)", int), LIMITS[".css"] // KB),
        ("a design's font limit in KB", find(r"\.woff2 \(at most (\d+) KB each\)", int), LIMITS[".woff2"] // KB),
        ("a design's image types", find(r"images as (.+?) \(at most", lambda s: {"." + w.lstrip(".") for w in words(s)}),
         set(SUBFOLDERS["img"])),
        ("a design's image limit in KB", find(r"\.jpeg \(at most (\d+) KB each\)", int),
         image_limits.pop() // KB if len(image_limits) == 1 else image_limits),
        ("a design's total in KB", find(r"at most (\d+) KB and \d+ files in all", int), FOLDER_LIMIT // KB),
        ("a design's file count", find(r"at most \d+ KB and (\d+) files in all", int), FILE_COUNT_LIMIT),
        ("design.json's fields", set(re.findall(r"\"(\w+)\"", meta.group(1))) if meta else None, set(META_FIELDS)),
        ("the licences allowed", find(r"Licences allowed for fonts and images: (.+?)\. ", words), set(LICENCES)),
        ("the settings named, each in content/config.json",
         set(re.findall(r"\"(\w+)\"", settings.group(1))) <= set(json.loads(read("content/config.json")))
         if settings else None, True),
        ("the scope marker", find(r"the marker `(\[scope: [^`]+\])`"), AS_CONTRIBUTOR),
        ("the template's sections, by count", find(r"opens with (\w+) sections"), NUMBERS.get(len(sections))),
        ("the template's sections, each kept by name",
         all(f"keep {s}" in prompt for s in sections) and f"two sections, {' and '.join(sections)}" in prompt,
         True),
        ("the issue forms", words(re.sub(r"\s*\(.*?\)", "", stated_forms)) if stated_forms else None,
         set(forms)),
        ("blank issues turned off", "Blank issues are turned off" in prompt, blank_off),
        ("the first response's days", find(r"A first response comes within (\d+) days", int),
         int(re.search(r"A first response within (\d+) days", read("CONTRIBUTING.md")).group(1))),
        ("the Python version", find(r"Python ([\d.]+) or later"),
         re.search(r"Python ([\d.]+) or later", read("docs/how-to/add-a-design.md")).group(1)),
    ]


def main(argv: list[str]) -> int:
    readme = Path(argv[0]) if argv else ROOT / "README.md"
    m = BLOCK.search(readme.read_text(encoding="utf-8")) if readme.is_file() else None
    if not m:
        print(f"no prompt between prompt:start and prompt:end in {readme}", file=sys.stderr)
        return 2
    raw = m.group(1)
    prompt = flat(raw)
    problems = []
    bare = re.sub(r"https?://\S+", " ", raw)
    named = {p.rstrip(".,") for p in PATH.findall(bare)}
    named |= {p.rstrip(".,") for p in TICKED.findall(raw) if "<" not in p and not p.startswith("[")}
    for path in sorted(named):
        if not (ROOT / path).exists():
            problems.append(f"it names {path}, which does not exist")
    for what, said, source in facts(prompt):
        if said is None:
            problems.append(f"{what}: its words for it are not found; the prompt and this check must change together")
        elif said != source:
            problems.append(f"{what}: the prompt says {said!r}, the repository {source!r}")
    sources = flat(read("docs/reference/commands.md") + "\n" + read("docs/how-to/add-a-design.md"))
    commands = [flat(c) for c in COMMAND.findall(raw)]
    for command in commands:
        if command not in sources:
            problems.append(f"the command '{command}' is in neither docs/reference/commands.md nor "
                            f"docs/how-to/add-a-design.md")
    for phrase in SAFETY:
        if phrase not in prompt:
            problems.append(f"its safety rule '{phrase}' is missing")
    for problem in problems:
        print(f"FAIL {problem}")
    print(f"{len(named)} path(s), {len(facts(prompt))} fact(s), {len(commands)} command(s), "
          f"{len(SAFETY)} safety rule(s); {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
