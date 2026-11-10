---
type: deferred
description: "Link previews (Open Graph and an X card) on a copy's own site, as the gallery page has them. Deferred 2026-11-06 by the owner; reopen when a user asks."
status: open
---

# Link previews on a copy's own site

**Deferred 2026-11-06.** Not rejected. Not scheduled. The owner's decision
of that date, as Report 17 recommended (relayed in Brief 17).

## What was proposed

A site built from the template carrying the tags LinkedIn, X and others
read when its address is shared, og:title, og:description, og:url,
og:image and an X card, as the gallery page has carried since 2026-11-04
(ADR-0022), so a shared link to a user's portfolio shows a picture and
its words.

## Why it was not built

Open Graph needs absolute addresses, and a site names none of its own:
"We will configure no site URL and no base path" (ADR-0007). The gallery
page names its address because it is the project's, fixed in build.py as
PROJECT_URL is (ADR-0022); a copy's address is its owner's. Nothing was
built for a site; no user has asked.

## What could and could not be compared

What it would take, from Report 17, 6.2, 2026-11-04:

- **The site's absolute address**, either a setting in content/config.json,
  against ADR-0004's one setting and ADR-0007's nothing to configure, or
  given by the deploy, as configure-pages gives it, which ADR-0007 refused
  because a local and a deployed build would differ.
- **A picture of at least 1200 by 627 pixels and at most 5 MB** (LinkedIn,
  "Make your website shareable on LinkedIn", read 2026-11-04): either a
  file the user adds to content/, or one the deploy takes in Chrome, which
  a copy's deploy does not run today (its shots job runs in the gallery
  only).
- **Its words** from site.json's name and headline, as the site's
  description tag already has them.

The smallest version: a picture the user supplies and the address from
the deploy. Not measured: how many users would want it, or whether a
picture they supply would meet the limits without help.

## The trigger

A user asks: the first issue, discussion or pull request asking for link
previews on their own site.

## What revisiting would have to produce

A record amending ADR-0007 for the address, with the owner's approval;
the picture's rules and their check, held as check_built holds the
gallery's (ADR-0022), with defeat cases; the cleanup's and the copy's
documents updated; and a site that builds unchanged when the user gives
no picture.
