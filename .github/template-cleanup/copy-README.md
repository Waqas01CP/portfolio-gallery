# My portfolio

This repository builds my portfolio site and publishes it with GitHub
Pages. Each commit to `main` builds the site again; the **Actions** tab
shows each run.

- **The content** is in `content/`: [what each field means](docs/reference/content.md),
  and [the shape of the CV](docs/reference/cv-format.md) the checks trace
  every sentence to.
- **The CV is the source.** Every fact in `content/site.json` and
  `content/items.json` must also be in `content/cv.md`, so a change to one
  needs the same change in the other, or the build fails and names the CV
  line to look at. To publish without a CV, set `"content_trace": false`
  in `content/config.json`.
- **The design** is named in `content/config.json`, one of the folders in
  `designs/`; [what a design may style](docs/reference/design-contract.md).
- **Step by step**, from the copy to a live site:
  [docs/how-to/use-this-template.md](docs/how-to/use-this-template.md).

Built with [portfolio-gallery](https://github.com/Waqas01CP/portfolio-gallery),
whose gallery shows every design: https://waqas01cp.github.io/portfolio-gallery/.
It is under the MIT licence; see [LICENSE](LICENSE).
