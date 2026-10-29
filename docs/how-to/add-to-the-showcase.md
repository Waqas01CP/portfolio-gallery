---
type: how-to
description: "A contributor's steps to add their own portfolio site to the gallery's showcase, in the browser: the link to their GitHub profile, a screenshot as their tool saves it, the entry, the pull request, and what is checked then and every week. Read to show your site in the gallery."
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

Snip your site's first screen, save it, and upload it as your tool saved
it. There is no size to check and nothing to resize.

- Windows: press the Windows logo key, Shift and S together, then drag
  over the page (Microsoft, "Use Snipping Tool to capture screenshots").
- Mac: press Shift, Command and 4 together, then drag over the page
  (Apple, "How to take a screenshot on your Mac").

Any size and any shape work, a phone's tall screen too: the gallery makes
its own smaller copies of your screenshot, without its metadata, and your
card shows a copy whole, never cropped, at the card's full width in your
screenshot's own shape; a click opens a larger copy over the gallery, with
a button to close it. A shape longer than
a 21:9 screen either way, as a whole page or a very wide monitor gives,
is shown whole within that shape, with bands. The checks take PNG, JPEG
or WebP, as screenshot tools save them. Two things they refuse, neither
of which an ordinary snip has:

- a location in the file's metadata, which a photo from a phone may carry;
- a file over 20 MB, larger than any screenshot measured, even of a wall
  of photographs on a 5K screen.

A Mac set to save screenshots in HDR saves HEIF, which the gallery's tools
cannot read; its usual setting saves PNG.

## 3. Open the pull request

1. On https://github.com/Waqas01CP/portfolio-gallery, click **Fork**, then
   **Create fork**.
2. In your fork, click **Add file**, then **Create new file**. Name it
   `showcase/<your-login>/entry.json`, with your GitHub login in lower
   case, and write:

```
{"name": "Your Name", "url": "https://your-site.example/", "description": "One line about you or your work.", "professions": ["software"]}
```

   The description is optional, one line of at most 120 characters; the
   name at most 80. `professions` is optional too: one to three ids from
   `src/professions.json`, such as `["mobile"]`, shown on your card
   (ADR-0020). Click **Commit changes**.
3. In your fork, open the `showcase/<your-login>/` folder, click **Add
   file**, then **Upload files**, add your screenshot as your tool saved
   it, under the name it was given, and **Commit changes**.
4. Click **Contribute**, then **Open pull request**. The description
   opens with two sections: keep **A showcase entry**, tick its three
   lines, and delete **A design**. Then click **Create pull request**.

The pull request may hold your folder and nothing else: `entry.json` and
the one screenshot.

Once merged, your card gets a like button: a post in the repository's
Discussions, made for it at the next publish, where a thumbs up counts
(ADR-0021).

## What is checked

On the pull request:

- **Scope**: every file is in `showcase/<your-login>/`, your own login as
  GitHub reports it for the pull request.
- **The files**: the fields of `entry.json`; the screenshot's format, by
  its first bytes, that it is one still image, that its metadata holds no
  location, and the 20 MB cap; and that no other entry lists the same
  site. Then Chrome reads the screenshot and draws the gallery's copies of
  it, so a file it cannot read is found here.
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
folder, or an issue with the **Showcase entry** form, which also takes a
report of an entry that impersonates someone or has gone bad. Anything
merged into this repository stays in its history, which is public: your
name, address, description and screenshot among it.
Removing an entry takes it off the gallery, not out of the history.
