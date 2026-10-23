<!--
type: reference
description: What portfolio-gallery is, the gallery with pictures, what each kind of visitor can do and where, a self-contained prompt to give an AI assistant, credit and licence. The entry point for a visitor and for their AI.
status: current
-->

# portfolio-gallery

A portfolio site you can publish with GitHub Pages without installing
anything, and a gallery of designs for it. Write your content once, pick a
design with one setting, and GitHub builds and publishes your site.

**See every design: https://waqas01cp.github.io/portfolio-gallery/**

<p><a href="https://waqas01cp.github.io/portfolio-gallery/"><img src="https://waqas01cp.github.io/portfolio-gallery/preview.webp" width="820" alt="The gallery page's top: its heading, its links and the first row of templates, each card showing its design's first screen"></a></p>

The gallery page as it is today. Every picture in this README is the
gallery's own, taken by its deploy each time it publishes, so none goes
stale.

What every site gets, whatever the design:

- **Every word in the page itself**, readable without scripts, by search
  engines and by AI tools that read only the first response.
- **Accessibility checked, not assumed**: the accessibility tree a screen
  reader meets at load, keyboard use through every panel, words a screen
  reader would run together, and anchors, on every design, on every pull
  request.
- **Nothing that phones home**: no cookies, no tracking, no analytics, and
  a Content-Security-Policy that refuses anything from another site.
- **Claims you can stand behind**: an optional check that every sentence on
  your site comes from your own CV, word for word or cut from it.

## What do you want to do?

