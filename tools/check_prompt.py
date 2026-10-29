"""Check that the prompts for an AI assistant agree with the repository
(the owner's decisions of 2026-10-21 and 2026-10-23; ADR-0017).

  python tools/check_prompt.py [README]

Each prompt restates the repository, so that an AI given it needs nothing
else; this holds it to what it restates. A prompt is the fenced block
between a README's prompt:start and prompt:end markers. Two are checked.

README.md's, the gallery's, for anyone arriving at the project:

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

.github/template-cleanup/copy-README.md's, which a copy of the template
receives as its README, for the copy's owner (ADR-0017, Changes,
2026-10-23). It is checked here, before any copy receives it, against
what a copy keeps:

  - every path it names exists and is one a copy keeps: none that
    .github/template-cleanup/remove.txt lists;
  - every fact it states equals its source: the settings it names and the
    content trace's starting value (content/config.json); the Deploy and
    Checks workflows' names, Deploy's jobs and the step a failed build
    names (.github/workflows/); the notice a run ends with while GitHub
    Pages is off (tools/ci.py), and Run workflow, which only a workflow
    that can be started by hand offers; the Python version
    (docs/how-to/use-this-template.md);
  - every command it gives appears in docs/how-to/use-this-template.md,
    the guide a copy keeps;
  - it carries the same safety rules, but security, which a copy's owner
    receives as reports of their own.

And the copy's README itself leads with turning GitHub Pages on (the
owner's decision of 2026-10-23; ADR-0015, Changes): its first block, a
callout, names the setting, the notice a run ends with until then
(tools/ci.py), the Deploy workflow by its name, and Run workflow, which
Deploy must offer.

A fact is found by the words the prompt states it in; a prompt reworded
so that a fact is no longer found fails, naming it, so the check and the
prompt change together.

Then the two routers for coding agents (ADR-0017, Changes, 2026-10-23):
AGENTS.md, and .github/template-cleanup/copy-AGENTS.md, which a copy
receives as its AGENTS.md. Each states no rule of its own, so what it
names is all there is to check: every Markdown file it names exists, and
for a copy's is one a copy keeps; every section it links is a heading of
that file, under the heading's own words (for a copy's, of copy-README.md,
the copy's README); and it links the README's section holding the prompt.

Last, the README's pictures and links on the live gallery (ADR-0017,
Changes, 2026-10-23): each names something the deploy publishes, the
gallery page, its own picture (preview.webp), a design's demo or preview
for a design in designs/, or a card's copies for an entry in showcase/,
so that a picture renamed, or a design or entry gone, fails here rather
than showing broken on GitHub.

Given a README, only its prompt is checked, as the gallery's. Exit 0 when
everything agrees; 1 on any disagreement, each printed with its file; 2
when a prompt or a router is missing. Standard library only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from build import PREVIEW_FILE, SHOWCASE_CARD, SHOWCASE_FULL, SHOWCASE_TALL, SHOWCASE_WIDE  # noqa: E402
from check_design import FILE_COUNT_LIMIT, FOLDER_LIMIT, KB, LICENCES, LIMITS, META_FIELDS, SUBFOLDERS  # noqa: E402
from check_showcase import (DESCRIPTION_LIMIT, ENTRY_FIELDS, KINDS, MAX_BYTES,  # noqa: E402
                            NAME_LIMIT)
from scope_check import AS_CONTRIBUTOR  # noqa: E402
from ci import PAGES_OFF_TITLE  # noqa: E402

CLEANUP = ".github/template-cleanup"
COPY_README = f"{CLEANUP}/copy-README.md"
COPY_AGENTS = f"{CLEANUP}/copy-AGENTS.md"
LIVE = "https://waqas01cp.github.io/portfolio-gallery/"
LIVE_ADDRESS = re.compile(re.escape(LIVE) + r"([^\s\"'<>()]*)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
MARKDOWN_NAME = re.compile(r"(?<![\w/.-])((?:[\w-]+/)*[\w-]+\.md)\b")
BLOCK =re.compile(r"<!-- prompt:start[^>]*-->\s*```text\n(.*?)\n```\s*<!-- prompt:end -->", re.S)
PATH = re.compile(r"(?<![\w/.-])((?:\.github|content|designs|docs|showcase|src|tools)/[A-Za-z0-9_./-]*)(?![\w<-])")
TICKED = re.compile(r"`([^`\s]+)`")
COMMAND = re.compile(r"^\s{3,}((?:python|\.venv)\S* .+?)\s*$", re.M)
NUMBERS = {1: "one", 2: "two", 3: "three", 4: "four"}
SAFETY = ("explain what it does", "Never ask for, accept or handle a password",
          "Never say you have done any of these", "stays in its public history",
          "privately, never in a public issue")
# A copy's owner is the one who receives reports about their site.
COPY_SAFETY = SAFETY[:4]
GALLERY_GUIDES = ("docs/reference/commands.md", "docs/how-to/add-a-design.md")
COPY_GUIDES = ("docs/how-to/use-this-template.md",)


def flat(text: str) -> str:
    return " ".join(text.split())


def words(listed: str) -> set[str]:
    return {w.strip(" .") for w in re.split(r",\s*|\s+or\s+|\s+and\s+", listed) if w.strip(" .")}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def block(text: str) -> str | None:
    """A README's prompt, or None."""
    m = BLOCK.search(text)
    return m.group(1) if m else None


