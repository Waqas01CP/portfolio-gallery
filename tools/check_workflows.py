"""Check when each workflow job runs, without running it.

  python tools/check_workflows.py           every .github/workflows/*.yml
  python tools/check_workflows.py FILE ...  the named workflow files only

GitHub skips a job when a job before it in its chain of `needs` was skipped
or failed, through the whole chain, unless the job's own `if:` holds a
status function; an `if:` without one gets `success()` added. A skipped
job reports success, so the run stays green while it does nothing (GitHub
Docs, "Using jobs in a workflow" and "Expressions", read 2026-10-16). The
deploy job did exactly that on 2026-10-16: shots is skipped in site mode,
so deploy was skipped in every run, and no copy of the template would
ever have published.

A job can be skipped if it has an `if:`, or if it needs a job that can be.
Every job that needs a job that can be skipped must have an `if:` that:

  - holds `always()`, `cancelled()` (as in `!cancelled()`) or `failure()`,
    so GitHub adds no `success()`;
  - with `always()` or `cancelled()`, names `needs.<job>.result` for every
    job it needs, so it cannot run after one of them failed.

It also refuses a `needs` naming no job in the file, and a workflow that
runs on a schedule unless it holds no permissions at all: `permissions: {}`
at the top and none in its jobs. A scheduled run starts with nobody's
review, so it may write nothing (ADR-0016, the owner's answer Q2 of
2026-10-19).

Every job that fetches axe-core, in every workflow, must pin the same
version and SHA-512 (AXE_VERSION, AXE_SHA512): the weekly run of every
page and the checks of each change judge pages by the same rules
(ADR-0019). A verdict job, which runs `tools/ci.py verdict` after a
failure on purpose so as to fail itself, may name the results it needs in
its steps rather than its if:, and must name every one.

Every `uses:` names an action at a full commit SHA, which no one can
move, as a tag can be. npm runs only as `npm ci --ignore-scripts`: every
package checked against a committed lockfile's hash, and no package's
install script run; no `npm install`, no `npx`, no other package
manager (ADR-0012).

A workflow that publishes with actions/deploy-pages must ask first
whether GitHub Pages is on (the owner's decision of 2026-10-23; ADR-0015,
Changes): a job named pages running `tools/ci.py pages`; the publishing
job needing it and running only when `needs.pages.outputs.on == 'true'`;
no other job needing or reading it, so a build or check never waits on
Pages and still fails when it should; and no `continue-on-error`, which
would end a failed run green. And the decision itself,
tools/ci.py's pages_verdict, must give its table: with Pages off, a
notice in a copy and a failure in the gallery; publishing from GitHub
Actions, publish; from a branch, or any other answer, fail.

Its limit: it checks that each result is named, not what the condition
does with it. `!cancelled() && needs.assemble.result != 'success'` passes,
though such a job runs only after assemble did not succeed (the portfolio
architecture chat, 2026-10-18). Reading GitHub's expression language is
beyond it; the review of a workflow change reads the condition.

It reads only the YAML the workflows use under `jobs:`: block mappings by
indentation, `needs:` as one name, a flow list or a block list, and `if:`
as a plain or quoted scalar, a continued plain scalar, or a folded or
literal block. At the level of the jobs and their keys, anything else (a
tab, an anchor, alias, tag or merge key, a flow mapping, a line it cannot
place) is reported as unreadable, never passed. What lies deeper, such as
a step's inputs, is skipped: it cannot change when a job runs.
Exit 0 on a pass, 1 on a failure with every problem printed, 2 on a usage
error. Standard library only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
sys.path.insert(0, str(ROOT / "tools"))
from ci import pages_verdict  # noqa: E402

PUBLISH = "actions/deploy-pages@"
PAGES_ON = re.compile(r"""needs\s*\.\s*pages\s*\.\s*outputs\s*\.\s*on\s*==\s*['"]true['"]""")
READS_PAGES = re.compile(r"needs\s*\.\s*pages\b")
# (mode, the API's status, build_type, what Deploy must do, why).
PAGES_TABLE = (
    ("site", 404, None, "notice", "with Pages off, a copy's Deploy ends with a notice and publishes nothing, "
                                  "never red on a stranger's first run"),
    ("gallery", 404, None, "fail", "with Pages off, the gallery's Deploy fails: the gallery would be down"),
    ("site", 200, "workflow", "publish", "with Pages publishing from GitHub Actions, a copy publishes"),
    ("gallery", 200, "workflow", "publish", "with Pages publishing from GitHub Actions, the gallery publishes"),
    ("site", 200, "legacy", "fail", "with Pages publishing from a branch, what it shows is not what was built"),
    ("site", 500, None, "fail", "any other answer from GitHub's API fails"),
)

KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:(?:\s+(.*))?$")
VERDICT = "tools/ci.py verdict"
USES = re.compile(r"^\s*(?:-\s+)?uses:\s*(\S+)")
PINNED = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+@[0-9a-f]{40}")
PACKAGES = re.compile(r"\b(npm|npx|pnpm|yarn|bun)\b(.*)")
STATUS = re.compile(r"\b(always|cancelled|failure)\s*\(\s*\)")
RESULT = re.compile(r"""needs\s*(?:\.\s*([A-Za-z0-9_-]+)|\[\s*['"]([A-Za-z0-9_-]+)['"]\s*\])\s*\.\s*result""")


class Unreadable(Exception):
    pass


def strip_comment(value: str) -> str:
    """A YAML comment starts with # after a space, outside quotes."""
    quote = None
    for i, ch in enumerate(value):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "#" and (i == 0 or value[i - 1] in " \t"):
            return value[:i].rstrip()
    return value.rstrip()


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def read_jobs(text: str) -> dict[str, dict]:
    """{job: {"needs": [names], "if": expression or None, "line": n}}."""
    lines = text.splitlines()
    rows = []  # (line number, indent, content) under jobs:, blanks and comments dropped
    inside = False
    for number, line in enumerate(lines, 1):
        if not inside:
            if re.match(r"^jobs\s*:\s*(#.*)?$", line):
                inside = True
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1] not in (" ", "\t"):
            break  # the next top-level key
        if "\t" in line[:indent_of(line) + 1]:
            raise Unreadable(f"line {number}: a tab in the indentation")
        rows.append((number, indent_of(line), line.strip()))
    if not inside:
        raise Unreadable("no jobs: mapping at the top level")
    if not rows:
        return {}
    job_indent = rows[0][1]
    jobs: dict[str, dict] = {}
    i = 0
    while i < len(rows):
        number, indent, content = rows[i]
        if indent != job_indent:
            raise Unreadable(f"line {number}: cannot place this line in a job")
        match = KEY.match(content)
        if not match or (match[2] and strip_comment(match[2])):
            raise Unreadable(f"line {number}: expected a job name ending in ':'")
        job = {"needs": [], "if": None, "line": number}
        jobs[match[1]] = job
        i += 1
        body = []
        while i < len(rows) and rows[i][1] > job_indent:
            body.append(rows[i])
            i += 1
        job["body"] = "\n".join(content for _, _, content in body)
        read_job(body, job)
    return jobs


def read_job(body: list[tuple[int, int, str]], job: dict) -> None:
    if not body:
        return
    prop = body[0][1]
    i = 0
    while i < len(body):
        number, indent, content = body[i]
        if indent != prop:
            raise Unreadable(f"line {number}: cannot place this line")
        match = KEY.match(content)
        if not match:
            raise Unreadable(f"line {number}: expected a key")
        key, value = match[1], strip_comment(match[2] or "")
        i += 1
        nested = []
        while i < len(body) and (body[i][1] > prop or (body[i][1] == prop and body[i][2].startswith("- "))):
            nested.append(body[i])
            i += 1
        if key == "needs":
            job["needs"] = read_needs(value, nested, number)
        elif key == "if":
            job["if"] = read_scalar(value, nested, number)
        elif key == "permissions":
            job["permissions"] = number


def refuse_special(value: str, number: int) -> None:
    if value[:1] in ("&", "*", "{", "!"):
        raise Unreadable(f"line {number}: an anchor, alias, tag or flow mapping")


def read_needs(value: str, nested, number: int) -> list[str]:
    if value:
        refuse_special(value, number)
        if nested:
            raise Unreadable(f"line {number}: needs: has a value and lines below it")
        if value.startswith("["):
            if not value.endswith("]"):
                raise Unreadable(f"line {number}: a flow list that does not close on its line")
            names = [unquote(strip_comment(n).strip()) for n in value[1:-1].split(",")]
            return [n for n in names if n]
        return [unquote(value)]
    names = []
    for n, _, content in nested:
        if not content.startswith("- "):
            raise Unreadable(f"line {n}: expected '- name' under needs:")
        item = strip_comment(content[2:].strip())
        refuse_special(item, n)
        names.append(unquote(item))
    return names