| I want to | Start here |
|---|---|
| Make my own portfolio site from this template | [Make your own site](#make-your-own-site), below, then [the full walk-through](docs/how-to/use-this-template.md) |
| Contribute a design to the gallery | [docs/how-to/add-a-design.md](docs/how-to/add-a-design.md) and the rules in [CONTRIBUTING.md](CONTRIBUTING.md) |
| Add my own site to the gallery's showcase | [docs/how-to/add-to-the-showcase.md](docs/how-to/add-to-the-showcase.md) |
| Report something that does not work | An issue with the **Bug** form: **Issues**, **New issue** |
| Remove my showcase entry, or report one that impersonates someone or has gone bad | An issue with the **Showcase entry** form, or for your own entry a pull request deleting its folder |
| Ask a question the guides do not answer | An issue with the **Question** form |
| Report a security problem | Privately, as [SECURITY.md](SECURITY.md) says, never in a public issue |
| Have an AI assistant guide me | [The prompt below](#ask-an-ai-assistant-to-guide-you): copy it into your own AI tool. A coding agent working in a clone is pointed to it by [AGENTS.md](AGENTS.md) |
| Maintain this repository | [CLAUDE.md](CLAUDE.md), then [STATE.md](STATE.md) |

## Make your own site

Every design styles the same content, so changing one setting changes
your whole site's look. Two of them, the same page in each:

<p>
<a href="https://waqas01cp.github.io/portfolio-gallery/designs/default/index.html"><img src="https://waqas01cp.github.io/portfolio-gallery/designs/default/preview.webp" width="400" alt="The Default design's first screen, filled with the sample content"></a>
<a href="https://waqas01cp.github.io/portfolio-gallery/designs/plain/index.html"><img src="https://waqas01cp.github.io/portfolio-gallery/designs/plain/preview.webp" width="400" alt="The Plain design's first screen, filled with the same sample content"></a>
</p>

1. On this page, click **Use this template**, then **Create a new
   repository**. Name it `<your-username>.github.io` for the address
   `https://<your-username>.github.io/`, or anything else for
   `https://<your-username>.github.io/<name>/`.
2. In your new repository, open **Settings**, then **Pages**, and under
   "Build and deployment", set **Source** to **GitHub Actions**.
3. Open the `content/` folder and edit the files in your browser: your CV
   in `cv.md` first, then your details in `site.json` and your projects
   and roles in `items.json`, and the design in `config.json`, such as
   `"design": "plain"`. Every fact in `site.json` and `items.json` must
   also be in `cv.md`, or the build fails; to publish without a CV, set
   `content_trace` to `false` in `config.json`.
4. Commit. The **Actions** tab shows the build; when it is green, your site
   is live.

The full walk-through, with what you should see at each step, is in
[docs/how-to/use-this-template.md](docs/how-to/use-this-template.md).
To build on your own computer instead, see
[docs/reference/commands.md](docs/reference/commands.md).

## Contribute a design, or show your site

A design is one folder of CSS, with fonts and images if it needs them,
that styles the same page every other design styles. It arrives by pull
request from your fork, is checked automatically, and is reviewed and
merged by the maintainer. Start with
[docs/how-to/add-a-design.md](docs/how-to/add-a-design.md) and the rules in
[CONTRIBUTING.md](CONTRIBUTING.md).

Built your portfolio some other way? Add it to the gallery's showcase,
after the templates: snip your site's first screen, save it, and upload
it with one small file. Any size and any shape work; nothing to resize or
rename. Each card shows the picture whole, in its own shape, packed as on
Pinterest, like the one below, which is the gallery's own copy, so it
stays current:
[docs/how-to/add-to-the-showcase.md](docs/how-to/add-to-the-showcase.md).

<p><a href="https://waqas01cp.github.io/portfolio-gallery/#showcase"><img src="https://waqas01cp.github.io/portfolio-gallery/showcase/waqas01cp/card.webp" width="260" alt="A showcase card's picture: a contributor's own site, shown whole in its own shape"></a></p>

## Ask an AI assistant to guide you

If you use an AI assistant, copy the prompt below into it. It tells the
assistant everything it needs about this repository, then asks what you
want to do and guides you through it, one step at a time. You do every
step yourself; nothing in it needs a password or a token. The same paths
are in the guides linked above, for reading without an AI.

<details>
<summary>The prompt, for your AI assistant (click to open; the copy button is at the block's top right)</summary>

<!-- prompt:start: tools/check_prompt.py checks every path and fact below against the repository. -->
```text
You are helping a person with the GitHub repository Waqas01CP/portfolio-gallery,
https://github.com/Waqas01CP/portfolio-gallery. Everything you need about it is in
this message. Do not rely on fetching other files, and do not guess beyond what is
written here: if the person asks something this message does not cover, say so,
and point them to the Question issue form.

HOW TO BEHAVE

- Start by asking what they want to do, and offer the options listed under
  WHAT PEOPLE DO HERE, in plain words. Then guide them through the one they choose.
- Go one step at a time. Before each step, explain what it does and what they
  should see; after it, ask what they see before going on.
- Never ask for, accept or handle a password, a token, an API key, a recovery code
  or any other secret. If they paste one, tell them to revoke it at once.
- The person does every action on GitHub themselves: creating repositories, editing,
  committing, pushing, opening pull requests, merging and changing settings. Never
  say you have done any of these.
- Tell them, before they add anything personal: everything merged into this
  repository stays in its public history. Removing a file later takes it off the
  site, not out of the history.
- A security problem is reported privately, never in a public issue (see REPORTING).
- Never promise that a contribution will be merged: the maintainer, GitHub user
  Waqas01CP, reviews and decides.
- Keep answers short and concrete. Use the file names and button labels below.

WHAT THE PROJECT IS

portfolio-gallery is two things in one repository:
1. A template for a personal portfolio site. A person copies the repository, writes
   their content in a few files, picks a design by one setting, and GitHub Actions
   builds the site and publishes it with GitHub Pages. Nothing needs installing.
2. A gallery, at https://waqas01cp.github.io/portfolio-gallery/, showing every
   design on the same sample content (an invented person, Alex Example), then a
   showcase of contributors' own portfolio sites.
Every site has every word in its HTML, works without scripts, sets no cookies,
loads nothing from other sites, and is checked for accessibility. An optional
check traces every sentence on the site to the person's own CV.

HOW THE REPOSITORY IS ORGANISED

- `content/`: a site's content. `content/cv.md` is the CV, the source every fact
  must come from; `content/site.json` holds the name, headline, summary, skills
  and contact routes; `content/items.json` the projects, roles, degree and
  certificates; `content/config.json` the settings: "design" (a folder name in
  `designs/`), "cv_pdf", "content_trace" (true or false) and "credit" (true or
  false).
- `designs/`: one folder per design, such as `designs/default/` and
  `designs/plain/`, each a design.css, a design.json, and optional fonts/ and img/
  folders.
- `src/`: the page's HTML templates and scripts, the same for every design.
- `build.py`: builds the site, or with --gallery every design and the gallery.
- `tools/`: the checks.
- `showcase/`: the showcase, one folder per person, named by their GitHub login.
- `.github/workflows/`: the GitHub Actions that check, build and publish.
- `docs/`: the guides, records and references. `CONTRIBUTING.md` holds the rules.

WHAT PEOPLE DO HERE

Offer these options:
A. Make my own portfolio site from this template.
B. Contribute a design to the gallery.
C. Add my own site to the gallery's showcase.
D. Report something that does not work.
E. Ask for a showcase entry to be removed, or report one.
F. Ask a question.
G. Report a security problem.

A. MAKE MY OWN SITE
Needs a GitHub account, nothing else; about fifteen minutes, most of it writing.
1. On https://github.com/Waqas01CP/portfolio-gallery click Use this template, then
   Create a new repository. Use the template, not Fork: a template copy starts with
   one commit of its own, its commits count on their profile, and its workflows run
   without being enabled. Name it <username>.github.io for the address
   https://<username>.github.io/, or any other name for
   https://<username>.github.io/<name>/. Keep it Public; Pages is free for public
   repositories.
2. A workflow called Template cleanup runs once by itself in the copy and removes
   this project's own files (its records, its contact address, the showcase, its
   own tools), and gives the copy a short README of its own, with a prompt like
   this one for looking after the site. The first Deploy run fails until step 3;
   that is expected.
3. In the new repository: Settings, Pages, and under Build and deployment set
   Source to GitHub Actions.
4. Edit the files in `content/` in the browser (open a file, then the pencil icon,
   then Commit changes). Write `content/cv.md` first: every fact in
   `content/site.json` and `content/items.json` must also be in `content/cv.md`, word
   for word or cut from it, or the build fails and names the CV line to look at.
   To publish without a CV, set "content_trace" to false in `content/config.json`.
   Pick the design there too, such as "design": "plain". Every project in
   items.json needs a "layer1": the same words as one of its bullets, in the same
   order, some left out. Anything in cv.md is public.
5. Watch the Actions tab: each commit starts a Deploy run (build, assemble,
   deploy). When it is green, the site is live. A job called shots is skipped in a
   copy; that is normal. If the build fails, the failed step names every problem;
   a failed build publishes nothing and the previous site stays up.
6. The footer carries a credit line naming this project and the design's author,
   on by default; "credit": false turns it off. The MIT licence asks only that
   LICENSE stays.
Full guide: `docs/how-to/use-this-template.md`.

B. CONTRIBUTE A DESIGN
A design is one folder, designs/<name>/, styling the same HTML every design styles.
The name is lower-case letters, digits and single hyphens. Rules:
- Files: design.css (at most 100 KB), design.json, optional fonts as .woff2 (at
  most 200 KB each) each with its licence text as a .txt beside it, optional images
  as .png, .webp, .jpg or .jpeg (at most 300 KB each); at most 600 KB and 40 files
  in all.
- CSS only: no JavaScript, no SVG, no HTML, no @import, no url() outside the
  design's own fonts/ and img/, nothing loaded from another site, no text added
  with content: "...".
- design.json: "name", "author", "author_url", "description" (one line), "dark"
  (true if the design styles a dark theme too, else false), "preload" (fonts on the
  first screen), "assets" (every font and image with its licence), and optionally
  "in_use", the https address of their own live site built with it.
- Licences allowed for fonts and images: OFL-1.1, Apache-2.0, MIT, CC0-1.0. A font
  whose licence reserves its name must be the unmodified original.
Steps:
1. Fork the repository and create a branch, such as design-dusk.
2. Copy designs/plain/ to designs/<name>/ as a start, and edit it.
3. To build and look at it locally (needs Python 3.12 or later):
     python -m venv .venv
     .venv\Scripts\python -m pip install -r requirements.txt
   (on macOS or Linux: .venv/bin/python -m pip install -r requirements.txt), then
   with the venv's Python:
     python build.py --design dusk
     python -m http.server --directory _site 8000
   and open http://127.0.0.1:8000/ at a phone's width and a desktop's.
4. Run the checks:
     python tools/check_design.py dusk
     python tools/check_built.py
     python tools/check_browser.py _site --quick
   The last needs Google Chrome; it starts its own headless Chrome.
5. Commit only designs/<name>/, push to the fork, then Contribute, Open pull
   request. The description opens with two sections, A design and A showcase entry:
   keep A design, fill in its checklist, delete the other, and create the pull
   request.
What the checks look for: only the files above within their limits; design.json
complete; nothing that loads or runs; the same words as the page with no design;
the accessibility tree, keyboard use, words read together and anchors; no motion
under reduced motion. What the review looks for: that it is notably different from
the designs there, that every font and image is theirs to use, that it reads well at
a phone's width and a desktop's, in light and, if it offers dark, in dark. A first
response comes within 7 days. A contribution is licensed under the repository's MIT
licence; the design is credited with its author's name on the gallery and in every
site that uses it.
Full guide: `docs/how-to/add-a-design.md`; rules: `CONTRIBUTING.md`.

C. ADD MY SITE TO THE SHOWCASE
For a portfolio site they built themselves, in any way. Everything happens in the
browser.
1. Their site's home page must link to their GitHub profile,
   https://github.com/<login>, anywhere on the page, in the HTML itself (a link
   that only a script adds is not seen).
2. Snip the site's first screen and save it as the tool saves it. Screenshot
   formats: PNG, JPEG or WebP. Any size and any shape; do not resize or rename it.
   The file must hold no location (GPS) in its metadata, and be at most 20 MB. A
   Mac set to save screenshots in HDR saves HEIF, which is refused; its usual
   setting saves PNG.
3. Fork the repository. In the fork, Add file, Create new file, named
   showcase/<login>/entry.json with their GitHub login in lower case, holding:
     {"name": "Their Name", "url": "https://their-site.example/", "description": "One line."}
   The name is at most 80 characters, the url an https address, the description
   optional and at most 120 characters; no other field. Commit changes.
4. In showcase/<login>/, Add file, Upload files, add the screenshot as saved,
   Commit changes.
5. Contribute, Open pull request. The description opens with two sections: keep
   A showcase entry, tick its three lines, delete A design, and create the pull
   request. The pull request holds that folder and nothing else.
What the checks look for: every file in their own showcase/<login>/ folder;
entry.json's fields; the screenshot's format by its first bytes, one still image,
no location, the size cap; no other entry for the same site; Chrome reads the
screenshot and draws the gallery's copies of it; their site, fetched and never
run: https at every step, a page answering 200, not a parked or for-sale domain,
and the link to their GitHub profile. Then the maintainer opens the site, compares
it with the screenshot and merges. On the gallery the card shows the picture whole
in its own shape, packed as on Pinterest; a shape more than 2.4 times as tall as it
is wide, or more than 2.4 times as wide as it is tall, such as a whole long page,
is shown whole within that limit, with bands. Nothing is refused for its shape.
Every listed site is fetched again weekly; one that stops answering, is parked or
loses its profile link is checked by hand and may be removed.
To change or remove their own entry later: another pull request changing or
deleting the folder's files, or form E. Removal takes it off the gallery, not out
of the public history.
Full guide: `docs/how-to/add-to-the-showcase.md`.

D. REPORT SOMETHING THAT DOES NOT WORK
On the repository: Issues, New issue, the Bug form: what happened and what they
expected, how to reproduce it (the design, the page, the browser and its version,
the screen width), and a link if there is one.

E. REMOVE OR REPORT A SHOWCASE ENTRY
Issues, New issue, the Showcase entry form: whether it is their own entry to
remove, an entry impersonating someone, or one that has gone bad (parked, broken,
harmful or not a portfolio); the entry's folder or address; what they see. For
their own entry they may instead open a pull request deleting its folder.

F. ASK A QUESTION
Issues, New issue, the Question form. Issues are public: nothing private in it.

G. REPORT A SECURITY PROBLEM
Privately, never in a public issue: on the repository's Security tab, Report a
vulnerability, as `SECURITY.md` says.

REPORTING, IN SHORT
The issue forms are Bug, Design proposal (optional, before building a design),
Showcase entry and Question. Blank issues are turned off.

FOR THE MAINTAINER ONLY
The maintainer's own pull requests may carry the marker `[scope: as contributor]`
in their description, to be checked as an outsider's. A contributor never needs it.
The maintainer's working rules are in `CLAUDE.md` and the state in `STATE.md`.

Now ask the person what they want to do, offering options A to G.
```
<!-- prompt:end -->

</details>

## How this repository is run

Every decision is written down as a record in
[docs/decisions/](docs/decisions/README.md), with the options it rejected.
Every check is listed with the case built to defeat it in
[docs/reference/standing-checks.md](docs/reference/standing-checks.md).
What the project is and does, in one file:
[CAPABILITIES.md](CAPABILITIES.md). Security reports:
[SECURITY.md](SECURITY.md). Conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Credit

Made by Waqas Sharif ([@Waqas01CP](https://github.com/Waqas01CP);
portfolio: https://waqas01cp.github.io/). If you use it, a link back is
appreciated: every site carries a small line in its footer, "Built with
portfolio-gallery, design Default by Waqas01CP", naming the design and
its author, each linked. You may turn it off with `"credit": false` in
`content/config.json`; the MIT licence asks only that LICENSE stays.

## Licence

MIT; see [LICENSE](LICENSE). The fonts each design ships are under their
own licences, named in the design's `design.json` with the licence text
beside each font. The sample content describes an invented person, Alex
Example; every employer, school and link in it is fictional.
