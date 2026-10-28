<!--
type: reference
description: The rules for contributing to portfolio-gallery. How a design or a showcase entry is proposed and submitted, what the checks enforce, what the review covers, how credit is shown, and what the maintainer commits to.
status: current
-->

# Contributing

Thank you for wanting to add to the gallery. This file is the rules, and
they apply to every contribution, the maintainer's included. They exist
because a design you contribute is published by everyone who chooses it,
under their own name.

**Contributions are designs, or a link to your own site.** The gallery
shows templates first, designs anyone can use, then the showcase,
contributors' own portfolio sites. A design is encouraged, and shown
among the templates, with an optional "In use" link to your own site
built with it. A showcase entry is your site's link and a screenshot as
your tool saved it, any size and any shape, with nothing to resize or
rename, and nothing ranks it lower within the showcase:
[docs/how-to/add-to-the-showcase.md](docs/how-to/add-to-the-showcase.md).
Anything else (a bug fix, a feature, a change to the page's HTML or to a
check) starts as an issue, so it can be discussed before anyone writes
it.

## What a design is

A design is one folder, `designs/<your-design>/`, holding:

| File | What |
|---|---|
| `design.css` | Your stylesheet, at most 100 KB |
| `design.json` | The design's name, your name as you want it shown, your profile's address, a one-line description, whether it offers a dark theme, the fonts to preload, the licence of every font and image, and optionally `in_use`, your own live site built with it |
| `fonts/*.woff2` | Optional fonts, at most 200 KB each, each with its licence text as `fonts/*.txt` |
| `img/*.png`, `*.webp`, `*.jpg`, `*.jpeg` | Optional images, at most 300 KB each |

Nothing else: no SVG, which can carry script; no HTML, templates or
JavaScript; no other folders; at most 600 KB and 40 files in all. Every
design styles the same HTML, so your design works with anyone's content,
and one setting swaps it for another. What the HTML offers you is in
[docs/reference/design-contract.md](docs/reference/design-contract.md).

## How to propose and submit one

1. If you want a view before you start, open an issue with the **Design
   proposal** form. It is optional.
2. Fork this repository and create a branch in your fork.
3. Add your folder under `designs/`. Copy `designs/plain/` as a start if it
   helps; it is short.
4. Build and look at it locally, and run the checks if you can:
   [docs/how-to/add-a-design.md](docs/how-to/add-a-design.md) has every
   command.
5. Open a pull request from your branch. Its description opens with two
   sections, one for a design and one for a showcase entry: keep **A
   design**, fill in its checklist, and delete the other.

## What the checks enforce

They run on every pull request, and every one must pass before a review:

- **Scope.** Your pull request changes one design folder, or your own
  showcase folder, `showcase/<your-login>/`, and nothing else. This check
  runs from this repository's own copy, not yours.
- **The design's files**: only the files above, within their limits; every
  file's content matches its type; `design.json` complete; every font and
  image listed with its licence; the stylesheet has no `@import`, no
  `url()` outside your own `fonts/` and `img/`, and nothing that loads from
  elsewhere or runs.
- **The pages built with your design**: nothing requested from another
  site; the same words as the page with no design (a design can neither
  hide content nor add text of its own); the page a screen reader meets
  at load is the page it meets later; every "In depth" panel works by
  keyboard; no words run together for a screen reader; links land where
  they point; nothing moves when a visitor has asked for reduced motion;
  no page scrolls sideways, on a phone 320 px wide or on a wide screen.

Every check, and the case built to make it fail, is in
[docs/reference/standing-checks.md](docs/reference/standing-checks.md).
For a first contribution, GitHub asks the maintainer to approve the checks
before they run; that is a setting, not a judgement.

## What the review covers

Checks cannot read intent. The maintainer reviews what they cannot:

- that the design is **notably different** from the designs already in the
  gallery, and not a copy of someone else's work;
- that **you have the right to every font and image**: a font must ship
  with its licence, and a font whose licence reserves its name must be the
  unmodified original;
- that it reads well, at a phone's width and a desktop's, in light, and
  in dark too when its `design.json` says it offers dark;
- that its name and description say what it is.

A design can be declined for these reasons, with the reason given.

For a showcase entry, the checks cover its files, draw the gallery's
copies of its screenshot, and fetch the site without rendering it; the
maintainer opens the site in a browser and
checks that the screenshot shows it, that it is a portfolio, and that it
is fit to show. Each listed site is fetched again every week; one that
stops answering, is parked or loses its link to its author's GitHub
profile is opened by hand, then removed if it is gone.

## Licence and credit

By opening a pull request you license your contribution under this
repository's MIT licence, as GitHub's terms provide for every repository
with a licence. Fonts and images keep their own licences, which your
`design.json` names.

Your design is credited on the gallery: its card shows your name as
`design.json` gives it, linked to the address you give, and so does the
footer of its live demo. Every site built with your design names it and
you in its footer, beside portfolio-gallery, each linked, unless its
owner turns the credit off.

## What the maintainer commits to

- Every pull request gets a review, with reasons for any change asked for
  or any decline.
- A first response within 7 days.
- Engine changes that would break a merged design are made with the
  design updated in the same change, or with its author told first.

## Conduct

Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md).
Security problems are reported privately, as [SECURITY.md](SECURITY.md)
says, never in a public issue.
