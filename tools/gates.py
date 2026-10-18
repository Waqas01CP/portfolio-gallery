"""The repository gates (ADR-0008). Called by the thin hooks in .githooks/.

  python tools/gates.py pre-commit    gates A, B and C, with D throughout
  python tools/gates.py pre-push      gate E, reading git's pre-push input

Each gate, what it blocks, and the case built to defeat it (the proofs are
in the session log that built them; docs/reference/standing-checks.md):

  A  Never commit, pre-commit. Refuses CHAT_STATE.md and
     CAPABILITIES-PRIVATE.md, the architecture chat's own files, at any
     path and in any letter case; anything
     under briefs/ but briefs/README.md; any staged path matching a pattern
     in tools/never-commit.txt; and any staged text file holding a
     drive-letter absolute path or a climb out of the repository. Also
     refuses, in any staged text file and in the commit's author and
     committer, each private pattern in .git/info/never-commit, a file in
     git's own folder that is never committed: so a maintainer can keep his
     name, his email or a private folder name out of the history without
     writing them into this public repository (format below). Prints the
     file, line and matched text, so a false positive can be seen for what
     it is. Defeated by staging CHAT_STATE.md with -f, and
     CAPABILITIES-PRIVATE.md with -f at the root and as
     docs/capabilities-private.md, a planted absolute
     path, a planted private pattern, a commit under a refused identity,
     an allowed text in a file it is not allowed in, and a refused name
     beside an allowed text that holds it. Controls: prose naming a folder
     passes; an allowed text in its own file passes.
  B  The staged tree builds, pre-commit. Copies the staged tree to a
     temporary folder and runs, there: the workflows' job conditions
     (tools/check_workflows.py); every design checked; the site built,
     its files checked and its content traced; the gallery built and its
     files checked (tools/ci.py build). Building the staged tree, not the
     working tree, judges what is about to be committed; untracked files
     on disk play no part. Defeated by a staged design with an @import,
     by content whose cut is not a cut, and by a deploy job with no if:.
  C  Map, pre-commit. Runs tools/generate_map.py --check against the
     staged files: refuses a stale map, and a staged Markdown header GitHub
     would refuse to read. Defeated by a new Markdown file committed without
     regenerating the map, and by a description holding an unquoted ": ".
  D  Missing tool, every gate. A missing git, build.py, tools/ci.py or map
     generator is a refusal naming what is missing, never a skip. The
     hooks apply the same rule to the venv interpreter and to this file.
     Defeated by renaming the map generator, and by moving the venv.
  E  STATE.md moved, pre-push. Across every commit being pushed, if any
     touches an implementation path and none touches STATE.md, refuses.
     Pre-push, so a series of commits with the bookkeeping last passes.
     Defeated by pushing a tools/ change with no STATE.md change. Control:
     several commits where only the last touches STATE.md pass.

.git/info/never-commit, one private pattern per line, # for comments:

  some text             refused anywhere, matched ignoring case
  some text<TAB>@allow LICENSE README.md
                        refused except in the files named; in those
                        files it is taken out of each line before the
                        other patterns are matched, so an allowed address
                        does not count as the name it holds, and the name
                        on its own is still refused there
  sha256:<hex>:<n>      refused wherever the SHA-256 of a lower-cased
                        window of n characters equals <hex>, so the text
                        itself need not be written down even there

Standard library only.
"""

from __future__ import annotations

import fnmatch
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Gate A. Every pattern is written so this file's own source cannot match
# it: a drive letter is followed by a character class, never by a literal
# separator, and a climb is written with escaped dots.
DRIVE_PATH = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")
CLIMB = re.compile(r"(?:\.\.[\\/]){2,}")
NEVER_COMMIT_LIST = "tools/never-commit.txt"

# Gate E.
IMPLEMENTATION_FILES = {"build.py", "requirements.txt"}
IMPLEMENTATION_DIRS = ("src/", "tools/", "content/", ".githooks/", ".github/")


class MissingTool(Exception):
    """Gate D: a tool a gate needs is absent. Always a refusal."""


def git(*args: str) -> bytes:
    try:
        result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    except FileNotFoundError:
        raise MissingTool("git is not on the PATH") from None
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: "
                           f"{result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout


def zsplit(output: bytes) -> list[str]:
    return [p for p in output.decode("utf-8").split("\0") if p]


def staged_blob(path: str) -> bytes:
    return git("cat-file", "blob", f":{path}")


# Gate A: never commit.

