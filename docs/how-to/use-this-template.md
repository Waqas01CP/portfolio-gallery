---
type: how-to
description: A user's journey, click by click. Copy the repository, turn on Pages, write your content in the browser, pick a design, and publish; then the address, the checks, and building on your own computer if you like. Read to make your own site.
status: current
---

# Make your own site from this template

You need a GitHub account and nothing else. About fifteen minutes, most of
it writing your content.

## 1. Copy the repository

**Use "Use this template", not "Fork".** Both copy the files; the
difference is what you get with them (GitHub Docs, "Creating a repository
from a template", read 2026-10-12):

- A copy from a template "starts with a single commit": your history is
  your own.
- "Commits to a fork don't appear in your contributions graph, while
  commits to a repository created from a template do appear": the work you
  put into your site shows on your profile.
- A fork's workflows do not run until you enable them: "Workflows don't
  run in forked repositories by default. You must enable GitHub Actions in
  the Actions tab of the forked repository" (GitHub Docs, "Events that
  trigger workflows"). A template copy has no such step.

Fork only to contribute a design
([how to add a design](https://github.com/Waqas01CP/portfolio-gallery/blob/main/docs/how-to/add-a-design.md)).

1. On the repository's page, click **Use this template**, then **Create a
   new repository**.
2. Choose the name:
   - `<your-username>.github.io` (exactly your username) for
     `https://<your-username>.github.io/`;
   - anything else, such as `portfolio`, for
     `https://<your-username>.github.io/portfolio/`.
3. Leave it **Public**: GitHub Pages is free for public repositories.
4. Click **Create repository**. You see your new repository with all the
   files, and one commit.

GitHub runs your copy's workflows for that first commit on its own:
"Checks", "Deploy" and "Template cleanup" started by themselves in test
copies on 2026-10-18. "Deploy" builds and checks your site but publishes
nothing yet, because Pages is not set up: the run ends with the notice
"Turn on GitHub Pages to publish your site", with no red. Step 3 fixes it.

## 2. Make it yours

The "Template cleanup" workflow removes portfolio-gallery's own project
files from your copy, once, by itself: in your history you see "Make it
yours: remove portfolio-gallery's project files" by github-actions, then
a second commit removing the project's own workflows, the cleanup's among
them. Your README becomes a short one of your own, with a prompt you can
give an AI assistant to guide you, and AGENTS.md, the file coding agents
read first, points them to it. Those commits start no
other run; your next commit builds and checks the cleaned files.

If those commits are not there, as when Actions are turned off, delete
these yourself, the first two above all:

1. `CODE_OF_CONDUCT.md`: its contact address is the project's, so reports
   about your site would go there instead of to you.
2. `.github/CODEOWNERS`: it makes the project's account the owner of
   every file in your repository.
3. `showcase/`, the gallery's showcase of other people's sites, and the
   `"in_use"` line in each `designs/*/design.json`, a link to a design
   author's own site.
4. The project's records and rules: `docs/decisions/`, `docs/deferred/`,
   `logs/`, `STATE.md`, `CAPABILITIES.md`, `MAP.md`,
   `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`,
   `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`.
5. Its own guides: `docs/setup-on-github.md`,
   `docs/how-to/add-a-design.md`, `docs/how-to/add-to-the-showcase.md`,
   and in `docs/reference/`: `commands.md`, `completed.md`,
   `provenance.md`, `standing-checks.md`.
6. Its own tools: `.githooks/`, and in `tools/`: `gates.py`,
   `never-commit.txt`, `generate_map.py`, `prove_checks.py`,
   `scope_check.py`, `check_showcase.py`, `check_prompt.py`,
   `check_template_cleanup.py`.
7. The cleanup itself: first copy its `copy-README.md` over `README.md`
   and its `copy-AGENTS.md` over `AGENTS.md`, your copy's own, which
   point you and any AI assistant to the right files; then delete
   `.github/template-cleanup/`, and the project's own workflows,
   `.github/workflows/scope.yml`, `.github/workflows/showcase-links.yml`,
   `.github/workflows/checks-weekly.yml` and
   `.github/workflows/template-cleanup.yml`.

Each path, with why it goes, is listed in
`.github/template-cleanup/remove.txt`. Keep `LICENSE`: the MIT
licence asks that its notice stays with every copy.

## 3. Turn on GitHub Pages

1. In your repository, click **Settings**, then **Pages** in the left
   sidebar.
2. Under "Build and deployment", set **Source** to **GitHub Actions**.
   Nothing else on that page needs changing.
3. Click **Actions**, then **Deploy** in the left list, then **Run
   workflow**, and the green **Run workflow** button. Or commit any
   change: every commit publishes.

GitHub Actions cannot turn Pages on by itself: the action that could
needs a token other than the run's own (actions/configure-pages, its
`enablement` input), and one setting is less to ask than a token.

## 4. Write your content

Everything you write is in the `content/` folder. Click a file, then the
pencil icon to edit it in the browser. Each file's fields are explained
in docs/reference/content.md.

**Your CV comes first, and the page must match it.** The checks trace
every sentence on your site to `cv.md`, and every line of `cv.md` to your
site. So every fact you write in `site.json` or `items.json` must also be
in `cv.md`, word for word or cut from it, and a change to one needs the
same change in the other. Until they match, the build fails and names the
line of `cv.md` to look at. Write `cv.md` first, then take the other
files' text from it. If you would rather not publish your CV, set
`"content_trace": false` in `config.json` and delete `cv.md`; nothing is
traced then.

1. **`cv.md`**: your CV in the Markdown shape of docs/reference/cv-format.md.
   Anything in this file is public.
2. **`site.json`**: your name, headline, location, summary, skills and how
   to reach you. Replace every value about Alex Example.
3. **`items.json`**: your projects, roles, degree and certificates, one
   entry each. Keep the shape of the sample entries. Every project needs a
   `layer1`, a short fact that is a cut of one of its bullets: the same
   words in the same order, some left out.
4. **`config.json`**: the design, by its folder name in `designs/`, such as
   `"design": "plain"`; every design is in the gallery. Also the PDF to
   offer as "Download CV" (`"cv_pdf": ""` for none; upload yours to
   `content/` and name it here exactly, letter for letter), and whether the
   footer carries the credit line (`"credit"`), "Built with
   portfolio-gallery", with the design and its author.

Commit each change with **Commit changes**. The browser commits one file
at a time, so when a fact changes in two files, the run for the first
commit fails and the second goes green; a failed build publishes nothing.

## 5. Watch it publish

Open the **Actions** tab. Each commit to `main` starts a "Deploy" run:
build, then assemble, then deploy, with "pages" beside them asking GitHub
whether Pages is on. When all four are green, your site is live at the
address from step 1, and the run's "deploy" job links to it. If "deploy"
shows as skipped and the run's summary says "Turn on GitHub Pages to
publish your site", Pages is still off: step 3. A fifth job, "shots",
shows as skipped too (a grey circle with a line through it): it takes the
gallery's previews and runs only in this project's own repository.

If the build fails, open the run and the failed step: it names every
problem, such as an item missing a field, a `layer1` that is not a cut, or
a sentence the content trace could not find in your CV, with the nearest
line of `cv.md` and what to do. Fix it in the file it names and commit
again. A failed build publishes nothing; your previous site stays up.

The "Checks" run, beside it, runs the accessibility checks on your content
in every design. It does not stop your site from publishing; read it to
see what a design does with your content.

## 6. Later

- **Another design**: change `"design"` in `config.json` and commit.
- **The address `https://<your-username>.github.io/`**: rename the
  repository to `<your-username>.github.io` under Settings, General. Every
  link in the site is relative to its page, so nothing else changes
  (ADR-0007).
- **Engine updates**: a template copy does not follow this repository. To
  take an update, copy the changed engine files (`build.py`, `src/`,
  `tools/`, `designs/`, `.github/workflows/`) into your repository; your
  `content/` is never touched by an update.
- **Credit**: the footer's line, "Built with portfolio-gallery, design
  Default by Waqas01CP" for the default design, names this project and
  the design's author, each linked, and is on by default. It is how the
  people who made your site get found, so please keep it if you can.
  Turning it off with `"credit": false` is your choice: the MIT licence
  asks only that `LICENSE` stays. A mention in your repository's README is
  appreciated either way.
- **Your site in the gallery**: once it is live, you can add it to the
  gallery's showcase (https://github.com/Waqas01CP/portfolio-gallery/blob/main/docs/how-to/add-to-the-showcase.md).

## 7. Build on your own computer, if you like

Nothing here is needed to publish: GitHub builds your site. To see a
change before you commit it, you need Python 3.12 or later and a clone of
your repository. From its folder:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt      Windows
.venv/bin/python -m pip install -r requirements.txt          macOS, Linux
```

Then, with the venv's Python (`.venv\Scripts\python` on Windows,
`.venv/bin/python` elsewhere):

```
python tools/ci.py build --mode site
python -m http.server --directory _site 8000
```

The first builds your site into `_site/`, checks its files and runs the
content trace, as the Deploy run's build does, and names every problem
the same way. The second serves it: open http://127.0.0.1:8000/ in your
browser, and stop it with Ctrl+C. Git ignores `_site/` and `.venv/`.