def named_paths(raw: str) -> set[str]:
    bare = re.sub(r"https?://\S+", " ", raw)
    named = {p.rstrip(".,") for p in PATH.findall(bare)}
    return named | {p.rstrip(".,") for p in TICKED.findall(raw) if "<" not in p and not p.startswith("[")}


def commands(raw: str) -> list[str]:
    return [flat(c) for c in COMMAND.findall(raw)]


def removed() -> list[str]:
    """What the template cleanup removes from a copy, from its own list."""
    return [line.strip().rstrip("/") for line in read(f"{CLEANUP}/remove.txt").splitlines()
            if line.strip() and not line.strip().startswith("#")] + [CLEANUP]


def kept(path: str) -> bool:
    """Whether a path exists here and a copy keeps it."""
    parts = PurePosixPath(path.rstrip("/")).parts
    gone = any(parts[:len(PurePosixPath(r).parts)] == PurePosixPath(r).parts for r in removed())
    return (ROOT / path).exists() and not gone


def workflow(name: str) -> tuple[str | None, list[str], list[str]]:
    """A workflow's name, its jobs and its steps' names."""
    text = read(f".github/workflows/{name}")
    title = re.search(r"^name:\s*(.+)$", text, re.M)
    jobs = re.findall(r"^  ([\w-]+):\s*$", text.split("\njobs:\n", 1)[-1], re.M)
    steps = [s.strip() for s in re.findall(r"^\s+- name: (.+)$", text, re.M)]
    return (title.group(1).strip() if title else None), jobs, steps


def by_hand(name: str) -> bool:
    """Whether a workflow can be started by hand, so offers Run workflow."""
    on = read(f".github/workflows/{name}").split("\njobs:\n", 1)[0]
    return bool(re.search(r"^\s+workflow_dispatch\s*:", on, re.M))


def pages_notice(prompt: str) -> tuple[str, object, object]:
    """The notice a run ends with while Pages is off, as a text quotes it."""
    m = re.search(r"ends with the notice \"([^\"]+)\"", prompt)
    return "the notice a Deploy run ends with while GitHub Pages is off", m.group(1) if m else None, PAGES_OFF_TITLE


def copy_lead(readme: str) -> list[tuple[str, object, object]]:
    """The copy's README leads with turning Pages on: its first block after
    the title, a callout, read as facts."""
    body = readme.split("\n", 1)[1].lstrip("\n") if readme.startswith("# ") else ""
    callout = body.split("\n\n", 1)[0]
    lead = flat(re.sub(r"^> ?", "", callout, flags=re.M))
    deploy, _, _ = workflow("deploy.yml")
    find = finder(lead)
    return [
        ("the copy's README opening with a callout on turning GitHub Pages on",
         callout.startswith("> [!IMPORTANT]") and "turn on GitHub Pages" in lead, True),
        ("the setting the callout names", "set **Source** to **GitHub Actions**" in lead, True),
        pages_notice(lead),
        ("the workflow the callout says to run", find(r"\*\*Actions\*\*, \*\*(\w+)\*\* in the left list"), deploy),
        ("Run workflow, named by the callout, offered by Deploy",
         "**Run workflow**" in lead and by_hand("deploy.yml"), True),
    ]


