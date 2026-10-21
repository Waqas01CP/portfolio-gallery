---
status: accepted
topic: process
description: "The README routes every kind of visitor to their path and carries a self-contained prompt a person gives their own AI assistant; tools/check_prompt.py holds the prompt to the repository it restates. AGENTS.md is proposed, not added. Read before changing the README's table or prompt, the issue forms, or what an AI arriving at the repository is told."
date: 2026-10-21
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0017: Documents a person and their AI can both follow

## Context and Problem Statement

Many visitors now arrive through an AI tool, which has to guess what to
read and when; a person must still understand the project and know what
to do. Before this record the README covered using the template and
contributing, but not reporting a problem, asking a question or asking
for a showcase entry's removal, and had nothing for an AI. CLAUDE.md, the
maintainer's working rules, is what Claude Code loads for anyone who
clones the repository. How should a person, and the AI they bring, find
their way?

## Decision Drivers

- The owner's decisions of 2026-10-21, through the portfolio architecture
  chat's Brief 11: documents a person and an AI can both follow, for this
  repository and his site's; a self-contained, comprehensive prompt for
  an AI in the README, which asks the person what they want to do and
  guides them; pictures that make the README better.
- The prompt restates the repository, so it must fail a check when the
  two disagree (Brief 11), as every check here is proven by the case
  built to defeat it (CLAUDE.md, Verification).
- Safety: the AI explains each step first, never handles a secret, and
  leaves every action on GitHub to the person; everything merged stays in
  the public history.
- A person without an AI follows the same paths in the documents.

## Assumptions

- A1. AGENTS.md is a documented convention for coding agents. **Sourced**,
  each read 2026-10-21, none dated on the page: agents.md ("a simple, open
  format for guiding coding agents", stewarded by the Agentic AI
  Foundation under the Linux Foundation, listing Codex, Cursor, Gemini
  CLI, GitHub Copilot's coding agent and others); OpenAI's Codex
  documentation (reads AGENTS.md from the project root down, at most
  32 KiB by default); Cursor's documentation ("Cursor supports AGENTS.md
  in the project root and subdirectories"); GitHub's Copilot support
  table (AGENTS.md read by the cloud agent, code review, VS Code chat and
  the CLI; CLAUDE.md and GEMINI.md as alternatives).
- A2. Claude Code reads AGENTS.md only when no CLAUDE.md is present, and
  only CLAUDE.md when both are, unless its setting changes that.
  **Sourced**: Claude Code's documentation, "How Claude remembers your
  project", read 2026-10-21 (AGENTS.md read directly from v2.1.277).
- A3. Gemini CLI reads GEMINI.md by default and AGENTS.md when its
  `context.fileName` setting names it. **Sourced**: its documentation,
  last updated 2026-06-18, which also says Gemini CLI was replaced by
  Antigravity CLI that day.
- A4. llms.txt is a proposal for websites, not repositories. **Sourced**:
  llmstxt.org, by Jeremy Howard, 2024-09-03, modified 2026-08-10.
- A5. GitHub renders a README's fenced block inside `<details>` with its
  own copy button, and proxies images from another site. **Measured**
  2026-10-22: GitHub's Markdown API rendered the README's prompt as a
  `<pre lang="text">` inside the `<details>`, and each picture through its
  image proxy, which answered 200 with the WebP; the copy button is added
  by GitHub's page, not the API, so it shows only on the branch.
- A6. A chat assistant given a repository's address reads its README
  first, if it reads anything. **Inferred**; it is why the prompt is
  self-contained rather than a pointer.

## Considered Options

- The README routes each visitor, and carries the prompt, checked against
  the repository
- An AGENTS.md at the root, for coding agents
- A prompt in a file of its own, linked from the README
- llms.txt

## Decision Outcome

Chosen option: "The README routes each visitor, and carries the prompt,
checked against the repository".

We will open the README with a table, "What do you want to do?", naming
the start of each path: use the template, add a design, add a site to
the showcase, report a problem, remove or report a showcase entry, ask a
question, report a security problem, have an AI guide you, maintain the
repository.
We will give each reporting path a form: Bug and Design proposal as
before, and, new, Showcase entry (removal, impersonation, an entry gone
bad) and Question; blank issues stay off.
We will carry in the README, in a collapsible section's fenced block, a
prompt addressed to the person's AI assistant that holds everything it
needs and asks what they want to do; and check it with
tools/check_prompt.py, in tools/ci.py checks and gate B, against the
sources of every path, fact and command it states.
We will open CLAUDE.md with a line telling any other AI that it is the
maintainer's rules and the README is its start.
We will show pictures the deploy keeps current, by their live addresses.
We will propose AGENTS.md, not add it.

### Consequences

- Good, because every kind of visitor, and any AI they bring, has one
  place to start, and a person without an AI the same paths.
- Good, because the prompt cannot drift from the repository unnoticed: a
  path, a limit, a field, a command or a form that changes on either side
  fails the check, and so does a fact reworded out of its sight.
- Bad, because the prompt is long, and the check's patterns follow its
  wording: changing a sentence that states a fact means changing the
  check with it.
- Bad, because a coding agent that reads AGENTS.md and not the README
  gets nothing new until AGENTS.md is decided.
- Neutral, because a copy of the template keeps none of this: its README
  is copy-README.md, and the cleanup removes the forms and the check.

### Confirmation

tools/check_prompt.py on the README; its defeat cases in
tools/prove_checks.py: a path that does not exist, the screenshot cap
stated wrong, the shape limit changed at its source, the scope marker
changed at its source, an issue form it does not name, a command in no
guide, a safety rule taken out, and a fact reworded out of its sight.

## Pros and Cons of the Options

### The README routes each visitor, and carries the prompt, checked

- Good, because the README is what a person and a chat assistant meet
  first (A6), and GitHub's copy button works on the block (A5).
- Bad, because the README grows by about 220 lines, inside a closed
  section.

### An AGENTS.md at the root

- Good, because coding agents read it by convention (A1).
- Bad, because Claude Code would still read CLAUDE.md here instead (A2),
  and a copy of the template would need its own; proposed for the owner,
  with the cleanup's handling, rather than added.

### A prompt in a file of its own

- Good, because the README stays short.
- Bad, because a person must find a second file, and an AI given the
  README must fetch it, which the owner's "self contained" rules out.

### llms.txt

- Bad, because it is a proposal for websites (A4), not a repository's
  entry point.

## More Information

The prompt's sources: tools/check_showcase.py, build.py,
tools/check_design.py, content/config.json, tools/scope_check.py,
.github/pull_request_template.md, .github/ISSUE_TEMPLATE/,
CONTRIBUTING.md, docs/how-to/add-a-design.md and
docs/reference/commands.md. The owner's words, 2026-10-21: "a self
contained, extremely comprehensive detailed prompt which tells everything
about the repo to the AI and asks users what do you want to do with this
repo".

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-21 | Written by the implementing seat, accepted as the owner's decision through the chat's Brief 11; the prompt's form, the check and the pictures are the seat's design within it. | Brief 11. |
