---
status: accepted
topic: build
description: "Each template and showcase site has a like button: a post in the repository's Discussions, category Likes, whose upvotes and thumbs up the deploy counts into the gallery's HTML. Read before changing the like button, the deploy's likes job, or what the gallery page loads."
date: 2026-10-29
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0021: Likes from GitHub Discussions

## Context and Problem Statement

The owner wants a like button on each template and each showcase site,
with every like counted. A like must be stored somewhere, and the gallery
is static pages on GitHub Pages. The scope floor forbids cookies,
tracking and requests to another origin in anything shipped (line 2),
requires every word in the initial HTML (line 3), and any paid service
(line 4).

## Decision Drivers

- ADR-0001 lines 2, 3 and 4.
- The owner's choice of 2026-10-29 UTC, of four options this seat put to
  him: "the simple option A is accepted ... i just need a like button for
  each template and site. which is essentially both. and i can turn on
  discussion."
- A like should be hard to inflate, and nobody's post but the project's
  should be able to claim a template's likes.

## Assumptions

- A1. A workflow's token with `discussions: write` can start a discussion
  and read reactions through GitHub's GraphQL API. **Sourced**: GitHub
  Docs, "Using the GraphQL API for Discussions" and the token's
  permissions, from the seat's knowledge, not read this session; proven
  by the first deploy after the owner turns Discussions on.
- A2. GitHub allows one reaction of each kind per account on a post.
  **Sourced**, as A1.
- A3. Categories cannot be made by the API; the owner makes the one named
  Likes. **Stated by the owner**: "i can turn on discussion".

## Considered Options

- A post per item in Discussions, its thumbs up counted into the HTML at
  each deploy (A, chosen)
- A counter on another site, called by the page
- The repository's stars
- GitHub's discussions embedded in the page (giscus)

## Decision Outcome

Chosen option: A, because it stores likes free on GitHub, needs no script
or request in the page, and lets one account like once.

- tools/likes.py, in the deploy's job likes, before build, in the gallery
  only: finds the category Likes; makes a post for any template or site
  without one, its item in a marker in the body; counts each post's thumbs
  up; writes likes.json. A post counts only if the workflow's own account
  or the owner wrote it, the first made if two, so a look-alike by anyone
  else claims nothing. Names go to GitHub as GraphQL variables, and only in
  titles, which notify no one.
- The job holds `contents: read` and `discussions: write`, nothing else.
  Any trouble with Discussions is a warning, never a failed run: likes.json
  is written empty, and build runs after likes whatever its result.
- build.py --likes FILE checks every entry, a post in this repository's
  Discussions and a whole number, and refuses anything else. Each card's
  line: "Like on GitHub", the link naming its item to a screen reader, to
  its post, with ", 3 likes"; without a count, to the category, with none.
- Counts change when the gallery is next published: each merge to main,
  or Deploy run by hand. A schedule would be a run that writes with
  nobody's review, which the owner refused for scheduled workflows
  (ADR-0016, Q2), so there is none.

### Consequences

- Good: no script, cookie or request in the page; free; one like per
  account.
- Bad: liking needs a GitHub account, on GitHub's page, not the card.
- Bad: a count can be a day or more behind, until the next publish.
- Neutral: nineteen posts appear in Discussions at the first run, and one
  more with each new template or site.

### Confirmation

Cases in tools/prove_checks.py, against a fake GraphQL API: a stranger's
look-alike post, made first with 50, is not counted, and the workflow's
post with 2 is (with the author rule removed, the stranger's 50 wins); the
owner's own post counts; a template with no post gets one; Discussions
off, no category Likes, and no token each end in a warning and an exit of
0. The build refuses a count linking outside the repository's
Discussions, a count not a whole number, and counts given to a site; a
file as likes.py writes it builds.

## Pros and Cons of the Options

### A post per item in Discussions

- Good: free, static, one like per account.
- Bad: an account needed; counts lag until the next publish.

### A counter on another site

- Good: one click, on the card.
- Bad: a request to another origin from every visitor (line 2); free
  tiers end; a script can inflate it.

### The repository's stars

- Good: nothing to build.
- Bad: one count for the whole project.

### giscus

- Good: reactions shown in the page.
- Bad: another site's frame in the page (line 2).

## More Information

- The owner's setup: docs/setup-on-github.md, step 13.
- The category's format is Open-ended discussion, not Announcement, since
  whether the workflow's account may start posts in an Announcement
  category was not tested; anyone may post there, and no one else's post
  is counted.

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-29 | **A1 proven on GitHub**: after the owner's step 13, Deploy run by hand made the nineteen posts, numbers 34 to 52, written by github-actions in the category Likes, an Open-ended discussion; the live gallery's nineteen cards each link to their post. | The run's log of the likes job, sent by the owner; the live gallery, read 2026-10-30. |
| 2026-10-30 | **A like is an upvote or a thumbs up on the post, the two added together.** The owner's own test like landed on a comment, which counts nothing: a visitor reaches for the upvote arrow as readily as the thumbs up. GitHub allows one of each per account, so one person counts at most twice; comments, and anything on them, count nothing. The workflow rewrites the text of its own posts that still say a thumbs up alone; the owner's posts are left as he wrote them. Cases: upvotes and thumbs up added, upvotes alone, the rewrite; with upvotes left out, the case fails. | The owner's choice of 2026-10-30 UTC, after his own like landed on a comment: "counting both is reasonable because not many people will do both as those who know about this will rarely both upvote and leave like emoji and those that do not know will just only leave a like." |