def finder(prompt: str):
    def find(pattern: str, cast=str):
        m = re.search(pattern, prompt)
        return cast(m.group(1)) if m else None
    return find


def facts(prompt: str) -> list[tuple[str, object, object]]:
    """The gallery's prompt: (what, what the prompt says, what the source
    says); None where the prompt's words for it are not found."""
    find = finder(prompt)
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
        pages_notice(prompt),
    ]


def copy_facts(prompt: str) -> list[tuple[str, object, object]]:
    """A copy's prompt, as facts() is the gallery's."""
    find = finder(prompt)
    config = json.loads(read("content/config.json"))
    deploy, deploy_jobs, deploy_steps = workflow("deploy.yml")
    checks, _, _ = workflow("checks.yml")
    settings = find(r"`content/config\.json`: the settings, (.*?)\.", lambda s: set(re.findall(r"\"(\w+)\"", s)))
    jobs = re.search(r"with the jobs (\w+), (\w+), (\w+) and (\w+)\. Two more, (\w+) and (\w+), are skipped", prompt)
    step = find(r"its failed step, usually \"([^\"]+)\"")
    return [
        ("the settings named, each in content/config.json", settings <= set(config) if settings else None, True),
        ("the content trace's starting value", find(r"While \"content_trace\" is (\w+), as it is to start"),
         json.dumps(config.get("content_trace"))),
        ("the Deploy workflow's name", find(r"starts a (\w+) run in the Actions tab"), deploy),
        ("Deploy's jobs", set(jobs.groups()) if jobs else None, set(deploy_jobs)),
        ("the step a failed build names, one of Deploy's", step,
         step if step in deploy_steps else "no step of that name"),
        ("the Checks workflow's name", find(r"The (\w+) run beside it runs accessibility checks"), checks),
        pages_notice(prompt),
        ("Run workflow, named by the prompt, offered by Deploy",
         "Deploy in the left list, Run workflow" in prompt and by_hand("deploy.yml"), True),
        ("the Python version", find(r"With Python ([\d.]+) or later"),
         re.search(r"Python ([\d.]+) or later", read(COPY_GUIDES[0])).group(1)),
    ]


def check_prompt(raw: str, stated, safety: tuple[str, ...], guides: tuple[str, ...],
                 for_copy: bool) -> tuple[list[str], str]:
    """Problems with one prompt, and a count of what was checked."""
    prompt = flat(raw)
    problems = []
    named = named_paths(raw)
    for path in sorted(named):
        if not (ROOT / path).exists():
            problems.append(f"it names {path}, which does not exist")
        elif for_copy and not kept(path):
            problems.append(f"it names {path}, which a copy does not receive "
                            f"({CLEANUP}/remove.txt lists it)")
    checked = stated(prompt)
    for what, said, source in checked:
        if said is None:
            problems.append(f"{what}: its words for it are not found; the prompt and this check must change together")
        elif said != source:
            problems.append(f"{what}: the prompt says {said!r}, the repository {source!r}")
    sources = flat("\n".join(read(g) for g in guides))
    given = commands(raw)
    for command in given:
        if command not in sources:
            problems.append(f"the command '{command}' is in neither {' nor '.join(guides)}" if len(guides) > 1
                            else f"the command '{command}' is not in {guides[0]}"
                            + (", the guide a copy keeps" if for_copy else ""))
    for phrase in safety:
        if phrase not in prompt:
            problems.append(f"its safety rule '{phrase}' is missing")
    return problems, (f"{len(named)} path(s), {len(checked)} fact(s), {len(given)} command(s), "
                      f"{len(safety)} safety rule(s)")