def read_scalar(value: str, nested, number: int) -> str:
    if value[:1] in (">", "|"):
        if not re.fullmatch(r"[>|][+-]?[0-9]?", value):
            raise Unreadable(f"line {number}: a block scalar header it cannot read")
        return " ".join(content for _, _, content in nested)
    refuse_special(value, number)
    if value[:1] in ("'", "\""):
        if nested or len(value) < 2 or value[-1] != value[0]:
            raise Unreadable(f"line {number}: a quoted value that does not close on its line")
        return unquote(value)
    return " ".join([value] + [strip_comment(content) for _, _, content in nested]).strip()


def top_level(text: str) -> dict[str, tuple[int, str, list[str]]]:
    """{key: (line, value, the lines under it)} for the file's top-level keys."""
    keys: dict[str, tuple[int, str, list[str]]] = {}
    current = None
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1] not in (" ", "\t"):
            match = KEY.match(line.strip())
            if match:
                current = match[1].strip("'\"")
                keys[current] = (number, strip_comment(match[2] or ""), [])
            continue
        if current:
            keys[current][2].append(line)
    return keys


def schedule_problems(text: str, jobs: dict[str, dict], shown: str) -> list[str]:
    keys = top_level(text)
    trigger = keys.get("on") or keys.get("true")
    if not trigger:
        return []
    _, value, nested = trigger
    if "schedule" not in value and not any(re.match(r"^\s+schedule\s*:", l) for l in nested):
        return []
    problems = []
    if "permissions" not in keys or keys["permissions"][1] != "{}" or keys["permissions"][2]:
        problems.append(f"{shown}: runs on a schedule, so it must hold no permissions: "
                        f"`permissions: {{}}` at the top")
    for name, job in jobs.items():
        if job.get("permissions"):
            problems.append(f"{shown}, job '{name}' (line {job['permissions']}): runs on a schedule, "
                            f"so it may grant itself no permissions")
    return problems


def pages_problems(text: str, jobs: dict[str, dict], shown: str) -> list[str]:
    """A workflow that publishes asks first whether Pages is on."""
    if PUBLISH not in text:
        return []
    problems = []
    lines = text.splitlines()
    starts = sorted((job["line"], name) for name, job in jobs.items())
    publishing = []
    for i, (line, name) in enumerate(starts):
        end = starts[i + 1][0] - 1 if i + 1 < len(starts) else len(lines)
        if any(PUBLISH in row for row in lines[line - 1:end]):
            publishing.append(name)
    if "pages" not in jobs or "tools/ci.py pages" not in text:
        problems.append(f"{shown}: publishes with actions/deploy-pages but has no job 'pages' running "
                        f"tools/ci.py pages, which says whether GitHub Pages is on")
    for name in publishing:
        job = jobs[name]
        if "pages" not in job["needs"] or not PAGES_ON.search(job["if"] or ""):
            problems.append(f"{shown}, job '{name}' (line {job['line']}): it publishes, so it must need "
                            f"'pages' and run only when needs.pages.outputs.on == 'true'")
    for name, job in jobs.items():
        if name in publishing or name == "pages":
            continue
        if "pages" in job["needs"] or READS_PAGES.search(job["if"] or ""):
            problems.append(f"{shown}, job '{name}' (line {job['line']}): it waits on or reads the pages job, "
                            f"so with Pages off a build or check that should fail could be skipped; only "
                            f"the publishing job may")
    if re.search(r"^\s*-?\s*continue-on-error\s*:", text, re.M):
        problems.append(f"{shown}: continue-on-error would let a failed build or check end the run green")
    for mode, status, build_type, want, why in PAGES_TABLE:
        got, _ = pages_verdict(mode, status, build_type)
        if got != want:
            problems.append(f"{shown}: tools/ci.py's pages_verdict gives '{got}' for {mode} mode, the API "
                            f"answering {status}{f' with {build_type}' if build_type else ''}, where it must "
                            f"give '{want}': {why}")
    return problems


def skippable(jobs: dict[str, dict]) -> set[str]:
    found = {name for name, job in jobs.items() if job["if"] is not None}
    changed = True
    while changed:
        changed = False
        for name, job in jobs.items():
            if name not in found and any(n in found for n in job["needs"]):
                found.add(name)
                changed = True
    return found


