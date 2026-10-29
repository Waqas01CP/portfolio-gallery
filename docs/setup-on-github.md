---
type: how-to
description: "The owner's click-by-click steps to publish this repository: create it on GitHub, push, and set every setting the security model depends on, in order, each with what you should see; then the test pull requests that prove each workflow. For the owner, after the architecture chat has checked them."
status: current
---

# Publishing portfolio-gallery on GitHub

For the owner of the GitHub account `Waqas01CP`. Written
2026-10-12 UTC by the implementing seat from GitHub's documentation as read
that day; each step names the page it rests on. **Do not start until the
portfolio architecture chat has checked these steps** (the brief's
Addendum 1). Where a screen differs from what a step says you should see,
stop and send what you see instead; GitHub changes its settings pages.

**Status, 2026-10-21 UTC:** the owner followed every step and Tests 1 to
5 between 2026-10-16 and 18, and the steps below carry what that showed.
Test 6 passed on 2026-10-20: his own entry, from a plain snip of
1077x1713 pixels saved as his tool named it, passed scope and checks on
pull request 13 and merged; Deploy, with its shots and assemble jobs,
passed on main; Showcase links, run by hand, passed (run 39507307570).
An earlier head of that branch, entry.json alone, failed checks at the
fetch step, as an entry without a screenshot should. One proof waits:
Test 1 again on or after 2026-11-02 (below).

Each step is one action. "Send back" lists what to paste to the chat.

## Before you start: the pre-publish search

Step 3 publishes every commit, and a public commit cannot be deleted
(ADR-0005). Push only once the pre-publish search has passed on the
commit you are about to push: the seat's part, and the search for your
master CV's text, which runs through the chat. The seat's latest report
names the commit each part last ran on; the top line of `git log` in
step 1 must show that commit.

## Part A: on your computer

### Step 1. Check the local repository

Open PowerShell in the repository's folder and run:

```
git status --short
git log --oneline
git remote -v
```

You should see: no lines from `git status`; the session's commits from
`git log`; and nothing from `git remote -v`, because no remote exists yet.

## Part B: create the repository

GitHub Docs, "Creating a new repository".

### Step 2. Create an empty repository

1. Go to https://github.com/new.
2. **Owner**: Waqas01CP. **Repository name**: `portfolio-gallery`.
3. **Description**: A portfolio site you can copy and publish on GitHub Pages without
   installing anything, and a gallery of designs for it, each contributed
   by pull request and checked automatically.
4. **Public**.
5. Leave **Add a README file** unticked, **.gitignore** at "None" and
   **License** at "None": the local copy has its own, and GitHub's would
   make the first push fail.
6. Click **Create repository**.

You should see a page titled "Quick setup", with the address
`https://github.com/Waqas01CP/portfolio-gallery.git`.

### Step 3. Push

In PowerShell, in the repository's folder:

```
git remote add origin https://github.com/Waqas01CP/portfolio-gallery.git
git push -u origin main
```

You should see gate E report "gate E passed", then git's own lines ending
with `main -> main`. If a window asks you to sign in to GitHub, sign in as
Waqas01CP.

Then open https://github.com/Waqas01CP/portfolio-gallery and click the
**Actions** tab. You should see two runs for the push: **Checks**, which
should go green in about 10 minutes (9 on 2026-10-16), and **Deploy**,
which publishes nothing yet: Pages is not set up and step 7's variable is
not set, so it runs as a copy's would and ends with the notice "Turn on
GitHub Pages to publish your site", its deploy job skipped. On 2026-10-16,
before that notice existed, it failed at its last job instead. Step 8
runs it again.

