---
type: how-to
description: A user's journey, click by click. Copy the repository, turn on Pages, write your content in the browser, pick a design, and publish; then the address and the checks. Read to make your own site.
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
"Checks" and "Deploy" started by themselves in a test copy on 2026-10-18,
and "Template cleanup" runs beside them. "Deploy" fails at its last job,
because Pages is not set up yet; step 3 fixes it.

## 2. Make it yours

Your copy starts with portfolio-gallery's own project files: its decision
records, logs, contribution rules and tools, and two files that name the
project's owner. The "Template cleanup" workflow removes them once, by
itself, and commits: in your history you see "Make it yours: remove
portfolio-gallery's project files", by github-actions. It also puts a
short README of your own in place of the project's. It never runs in
portfolio-gallery itself or in a fork, and its commit starts no other run;
your next commit builds and checks the cleaned files.

If it did not run, as when Actions are turned off, delete these yourself,
the first two above all:

1. `CODE_OF_CONDUCT.md`: it names the project owner's address, so reports
   about your site would reach him.
2. `.github/CODEOWNERS`: it names him as the owner of your files.
3. The project's records and rules: `docs/decisions/`, `docs/deferred/`,
   `logs/`, `briefs/`, `STATE.md`, `CAPABILITIES.md`, `MAP.md`,
   `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`,
   `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`.
4. Its own guides: `docs/setup-on-github.md`,
   `docs/how-to/add-a-design.md`, and in `docs/reference/`:
   `commands.md`, `completed.md`, `provenance.md`, `standing-checks.md`.
5. Its own tools: `.githooks/`, and in `tools/`: `gates.py`,
   `never-commit.txt`, `generate_map.py`, `prove_checks.py`,
   `scope_check.py`, `check_template_cleanup.py`.
6. `.github/template-cleanup/`, the cleanup's own list and script.

Then replace `README.md` with your own. The full list, with why each goes,
is `.github/template-cleanup/remove.txt` in portfolio-gallery.

Two workflow files may stay even after the cleanup:
`.github/workflows/scope.yml` and `.github/workflows/template-cleanup.yml`.
A workflow's own token may not be allowed to change workflow files, so
the cleanup tries to delete them in a commit of its own and says in its
run what GitHub answered. Each is written to run nothing in a copy;
delete them by hand if you like. Keep `LICENSE`: the MIT licence asks that
its notice stays with every copy.

## 3. Turn on GitHub Pages

1. In your repository, click **Settings**, then **Pages** in the left
   sidebar.
2. Under "Build and deployment", set **Source** to **GitHub Actions**.

Nothing else on that page needs changing.

## 4. Write your content

Everything you write is in the `content/` folder. Click a file, then the
pencil icon to edit it in the browser. Each file's fields are explained
in docs/reference/content.md.

1. **`site.json`**: your name, headline, location, summary, skills and how
   to reach you. Replace every value about Alex Example.
2. **`items.json`**: your projects, roles, degree and certificates, one
   entry each. Keep the shape of the sample entries. Every project needs a
   `layer1`, a short fact that is a cut of one of its bullets: the same
   words in the same order, some left out.
3. **`cv.md`**: your CV in the Markdown shape of docs/reference/cv-format.md.
   The checks then confirm that every sentence on your site comes from it.
   Anything in this file is public; if you would rather not publish your
   CV, set `"content_trace": false` in `config.json` and delete `cv.md`.
4. **`config.json`**: the design, by its folder name in `designs/`, such as
   `"design": "plain"`; every design is in the gallery. Also the PDF to
   offer as "Download CV" (`"cv_pdf": ""` for none; upload yours to
   `content/` and name it here exactly, letter for letter), and whether the
   footer says "Built with portfolio-gallery" (`"credit"`).

Commit each change with **Commit changes**.

## 5. Watch it publish

Open the **Actions** tab. Each commit to `main` starts a "Deploy" run:
build, then assemble, then deploy. When all three are green, your site is
live at the address from step 1, and the run's "deploy" job links to it.
A fourth job, "shots", shows as skipped (a grey circle with a line
through it): it takes the gallery's previews and runs only in this
project's own repository.

If the build fails, open the run and the failed step: it names every
problem, such as an item missing a field, a `layer1` that is not a cut, or
a sentence the content trace could not find in your CV. Fix it in the file
it names and commit again. A failed build publishes nothing; your previous
site stays up.

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
- **Credit**: the footer link is on by default. Turning it off is your
  choice; a mention in your repository's README is appreciated.
