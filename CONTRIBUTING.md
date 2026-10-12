<!--
type: reference
description: The rules for contributing to portfolio-gallery. How a design is proposed and submitted, what the checks enforce, what the review covers, how credit is shown, and what the maintainer commits to.
status: current
-->

# Contributing

Thank you for wanting to add to the gallery. This file is the rules, and
they apply to every contribution, the maintainer's included. They exist
because a design you contribute is published by everyone who chooses it,
under their own name.

**Contributions are designs.** Anything else (a bug fix, a feature, a
change to the page's HTML or to a check) starts as an issue, so it can be
discussed before anyone writes it.

## What a design is

A design is one folder, `designs/<your-design>/`, holding:

| File | What |
|---|---|
| `design.css` | Your stylesheet, at most 100 KB |
| `design.json` | The design's name, your name as you want it shown, your profile's address, a one-line description, the fonts to preload, and the licence of every font and image |
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
5. Open a pull request from your branch. Fill in the checklist in the
   pull request's description.

## What the checks enforce

They run on every pull request, and every one must pass before a review:

- **Scope.** Your pull request changes one design folder and nothing else.
  This check runs from this repository's own copy, not yours.
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
  they point; nothing moves when a visitor has asked for reduced motion.

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
- that it reads well, at a phone's width and a desktop's, in light and
  dark if it offers both;
- that its name and description say what it is.

A design can be declined for these reasons, with the reason given.

## Licence and credit

By opening a pull request you license your contribution under this
repository's MIT licence, as GitHub's terms provide for every repository
with a licence. Fonts and images keep their own licences, which your
`design.json` names.

Your design is credited on the gallery: its card shows your name as
`design.json` gives it, linked to the address you give, and so does the
footer of its live demo.

## What the maintainer commits to

- Every pull request gets a review, with reasons for any change asked for
  or any decline.
- A first response within a time the maintainer has not yet set. This line
  will say it once he has.
- Engine changes that would break a merged design are made with the
  design updated in the same change, or with its author told first.

## Conduct

Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md).
Security problems are reported privately, as [SECURITY.md](SECURITY.md)
says, never in a public issue.