def path_patterns() -> list[str]:
    """tools/never-commit.txt as staged, or as on disk when not yet staged."""
    try:
        text = staged_blob(NEVER_COMMIT_LIST).decode("utf-8")
    except RuntimeError:
        file = ROOT / NEVER_COMMIT_LIST
        if not file.is_file():
            raise MissingTool(NEVER_COMMIT_LIST) from None
        text = file.read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines()
            if line.strip() and not line.lstrip().startswith("#")]


def private_patterns() -> list[tuple[str, set[str]]]:
    """(pattern, files where it is allowed) from .git/info/never-commit."""
    location = git("rev-parse", "--git-path", "info/never-commit").decode().strip()
    file = Path(location) if Path(location).is_absolute() else ROOT / location
    if not file.is_file():
        return []
    patterns = []
    for line in file.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        text, _, allow = line.partition("\t")
        allowed = set(allow.split()[1:]) if allow.strip().startswith("@allow") else set()
        patterns.append((text.strip(), allowed))
    return patterns


def private_hits(line: str, patterns: list[tuple[str, set[str]]], path: str | None) -> list[str]:
    hits, lowered = [], line.lower()
    # Text allowed in this file is taken out first, so it cannot count as
    # another pattern it holds; the same length keeps every other match.
    for pattern, allowed in patterns:
        if path is not None and path in allowed and not pattern.startswith("sha256:"):
            lowered = lowered.replace(pattern.lower(), "\0" * len(pattern))
    for pattern, allowed in patterns:
        if path is not None and path in allowed:
            continue
        digest = re.fullmatch(r"sha256:([0-9a-f]{64}):(\d+)", pattern)
        if digest:
            size = int(digest[2])
            for i in range(len(lowered) - size + 1):
                if hashlib.sha256(lowered[i:i + size].encode("utf-8")).hexdigest() == digest[1]:
                    hits.append("a private pattern (by digest)")
                    break
        elif pattern.lower() in lowered:
            hits.append("a private pattern from .git/info/never-commit")
    return hits


def never_commit_reason(path: str, globs: list[str]) -> str | None:
    lowered = path.lower()
    if lowered.rsplit("/", 1)[-1] == "chat_state.md":
        return "CHAT_STATE.md is the architecture chat's ledger and is never committed"
    if lowered.rsplit("/", 1)[-1] == "capabilities-private.md":
        return ("CAPABILITIES-PRIVATE.md is the architecture chat's lane of CAPABILITIES.md "
                "and is never committed: every copy of the template inherits what is")
    if lowered.startswith("briefs/") and lowered != "briefs/readme.md":
        return "briefs are working space and are never committed (briefs/README.md)"
    for glob in globs:
        if fnmatch.fnmatchcase(path, glob):
            return f"matches '{glob}' in {NEVER_COMMIT_LIST}"
    return None


def pointers_in(path: str, text: str, patterns) -> list[str]:
    depth = path.count("/")
    found = []
    for number, line in enumerate(text.splitlines(), start=1):
        hits = [("a drive-letter absolute path", m.group(0)) for m in DRIVE_PATH.finditer(line)]
        # A climb of two or more levels leaves the repository only if it
        # rises above the root from this file's folder.
        hits += [("a climb out of the repository", m.group(0)) for m in CLIMB.finditer(line)
                 if m.group(0).count("..") > depth]
        hits += [(label, "(not shown)") for label in private_hits(line, patterns, path)]
        for label, matched in hits:
            shown = line.strip() if matched != "(not shown)" else "(the line is not shown)"
            shown = shown if len(shown) <= 120 else shown[:117] + "..."
            found.append(f"{path}, line {number}: {label}: {matched}\n      in: {shown}")
    return found


def gate_a(staged: list[str]) -> list[str]:
    globs, patterns = path_patterns(), private_patterns()
    refusals = []
    for variable in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT"):
        ident = git("var", variable).decode("utf-8", "replace")
        if private_hits(ident, patterns, None):
            refusals.append(f"A  the commit's {variable.split('_')[1].lower()} identity holds a "
                            f"private pattern; set user.name and user.email for this repository")
    for path in staged:
        reason = never_commit_reason(path, globs)
        if reason:
            refusals.append(f"A  {path}: {reason}")
            continue
        data = staged_blob(path)
        if b"\0" in data[:8000]:
            continue  # binary: no text path can be read from it
        refusals += [f"A  {hit}" for hit in pointers_in(path, data.decode("utf-8", "replace"), patterns)]
    return refusals


# Gate B: the staged tree builds and passes its file checks.