def supply_problems(text: str, shown: str) -> list[str]:
    """Actions at a full SHA; npm only as npm ci --ignore-scripts."""
    problems = []
    for number, line in enumerate(text.splitlines(), start=1):
        code = strip_comment(line)
        uses = USES.match(code)
        if uses and not PINNED.fullmatch(unquote(uses.group(1))):
            problems.append(f"{shown}, line {number}: {uses.group(1)} is not pinned to a full commit SHA")
        if re.match(r"\s*(?:-\s+)?name:", code):
            continue
        for tool, rest in PACKAGES.findall(code):
            if tool != "npm" or not re.match(r"\s+ci\b", rest) or "--ignore-scripts" not in rest.split():
                problems.append(f"{shown}, line {number}: {tool} runs only as `npm ci --ignore-scripts`, "
                                f"from a committed lockfile with no install script (ADR-0012)")
    return problems


def check_file(path: Path) -> list[str]:
    shown = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
    text = path.read_text(encoding="utf-8")
    try:
        jobs = read_jobs(text)
    except Unreadable as error:
        return [f"{shown}: unreadable under jobs:, {error}"]
    problems = (schedule_problems(text, jobs, shown) + pages_problems(text, jobs, shown)
                + supply_problems(text, shown))
    can_skip = skippable(jobs)
    for name, job in jobs.items():
        where = f"{shown}, job '{name}' (line {job['line']})"
        for need in job["needs"]:
            if need not in jobs:
                problems.append(f"{where}: needs '{need}', which is not a job in this file")
        risky = [n for n in job["needs"] if n in can_skip]
        if not risky:
            continue
        reason = (f"it needs {', '.join(repr(n) for n in risky)}, which can be skipped, and GitHub "
                  f"then skips it too")
        condition = job["if"]
        if condition is None:
            problems.append(f"{where}: has no if: of its own; {reason}")
            continue
        functions = set(STATUS.findall(condition))
        if not functions:
            problems.append(f"{where}: its if: holds no always(), cancelled() or failure(), so "
                            f"success() is still applied; {reason}")
            continue
        if functions & {"always", "cancelled"}:
            named = {a or b for a, b in RESULT.findall(condition)}
            # A verdict job runs after a failure on purpose, to fail itself:
            # it may name the results in its steps, where tools/ci.py verdict
            # reads them, and must name every one.
            verdict = VERDICT in job.get("body", "")
            if verdict:
                named |= {a or b for a, b in RESULT.findall(job["body"])}
            missing = [n for n in job["needs"] if n not in named]
            if missing:
                problems.append(f"{where}: its if: does not name "
                                f"{', '.join(f'needs.{n}.result' for n in missing)}, so it would run "
                                f"after that job failed"
                                + ("; a verdict job must pass every result to the verdict" if verdict else ""))
    return problems


def axe_pins(text: str) -> set[tuple[str | None, str | None]]:
    """Every axe-core version and SHA-512 a workflow fetches, in each of its
    jobs that fetch it."""
    versions = re.findall(r'^\s*AXE_VERSION:\s*"?([^"\s]+)"?\s*$', text, re.M)
    shas = re.findall(r"^\s*AXE_SHA512:\s*([0-9a-f]+)\s*$", text, re.M)
    if len(versions) != len(shas):
        return {(v, None) for v in versions} | {(None, h) for h in shas}
    return set(zip(versions, shas))


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(errors="backslashreplace")
    if any(a.startswith("-") for a in argv):
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    files = [Path(a).resolve() for a in argv] or sorted(WORKFLOWS.glob("*.yml")) + sorted(WORKFLOWS.glob("*.yaml"))
    missing = [str(f) for f in files if not f.is_file()]
    if missing or not files:
        print(f"no workflow file: {', '.join(missing) or WORKFLOWS}", file=sys.stderr)
        return 2
    problems = []
    pins = {}
    for path in files:
        found = check_file(path)
        problems += found
        shown = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
        print(f"{'FAIL' if found else 'ok  '} {shown}")
        for pin in axe_pins(path.read_text(encoding="utf-8")):
            pins.setdefault(pin, []).append(shown)
    if len(pins) > 1:
        problems.append("the workflows fetch different axe-core: " + "; ".join(
            f"{', '.join(sorted(set(where)))} {version} {(sha or 'no SHA-512')[:12]}"
            for (version, sha), where in sorted(pins.items(), key=lambda kv: str(kv[0]))))
    for problem in problems:
        print(f"  {problem}")
    print(f"\n{len(files)} workflow(s), {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
