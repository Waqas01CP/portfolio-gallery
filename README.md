<!--
type: reference
description: What portfolio-gallery is, the gallery link, how to make your own site in a few steps, how to contribute a design, credit and licence. The entry point for a visitor.
status: current
-->

# portfolio-gallery

A portfolio site you can publish with GitHub Pages without installing
anything, and a gallery of designs for it. Write your content once, pick a
design with one setting, and GitHub builds and publishes your site.

**See every design: https://waqas01cp.github.io/portfolio-gallery/**

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

## Make your own site

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

## Contribute a design

A design is one folder of CSS, with fonts and images if it needs them,
that styles the same page every other design styles. It arrives by pull
request from your fork, is checked automatically, and is reviewed and
merged by the maintainer. Start with
[docs/how-to/add-a-design.md](docs/how-to/add-a-design.md) and the rules in
[CONTRIBUTING.md](CONTRIBUTING.md).

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
appreciated: every site carries a small "Built with portfolio-gallery"
line in its footer, which you may turn off with `"credit": false` in
`content/config.json`.

## Licence

MIT; see [LICENSE](LICENSE). The fonts each design ships are under their
own licences, named in the design's `design.json` with the licence text
beside each font. The sample content describes an invented person, Alex
Example; every employer, school and link in it is fictional.