def slug(heading: str) -> str:
    """GitHub's anchor for a heading: lower case, punctuation dropped,
    spaces as hyphens."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def sections(text: str) -> dict[str, tuple[str, str]]:
    """A Markdown file's headings by anchor: (the heading, its section's text)."""
    found, heads = {}, list(re.finditer(r"^(#{1,6}) (.+?)\s*$", text, re.M))
    for i, m in enumerate(heads):
        end = next((h.start() for h in heads[i + 1:] if len(h.group(1)) <= len(m.group(1))), len(text))
        found[slug(m.group(2))] = (m.group(2), text[m.end():end])
    return found


def check_router(text: str, for_copy: bool) -> list[str]:
    """Problems with AGENTS.md, or with a copy's."""
    own = {"README.md": COPY_README if for_copy else "README.md",
           "AGENTS.md": COPY_AGENTS if for_copy else "AGENTS.md"}
    problems, prompt_linked = [], False
    named = set(MARKDOWN_NAME.findall(text)) | {t.split("#", 1)[0] for _, t in LINK.findall(text)}
    for path in sorted(p for p in named if p):
        if not (ROOT / own.get(path, path)).exists():
            problems.append(f"it names {path}, which does not exist")
        elif for_copy and path not in own and not kept(path):
            problems.append(f"it names {path}, which a copy does not receive ({CLEANUP}/remove.txt lists it)")
    for linked_as, target in LINK.findall(text):
        path, _, anchor = target.partition("#")
        if not anchor or not (ROOT / own.get(path, path)).is_file():
            continue
        found = sections(read(own.get(path, path)))
        where = "the copy's README" if for_copy and path == "README.md" else path
        if anchor not in found:
            problems.append(f"it links {target}, a section {where} does not have")
        elif found[anchor][0] != linked_as:
            problems.append(f"it links {target} as '{linked_as}', but the heading reads '{found[anchor][0]}'")
        elif path == "README.md" and block(found[anchor][1]) is not None:
            prompt_linked = True
    if not prompt_linked:
        problems.append("it links no section of the README that holds its prompt for an AI assistant")
    return problems


def published(path: str) -> bool:
    """Whether the deploy publishes this path on the live gallery."""
    if path == "" or path.startswith("#") or path == PREVIEW_FILE:
        return True
    design = re.fullmatch(rf"designs/([a-z0-9-]+)/(?:index\.html|{re.escape(PREVIEW_FILE)})", path)
    if design:
        return (ROOT / "designs" / design.group(1) / "design.json").is_file()
    entry = re.fullmatch(rf"showcase/([a-z0-9-]+)/(?:{re.escape(SHOWCASE_CARD)}|{re.escape(SHOWCASE_FULL)})", path)
    return bool(entry) and (ROOT / "showcase" / entry.group(1) / "entry.json").is_file()


def check_live(readme: str) -> tuple[list[str], int]:
    """The README's addresses on the live gallery, each one the deploy publishes."""
    addresses = sorted({a.rstrip("*.,;:") for a in LIVE_ADDRESS.findall(readme)})
    return [f"it shows or links {LIVE}{a}, which the deploy does not publish"
            for a in addresses if not published(a)], len(addresses)


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(errors="backslashreplace")
    prompts = [(Path(argv[0]) if argv else ROOT / "README.md", facts, SAFETY, GALLERY_GUIDES, False)]
    if not argv:
        prompts.append((ROOT / COPY_README, copy_facts, COPY_SAFETY, COPY_GUIDES, True))
    failures = 0
    for path, stated, safety, guides, for_copy in prompts:
        shown = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
        raw = block(path.read_text(encoding="utf-8")) if path.is_file() else None
        if raw is None:
            print(f"no prompt between prompt:start and prompt:end in {shown}", file=sys.stderr)
            return 2
        problems, counts = check_prompt(raw, stated, safety, guides, for_copy)
        if for_copy:
            for what, said, source in copy_lead(path.read_text(encoding="utf-8")):
                if said is None:
                    problems.append(f"its README's lead, {what}: its words for it are not found")
                elif said != source:
                    problems.append(f"its README's lead, {what}: it says {said!r}, the repository {source!r}")
            counts += ", the lead's 5 facts"
        for problem in problems:
            print(f"FAIL {shown}: {problem}")
        print(f"{shown}: {counts}; {len(problems)} problem(s)")
        failures += len(problems)
    for router, for_copy in ([] if argv else [("AGENTS.md", False), (COPY_AGENTS, True)]):
        if not (ROOT / router).is_file():
            print(f"no {router}", file=sys.stderr)
            return 2
        problems = check_router(read(router), for_copy)
        for problem in problems:
            print(f"FAIL {router}: {problem}")
        print(f"{router}: {len(LINK.findall(read(router)))} link(s); {len(problems)} problem(s)")
        failures += len(problems)
    if not argv:
        problems, count = check_live(read("README.md"))
        for problem in problems:
            print(f"FAIL README.md: {problem}")
        print(f"README.md: {count} address(es) on the live gallery; {len(problems)} problem(s)")
        failures += len(problems)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
