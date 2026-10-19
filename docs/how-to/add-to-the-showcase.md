---
type: how-to
description: "A contributor's steps to add their own portfolio site to the gallery's showcase, in the browser: the link to their GitHub profile, the screenshot and how to make it small enough, the entry, the pull request, and what is checked then and every week. Read to show your site in the gallery."
status: current
---

# Add your site to the showcase

The gallery shows templates first, designs anyone can use, then the
showcase: portfolio sites contributors built for themselves, in any way
they like. A design of your own is the way to be shown among the
templates ([add a design](add-a-design.md)); your site's link alone is
welcome too, and nothing ranks it lower within the showcase.

You need a GitHub account, your site at an `https://` address, and a
screenshot of its first screen. Everything below happens in the browser.

## 1. Link your site to your GitHub profile

Your site's home page must link to your GitHub profile,
`https://github.com/<your-login>`, anywhere on the page. The check fetches
the page as it is sent, never running it, and looks for that link: it
shows that the account opening the pull request controls the site. A link
that only a script adds is not seen.

## 2. Take the screenshot

1. Open your site in a desktop browser, in a window about 1280 pixels wide
   and 720 tall, and wait for it to finish loading.
2. Capture the first screen, not the whole page:
   - Windows: press the Windows logo key, Shift and S together, then drag
     over the page (Microsoft, "Use Snipping Tool to capture screenshots").
   - Mac: press Shift, Command and 4 together, then drag over the page
     (Apple, "How to take a screenshot on your Mac").
3. Check it against the rules:
   - a PNG, JPEG or WebP file;
   - wider than it is tall;
   - between 1,024 and 1,920 pixels wide;
   - at most 500 KB;
   - no location in its metadata. A screenshot has none unless a program
     added it; a photo from a phone often does.

The card shows your screenshot whole, scaled to fit, never cropped, and a
click opens it full size; any shape of a normal first screen works.

### If it is too large

A Mac screen, and many laptop screens, take screenshots at two or more
pixels to each point, so a 1280-wide window can become a 2560-pixel
image. Make it smaller, and save it as JPEG if it is still over 500 KB:

- **Windows, in Paint:** open the screenshot in Paint. On the Home tab,
  choose Resize, choose pixels, keep the proportions, and set the width to
  1280. Then save it with Save as, choosing JPEG (Microsoft, "Draw,
  Create, and Edit with Paint").
- **Mac, in Preview:** open the screenshot in Preview. Choose Tools, then
  Adjust Size, tick Scale proportionally, and set the width to 1280. Then
  choose File, then Export, and in Format choose JPEG (Apple, "Resize,
  rotate, or flip an image in Preview on Mac" and "Convert image file
  types in Preview on Mac"). A Mac that saves screenshots as HEIF needs this step
  too: the check takes PNG, JPEG or WebP.

Measured on 2026-10-19, first screens of four sites at 1280 by 720 were
at most 477 KB as PNG and 122 KB as JPEG; at 1920 by 1080, PNG reached
657 KB, over the limit, while JPEG stayed at 202 KB at most.

## 3. Open the pull request

1. On https://github.com/Waqas01CP/portfolio-gallery, click **Fork**, then
   **Create fork**.
2. In your fork, click **Add file**, then **Create new file**. Name it
   `showcase/<your-login>/entry.json`, with your GitHub login in lower
   case, and write:

```
{"name": "Your Name", "url": "https://your-site.example/", "description": "One line about you or your work."}
```

   The description is optional, one line of at most 120 characters; the
   name at most 80. Click **Commit changes**.
3. Rename your screenshot `screenshot.png`, `screenshot.jpg`,
   `screenshot.jpeg` or `screenshot.webp`, as its format is. In your fork,
   open the `showcase/<your-login>/` folder, click **Add file**, then
   **Upload files**, add the screenshot, and **Commit changes**.
4. Click **Contribute**, then **Open pull request**, and **Create pull
   request**.

The pull request may hold your folder and nothing else: `entry.json` and
the one screenshot.

## What is checked

On the pull request:

- **Scope**: every file is in `showcase/<your-login>/`, your own login as
  GitHub reports it for the pull request.
- **The files**: the fields of `entry.json`; the screenshot's format, by
  its first bytes, its shape, its width, its size and its metadata; and
  that no other entry lists the same site.
- **Your site**, fetched and never rendered: `https://` at every step, a
  certificate that verifies, a web page answering 200, no domain parking
  or sale service on the way, and the link to your GitHub profile. A site
  that refuses the check's request with 403 or 429, as bot protection
  does, is reported as not checked, and the maintainer opens it by hand.
- Then the maintainer opens your site in a browser, compares it with the
  screenshot, and merges.

Every week, each listed site is fetched again the same way. A site that
stops answering, is parked or loses its link to your profile is flagged,
and the maintainer opens it before removing the entry.

## Changing or removing your entry

Open another pull request that changes or deletes the files in your
folder. Anything merged into this repository stays in its history, which
is public: your name, address, description and screenshot among it.
Removing an entry takes it off the gallery, not out of the history.