def gate_b() -> list[str]:
    with tempfile.TemporaryDirectory(prefix="gate-b-") as tmp:
        tree = Path(tmp) / "tree"
        git("checkout-index", "--all", "--force", f"--prefix={tree.as_posix()}/")
        for required in ("build.py", "tools/ci.py", "tools/check_design.py", "tools/check_workflows.py"):
            if not (tree / required).is_file():
                raise MissingTool(f"{required} is not in the staged tree")
        steps = [["tools/check_workflows.py"],
                 ["tools/check_design.py"],
                 ["tools/ci.py", "build", "--mode", "site", "--out", str(Path(tmp) / "site")],
                 ["tools/ci.py", "build", "--mode", "gallery", "--out", str(Path(tmp) / "gallery")]]
        for step in steps:
            result = subprocess.run([sys.executable, *step], cwd=tree, capture_output=True, text=True)
            if result.returncode != 0:
                output = (result.stdout + result.stderr).strip().splitlines()
                tail = "\n      ".join(output[-25:])
                return [f"B  the staged tree fails {' '.join(step[:2])}:\n      {tail}"]
    return []


# Gate C: the map is current against the staged files.

def gate_c() -> list[str]:
    generator = ROOT / "tools" / "generate_map.py"
    if not generator.is_file():
        raise MissingTool("tools/generate_map.py")
    result = subprocess.run([sys.executable, str(generator), "--check"],
                            cwd=ROOT, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    if result.returncode == 0:
        return []
    if result.returncode == 2:
        return [f"C  {output}"]
    return [f"C  the map check failed (exit {result.returncode}), which is not a "
            f"staleness report. Fix the cause:\n      {output}"]


def pre_commit() -> int:
    refusals = []
    try:
        staged = zsplit(git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMRT"))
        refusals += gate_a(staged)
        refusals += gate_b()
        refusals += gate_c()
    except MissingTool as error:
        refusals.append(f"D  missing tool: {error}")
    except RuntimeError as error:
        refusals.append(f"   {error}")
    if refusals:
        print("COMMIT REFUSED by the repository gates (ADR-0008):", file=sys.stderr)
        for refusal in refusals:
            print(f"  {refusal}", file=sys.stderr)
        return 1
    print("gates A, B, C passed", file=sys.stderr)
    return 0


# Gate E: STATE.md moved, across the whole range being pushed.

def touched(commit: str) -> list[str]:
    parents = git("rev-list", "--parents", "-n", "1", commit).decode().split()[1:]
    if parents:
        return zsplit(git("diff", "--name-only", "-z", parents[0], commit))
    return zsplit(git("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "-z", commit))


def is_implementation(path: str) -> bool:
    return path in IMPLEMENTATION_FILES or path.startswith(IMPLEMENTATION_DIRS)


def pre_push(stdin: str) -> int:
    refusals = []
    try:
        for line in stdin.splitlines():
            local_ref, local_sha, remote_ref, remote_sha = line.split()
            if set(local_sha) == {"0"}:
                continue  # deleting a remote ref sends no commits
            if set(remote_sha) == {"0"}:
                range_args = [local_sha, "--not", "--remotes"]
            else:
                if subprocess.run(["git", "cat-file", "-e", f"{remote_sha}^{{commit}}"],
                                  cwd=ROOT, capture_output=True).returncode != 0:
                    refusals.append(f"E  {remote_ref}: the remote is at {remote_sha[:7]}, which this "
                                    f"clone does not have, so the range cannot be computed. Fetch first")
                    continue
                range_args = [f"{remote_sha}..{local_sha}"]
            commits = git("rev-list", *range_args).decode().split()
            by_commit = {c: touched(c) for c in commits}
            if any("STATE.md" in paths for paths in by_commit.values()):
                continue
            work = []
            for commit, paths in by_commit.items():
                hits = [p for p in paths if is_implementation(p)]
                if hits:
                    subject = git("log", "-1", "--format=%s", commit).decode().strip()
                    work.append(f"{commit[:7]} {subject}: {', '.join(hits[:5])}")
            if work:
                refusals.append(
                    f"E  {remote_ref}: implementation work is being pushed and no commit in the "
                    f"range touches STATE.md. Update it in a commit on this branch (the last of "
                    f"the series is fine) and push again. The work:\n      " + "\n      ".join(work))
    except MissingTool as error:
        refusals.append(f"D  missing tool: {error}")
    except RuntimeError as error:
        refusals.append(f"   {error}")
    if refusals:
        print("PUSH REFUSED by the repository gates (ADR-0008):", file=sys.stderr)
        for refusal in refusals:
            print(f"  {refusal}", file=sys.stderr)
        return 1
    print("gate E passed", file=sys.stderr)
    return 0


def main(argv: list[str]) -> int:
    if argv[:1] == ["pre-commit"]:
        return pre_commit()
    if argv[:1] == ["pre-push"]:
        return pre_push(sys.stdin.read())
    print("usage: gates.py pre-commit | pre-push <remote> <url>", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
