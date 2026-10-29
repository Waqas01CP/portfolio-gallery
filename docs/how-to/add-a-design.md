---
type: how-to
description: A contributor's journey, step by step. Fork, create a design folder, build and check it locally, and open a pull request that passes the checks. Read to add a design to the gallery.
status: current
---

# Add a design to the gallery

A design is one folder of CSS, fonts and images that styles the same page
every other design styles. The rules are in CONTRIBUTING.md; what the page
offers you is in docs/reference/design-contract.md.

## 1. Fork and branch

1. On this repository's page, click **Fork**, then **Create fork**.
2. In your fork, create a branch for your design, such as `design-dusk`.

## 2. Make the folder

Pick a name: lowercase letters, digits and single hyphens, such as
`dusk`. Then create `designs/dusk/` with:

- `design.css`: start from a copy of `designs/plain/design.css`, which
  covers every part of the page in under 300 lines.
- `design.json`:

```
{
  "name": "Dusk",
  "author": "Your Name",
  "author_url": "https://github.com/your-username",
  "description": "One line: what it looks like and who it is for.",
  "professions": ["frontend"],
  "dark": true,
  "preload": ["fonts/your-font.woff2"],
  "assets": [
    {
      "file": "fonts/your-font.woff2",
      "licence": "OFL-1.1",
      "licence_file": "fonts/YourFont-OFL.txt",
      "source": "https://github.com/the-font-project"
    }
  ]
}
```

In the gallery your design is shown with the sample person in
`content/`, Alex Example; the project's own templates made for a
profession may be shown with their own (ADR-0018).

`dark` says whether your design styles a dark theme. With `true`, the
page follows the visitor's device and offers a Dark switch, and your CSS
styles both themes (docs/reference/design-contract.md, "Light and dark").
With `false`, the page has one theme, the same on every device, and no
switch, and you style that theme only. It is light unless your CSS makes
it dark: the page tells the browser it is light, so the browser's own
defaults stay light, and a design whose one theme is dark sets
`color-scheme: dark` on `:root` itself, as `designs/console/` does.

`in_use` is optional: the `https://` address of your own live site built
with this design, shown as "In use" on its gallery card. Like a showcase
entry, it is fetched on the pull request and every week, never rendered,
for `https://`, a 200 answer and a domain not parked
(docs/how-to/add-to-the-showcase.md).

`professions` is optional: one to three ids from `src/professions.json`
for the professions your design is made for, such as `["games"]`, shown
on its gallery card. Leave it out if the design suits anyone (ADR-0020).

`preload` lists the fonts that set text on the first screen, so they load
with the page. `assets` lists every font and image, each once; an image
you made yourself is `"licence": "MIT", "source": "own work"`. Allowed
licences: OFL-1.1, Apache-2.0, MIT, CC0-1.0. Leave `preload` and `assets`
as `[]` if you ship none.

Things the checks will refuse, so you need not find out from them: SVG,
any script, `@import`, a `url()` that is not `fonts/...` or `img/...` in
your folder, and generated text (`content: "..."` with words in it). For a
decorative glyph, give it empty alternative text: `content: "+" / "";`.
And a page that scrolls sideways at any width from 320 px up: check yours
on a narrow phone with every section open.

## 3. Build and look at it

You need Python 3.12 or later. From the repository's folder:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt        Windows
.venv/bin/python -m pip install -r requirements.txt            macOS, Linux
```

Then, with the venv's Python (`.venv\Scripts\python` or `.venv/bin/python`):

```
python build.py --design dusk
python -m http.server --directory _site 8000
```

Open http://127.0.0.1:8000/ and look at it at a phone's width and a
desktop's, in light mode and, if `dark` is `true`, in dark mode and with
the Dark switch both ways, and with every "In depth" panel and timeline
card open. `python build.py --gallery` builds
every design, as the gallery shows them.

## 4. Run the checks

```
python tools/check_design.py dusk
python tools/check_built.py
python tools/check_browser.py _site --quick
```

The last needs Google Chrome installed; it starts its own headless Chrome
and never touches your browser. The pull request runs the full set; these
catch most problems first.

## 5. Open the pull request

1. Commit only `designs/dusk/` to your branch, and push it to your fork.
2. On your fork's page, click **Contribute**, then **Open pull request**.
3. The description opens with two sections: keep **A design**, fill in
   its checklist, and delete **A showcase entry**. Then create the pull
   request.

Two checks run: **scope**, at once, and **checks**, once the maintainer
approves a first-time contributor's run. **checks** looks at your design's
page in a browser and at no other design's, so it takes minutes, not an
hour. If one fails, open it from the
pull request's **Checks** tab: the failing step names every problem. Push
a fix to the same branch and both run again.

The maintainer then reviews what checks cannot see (CONTRIBUTING.md,
"What the review covers") and merges it, or says what to change and why.
Once merged, the next deploy builds your design into the gallery, with
its preview taken by the workflow, and credits you on its card.