**Send back:** the result of each run (green, the notice, or the failed
step's name).

## Part C: settings, in this order

### Step 4. Actions: which actions, approvals, the token

GitHub Docs, "Managing GitHub Actions settings for a repository".

1. **Settings** (the repository's tab), then in the left sidebar
   **Actions**, then **General**.
2. Under "Actions permissions", choose **Allow Waqas01CP, and select
   non-Waqas01CP, actions and reusable workflows**, tick **Allow actions
   created by GitHub**, and leave the rest unticked. The workflows use only
   actions GitHub publishes.
3. On the same page, tick **Require actions to be pinned to a full-length
   commit SHA**. Every action in the workflows already is, so nothing
   breaks, and a future change that is not is refused by GitHub itself.
   Click **Save** under this section.
4. Under "Approval for running fork pull request workflows from
   contributors", choose **Require approval for all external
   contributors**, and click **Save**. Why: the two first-time options stop
   asking once someone has had any change merged, and GitHub's page warns
   that "A malicious user could meet this requirement by getting a simple
   typo or other innocuous change accepted". The cost is one click per
   contributor's run. The scope check is not held back by this: GitHub
   runs `pull_request_target` workflows "regardless of approval settings".
5. Under "Workflow permissions", check that **Read repository contents and
   packages permissions** is selected and that **Allow GitHub Actions to
   create and approve pull requests** is unticked. Both are the defaults
   for a new repository in a personal account, by that page. Click
   **Save** if you changed anything.

**Send back:** the option now selected in each of the four sections.

### Step 5. Actions: allow the scope check's trigger

GitHub Docs, "Securely using pull_request_target", "About Actions
policies" and "Governing execution of GitHub Actions workflows", read
2026-10-12. GitHub has added a default policy that blocks the
`pull_request_target` event in public repositories, enforced from
2026-11-02 UTC. The scope check needs that event, and GitHub's page says
what to do: "If the workflow must continue to use pull_request_target,
create or update an applicable Actions event policy that explicitly allows
pull_request_target." The scope workflow is the safe kind that page
describes: it checks out only the default branch and runs nothing from the
pull request.

1. **Settings**, then **Actions**, then **Policies**.
2. Create a new policy. Name: **Allow the scope check**. Enforcement:
   **Active**.
3. Target only the workflow `.github/workflows/scope.yml`, in this
   repository.
4. Under the event rules, allow **pull_request_target**.
5. Save.

You should see the policy listed as Active. **Stop and send what you see**
if the page offers no way to target one workflow, or if allowing one event
would block others: a policy that allows only `pull_request_target` for
every workflow would stop the deploy (`push`) and the checks
(`pull_request`). In that case allow `push`, `pull_request`,
`pull_request_target` and `workflow_dispatch`, which are every event the
three workflows use, and say so in what you send back.

**Send back:** the policy's name, target and allowed events as the page
shows them.

### Step 6. Pages: publish from GitHub Actions

GitHub Docs, "Configuring a publishing source for your GitHub Pages site".

1. **Settings**, then **Pages**.
2. Under "Build and deployment", **Source**: **GitHub Actions**.

You should see the page say the site is built from a workflow; there is no
branch to choose.

### Step 7. The variable that makes this repository build the gallery

The deploy workflow builds the gallery only where the repository variable
`PORTFOLIO_GALLERY` is `true`; every copy of the template, which does not
have it, builds its owner's site instead.

1. **Settings**, then **Secrets and variables**, then **Actions**.
2. The **Variables** tab, then **New repository variable**.
3. Name `PORTFOLIO_GALLERY`, value `true`. **Add variable**.

### Step 8. Publish the gallery

1. **Actions** tab, then **Deploy** in the left list.
2. **Run workflow**, branch `main`, **Run workflow**.

You should see five jobs: build, pages, shots, assemble, deploy, all green
within about 5 minutes. If pages failed saying GitHub Pages is off, step 6
did not take: in the gallery an off Pages fails, since the gallery would
be down. Open the run and look at each job's icon, not the run's:
GitHub counts a skipped job as passed, so a run can be green while a job
was skipped (a grey circle with a line through it). If **shots** was
skipped, the build did not read the variable of step 7: check that it is
on the **Variables** tab of **Settings**, **Secrets and variables**,
**Actions** (not a secret, and not in an environment), named exactly
`PORTFOLIO_GALLERY`, with the value `true`, then run this step again. Then
open https://waqas01cp.github.io/portfolio-gallery/:
the gallery, with a card for each design in designs/, Default first, each
with its screenshot and a "Live demo" link that opens the design. Also open
https://waqas01cp.github.io/portfolio-gallery (no slash at the end): it
should arrive at the same page.

**Send back:** each job's result, and whether both addresses show the
gallery with both screenshots. If the shots job failed, send its log's
last 30 lines: Chrome's sandbox on the runner is the one thing the seat
could not test (ADR-0010).

### Step 9. Protect main with a ruleset

GitHub Docs, "Creating rulesets for a repository" and "Available rules for
rulesets".

1. **Settings**, then under "Code and automation" **Rules**, then
   **Rulesets**, **New ruleset**, **New branch ruleset**.
2. **Ruleset name**: `main`. **Enforcement status**: **Active**.
3. **Bypass list**: leave empty, so the rules bind you too and every change
   goes through a pull request and the checks.
4. **Target branches**: **Add target**, **Include default branch**.
5. Tick **Restrict deletions** and **Block force pushes**.
6. Tick **Require a pull request before merging**. Set **Required
   approvals** to **0**: you cannot approve your own pull requests, and
   your merge is the review (ADR-0003). Leave the other options under it
   unticked.
7. Tick **Require status checks to pass**. Add the check **checks**, with
   the source **GitHub Actions** if the page offers a source. The picker
   offers only checks that have already run here, and **scope** runs only
   on a pull request, so it cannot be added yet: Test 1 adds it. Leave
   **Require branches to be up to date before merging** unticked.
8. **Create**.

You should see the ruleset `main` listed as Active.

**Send back:** the rules ticked and the status check as listed.

### Step 10. Private vulnerability reporting

GitHub Docs, "Configuring private vulnerability reporting for a
repository".

1. **Settings**, then in the "Security" section of the sidebar **Advanced
   Security** (or "Code security").
2. To the right of **Private vulnerability reporting**, click **Enable**.

You should see the **Security** tab now offer **Report a vulnerability**.

### Step 11. Template repository, description, website, topics, label

GitHub Docs, "Creating a template repository".

1. **Settings**, **General**, tick **Template repository**. The repository
   page now shows **Use this template**, which the README tells users to
   click. Why a template and not forks: a copy from a template "starts
   with a single commit" and its commits "do appear in your contribution
   graph", where a fork's do not; and a fork's workflows stay off until its
   owner enables them. Forks remain the way to contribute a design.
2. On the repository's main page, the gear beside **About**:
   - **Description**, if it differs: the text of step 2.
   - **Website**: tick **Use your GitHub Pages website**, or paste
     `https://waqas01cp.github.io/portfolio-gallery/`.
   - **Topics**: `portfolio-template`, `portfolio`, `portfolio-website`,
     `github-pages`, `template`, `developer-portfolio`, `accessibility`,
     `static-site-generator`, `python`, `jinja2`, `css`, `resume`.
   - **Save changes**.
3. **Issues** tab, **Labels**, **New label**: `design`, with the
   description "A design proposed for the gallery: one folder of CSS,
   fonts and images on the shared page." The design proposal form applies
   it.

### Step 12. Keep your email address out of commits made on GitHub

GitHub Docs, "Setting your commit email address", read 2026-10-16. A file
you edit, or a pull request you merge, on GitHub's website is a commit,
authored with an email address of your account. Unless your addresses are
kept private, it can be a personal one, and a public commit cannot be
deleted. Part D's tests, and every merge of a contributor's design, are
such commits; gate A guards only commits made on your computer.

1. Your picture at the top right, **Settings**, then **Emails** in the
   sidebar.
2. Tick **Keep my email addresses private**. GitHub then authors your
   website commits with your no-reply address, the one this repository's
   commits use, and with your profile's name.
3. Optional: **Block command line pushes that expose my email**. It
   refuses a push, from any repository of yours, whose latest commit
   carries one of your private addresses. Tick it only if none of your
   repositories commits with one.

You should see an address ending in `@users.noreply.github.com` named
under the first box.

**Send back:** that the first box is ticked, and whether you ticked the
second. Not the address.

## Part D: prove each workflow

Each test is a pull request you open and then close without merging. The
marker `[scope: as contributor]` in a pull request's description makes the
scope check treat your pull request as an outsider's; without it, your
own pull requests pass the scope check as the owner's.

### Test 1. The scope check refuses a change outside designs/

1. On the repository's main page, open `README.md`, click the pencil,
   change one word.
2. **Commit changes**, choose **Create a new branch** (name it
   `test-scope`), **Propose changes**.
3. In the pull request's description, write `[scope: as contributor]`.
   **Create pull request**.

You should see **scope** fail within a minute, its summary saying
"README.md: outside designs/", and **checks** start.

4. Now that scope has run, make it required: **Settings**, **Rules**,
   **Rulesets**, `main`; under **Require status checks to pass**, **Add
   checks**, choose **scope** (source **GitHub Actions**), and **Save
   changes**.
5. Back on the pull request, wait for **checks** to pass, about 10
   minutes. You should see both checks marked **Required**, and the merge
   button disabled because scope failed.
6. **Close pull request**, then **Delete branch**.

### Test 2. A design is in scope and passes every check

A design is two files at least, and both must be in one pull request: a
pull request with one of them fails the design check, rightly.

1. On the repository's main page, **Add file**, **Create new file**, name
   `designs/test-design/design.css`, with this content, the least CSS
   that meets the rules (light only, one menu shown, no list or
   disclosure markers):

```
.mbar, .rail, .knot { display: none; }
ul, ol, summary { list-style: none; }
summary::-webkit-details-marker { display: none; }
```

   **Commit changes**, choose **Create a new branch** and name it
   `test-design`, **Propose changes**. GitHub then offers to open a pull
   request: do not open it yet.
2. Open https://github.com/Waqas01CP/portfolio-gallery/tree/test-design/designs/test-design
   and **Add file**, **Create new file**, name `design.json`, with this
   content:

```
{"name": "Test", "author": "Waqas01CP", "author_url": "https://github.com/Waqas01CP", "description": "A test design.", "dark": false, "assets": []}
```

   `"dark": false` makes the page light on every device, with no Dark
   switch, so a design that sets no colours reads in every case (ADR-0006,
   Changes, 2026-10-18). The two files passed every check on the seat's
   machine on 2026-10-18, axe included.

   **Commit changes**, choose **Commit directly to the `test-design`
   branch**, **Commit changes**.
3. Open https://github.com/Waqas01CP/portfolio-gallery/compare/main...test-design,
   click **Create pull request**, write `[scope: as contributor]` in the
   description, and **Create pull request**.

You should see **scope** pass ("In scope: 2 file(s), all in
designs/test-design/") and **checks** pass after about 15 minutes (13.5
on 2026-10-18). Wait for both before going on.

4. **Close pull request**, then **Delete branch**.

### Test 3. main refuses a direct change

1. Open `README.md` on `main`, click the pencil, change one word, and try
   **Commit changes** with **Commit directly to the main branch**.

You should see GitHub refuse, or offer only a new branch, naming the
ruleset. Cancel.

**Send back:** for each test, what each check showed and whether merging
was possible.

### Test 4. A copy of the template publishes its owner's site

This repository builds in gallery mode, so its own runs never take the
path every copy takes: site mode, with shots skipped, the path the deploy
job was skipped on until 2026-10-16. This test makes a copy as a user
would and watches it publish. It needs steps 11 and 12 first. The copy
is public while it exists and carries the same LICENSE, README credit and
Code of Conduct as this repository, as every user's copy will; it is
deleted at the end.

1. On https://github.com/Waqas01CP/portfolio-gallery, click **Use this
   template**, then **Create a new repository**.
2. **Owner**: Waqas01CP. **Repository name**: `pg-copy-test`. **Public**.
   Leave **Include all branches** unticked. **Create repository**.

   You should see the new repository's page say it was generated from
   Waqas01CP/portfolio-gallery.
3. Its **Actions** tab. You should see **Checks** and **Deploy** for its
   first commit; if none appear, note it and go on to 4. In Deploy: build,
   pages and assemble green, shots and deploy skipped (grey), no red, and
   the run's summary headed "Turn on GitHub Pages to publish your site",
   because the copy has no Pages yet (ADR-0015, Changes, 2026-10-23).
   Deploy starting at all is the fix of 2026-10-16 at work.
4. In the copy: **Settings**, **Pages**, **Source**: **GitHub Actions**.
5. **Actions**, **Deploy**, **Run workflow**, branch `main`, **Run
   workflow**. You should see build, pages, assemble and deploy green and
   shots skipped, within about 3 minutes. Then open
   https://waqas01cp.github.io/pg-copy-test/: the sample site, Alex
   Example.
6. Delete the copy: its **Settings**, **General**, at the bottom **Delete
   this repository**, and confirm with its name. Its site goes with it.

**Send back:** whether the first runs appeared on their own; each Deploy
job's icon in both runs; whether the address showed Alex Example; and
that the copy is deleted.

### Test 5. A copy cleans itself up, once

ADR-0015's cleanup in a real copy: that it runs once, what it removes,
that the copy still builds and checks, and whether GitHub lets a
workflow's own token delete workflow files. It needs steps 11 and 12.
The copy is public while it exists; the architecture chat reads its files
and runs before you delete it.

1. On https://github.com/Waqas01CP/portfolio-gallery, click **Use this
   template**, then **Create a new repository**. **Owner**: Waqas01CP.
   **Repository name**: `pg-cleanup-test`. **Public**. Leave **Include
   all branches** unticked. **Create repository**.
2. Its **Actions** tab. You should see three runs for its first commit:
   **Checks**, **Deploy** and **Template cleanup**. Template cleanup goes
   green within a few minutes. Open it, then its job, then its last step,
   "Try to remove the project's own workflows too", and note what it
   says: "Removed scope.yml and template-cleanup.yml." (as on 2026-10-18),
   or "GitHub did not let this workflow's token change workflow files...".
3. Its **Code** tab. You should see the latest commits "Make it yours:
   remove portfolio-gallery's project files" and "Make it yours: remove
   portfolio-gallery's own workflows", both by github-actions. The README
   reads "My portfolio"; there is no `CODE_OF_CONDUCT.md`,
   `CONTRIBUTING.md` or `STATE.md`, no `docs/decisions/` folder, and
   `.github/` holds only `workflows/checks.yml` and `workflows/deploy.yml`.
4. In the copy: **Settings**, **Pages**, **Source**: **GitHub Actions**.
5. Open `content/site.json`, click the pencil, and in the first contact
   route change the `"line"` value, "The quickest way to reach me.", to
   "The fastest way to reach me."; **Commit changes** directly to
   `main`. A contact route's line is one of the few texts the content
   trace takes as written rather than tracing to the CV, so this one edit
   needs no matching change in `content/cv.md`; a fact, such as the
   `"location"`, would (on 2026-10-18 this step said "location", and the
   trace refused it until cv.md matched). On the **Actions** tab you
   should see **Checks** and **Deploy** run on the cleaned files, and
   both go green. Open https://waqas01cp.github.io/pg-cleanup-test/: the
   sample site, with "fastest" under Contact.
6. Send the chat the copy's address and wait for its word: it reads the
   copy's files and runs through GitHub's API.
7. Delete the copy: its **Settings**, **General**, **Delete this
   repository**, and confirm with its name.

**Send back:** what step 2's last step said; the commits in step 3;
each run of step 5; then that the copy is deleted.

### Test 6. Your own site joins the showcase by pull request

The first real showcase entry, yours, made as any contributor would make
one (ADR-0016) and merged, unlike the tests above. It needs the showcase
on main, and screenshots taken as they come (ADR-0016, Changes,
2026-10-20): it proves the easy path, snip, save, upload. Your site
already links to https://github.com/Waqas01CP (checked 2026-10-19).

1. Open https://waqas01cp.github.io/ in your browser and snip its first
   screen as you normally would: on Windows, the Windows logo key, Shift
   and S, then drag over the page. Save it where your tool offers, under
   the name it gives. Check nothing about its size, and do not rename it.
2. On https://github.com/Waqas01CP/portfolio-gallery, **Add file**,
   **Create new file**, named `showcase/waqas01cp/entry.json`, holding:

```
{"name": "Your name as the card should show it", "url": "https://waqas01cp.github.io/", "description": "One line, at most 120 characters, or leave the field out."}
```

   **Commit changes**, choose **Create a new branch**, name it
   `showcase-waqas01cp`, **Propose changes**. Do not create the pull
   request yet.
3. Switch to the `showcase-waqas01cp` branch, open `showcase/waqas01cp/`,
   **Add file**, **Upload files**, add the screenshot as saved, and commit
   it directly to that branch.
4. Open https://github.com/Waqas01CP/portfolio-gallery/compare/main...showcase-waqas01cp,
   **Create pull request**. The description opens with two sections: keep
   **A showcase entry**, tick its three lines, delete **A design**, write
   `[scope: as contributor]` below them, and **Create pull request**.

You should see **scope** pass, its summary "In scope: 2 file(s), all in
showcase/waqas01cp/.", and **checks** pass, its step "Fetch the showcase
sites this pull request adds or changes" saying "ok
https://waqas01cp.github.io/ answers 200 with a web page linking to
github.com/waqas01cp", and its step "Run every check" making the
showcase's served copies: "card.webp" and "full.webp" for
showcase/waqas01cp, with their sizes.

5. Merge. When Deploy is green, open
   https://waqas01cp.github.io/portfolio-gallery/#showcase: one site, your
   card, the screenshot whole; a click on it opens the larger copy over
   the page, closed by its X, by Escape or by a click outside it.
6. **Actions**, **Showcase links**, **Run workflow**, branch `main`, **Run
   workflow**. You should see it pass, its log listing one entry and its
   response.

**Send back:** the scope and checks results, the gallery's Showcase
section, and the Showcase links run.

## The weekly showcase check

`.github/workflows/showcase-links.yml` fetches every showcase site and
every design's "In use" link each Monday at 06:17 UTC, and holds no
permissions: it edits nothing and opens nothing (ADR-0016). When it
fails, its summary lists the entries, and GitHub notifies the user who
last changed the workflow's cron line, which is you: open each site by
hand, then remove an entry that is gone by a pull request of your own.

GitHub disables a schedule in a public repository after 60 days without
activity there ("Events that trigger workflows", read 2026-10-19). After
a quiet spell, open **Actions**, **Showcase links**, and enable it again;
**Run workflow** checks at once.

## The weekly check of every page

A pull request's checks look only at the pages it alters (ADR-0019).
`.github/workflows/checks-weekly.yml` checks every page of the default
branch each Monday at 04:41 UTC, so a fault that reaches an unchanged page
from outside, such as a newer Chrome on GitHub's runner, shows within a
week. It holds no permissions and blocks nothing. When it fails, GitHub
notifies the user who last changed its cron line, which is you: open the
run, and fix the design it names by a pull request of your own. To check
every page at any time: **Actions**, **Checks** or **Checks, every
page**, **Run workflow**. Like the showcase check, GitHub disables its
schedule after 60 days without activity; enable it the same way.

A run of **Checks** is several jobs side by side (ADR-0019, Changes,
2026-10-29): **plan**, **files**, a **browser** job for each design it
checks, **gallery-page**, and last **checks**, the one the ruleset
requires, which fails unless every other part passed. When a run fails,
open it: the failed job is marked, and its last step names the problem.

## What the tests prove, and what they do not

- Test 1 proves the scope check runs from the default branch and refuses a
  change outside designs/, and that a failed required check blocks a merge.
  It proves step 5's policy only when run on or after 2026-11-02: until
  then GitHub only evaluates its block on `pull_request_target`, so the
  scope check runs with or without the policy. Run Test 1 once more on or
  after that date; scope must run and fail as before.
- Test 2 proves a design passes the scope check and the full checks on
  GitHub's runner, browser checks included.
- Test 3 proves the ruleset binds main.
- Test 4 proves a copy of the template publishes its owner's site in site
  mode, and shows whether a copy's first commit runs its workflows.
- Test 5 proves a copy cleans itself up once and still builds and checks,
  and shows whether a workflow's own token may delete workflow files. On
  2026-10-18 it did: the copy kept 52 files, and its `.github/` only
  checks.yml and deploy.yml. In this repository, the cleanup's run on main
  after it merged showed its job skipped.
- Test 6 proves a showcase entry passes the scope check as an outsider's
  and has its site fetched on GitHub's runner, that the gallery shows it,
  and that the weekly check runs with no permissions. It does not prove
  the check refuses a bad entry there: tools/prove_checks.py does, locally,
  with a defeat case for each rule.
- Step 8 proved the deploy, the screenshots and the addressing, in gallery
  mode.
- None of them is a fork from another account. The approval setting of
  step 4 shows itself on the first real contributor's pull request, as
  "Awaiting approval" on the checks; the scope check runs without waiting.
