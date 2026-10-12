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

Fork only to contribute a design (docs/how-to/add-a-design.md).

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

The **Actions** tab may already show a failed "Deploy" run: GitHub ran it
for that first commit, before Pages was set up. That is expected; the next
step fixes it. (Not verified: whether GitHub runs workflows for the first
commit of a template copy.)

## 2. Turn on GitHub Pages

1. In your repository, click **Settings**, then **Pages** in the left
   sidebar.
2. Under "Build and deployment", set **Source** to **GitHub Actions**.

Nothing else on that page needs changing.

## 3. Write your content

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

## 4. Watch it publish

Open the **Actions** tab. Each commit to `main` starts a "Deploy" run:
build, then assemble, then deploy. When all three are green, your site is
live at the address from step 1, and the run's "deploy" job links to it.

If the build fails, open the run and the failed step: it names every
problem, such as an item missing a field, a `layer1` that is not a cut, or
a sentence the content trace could not find in your CV. Fix it in the file
it names and commit again. A failed build publishes nothing; your previous
site stays up.

The "Checks" run, beside it, runs the accessibility checks on your content
in every design. It does not stop your site from publishing; read it to
see what a design does with your content.

## 5. Later

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
