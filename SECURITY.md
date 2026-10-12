<!--
type: reference
description: How to report a security problem in portfolio-gallery privately, what counts as one, and what happens next.
status: current
-->

# Security

## Reporting a problem

Please report a security problem privately, never in a public issue or
pull request:

1. Open this repository's **Security** tab.
2. Click **Report a vulnerability**.
3. Describe what you found, how to reproduce it, and what it lets someone
   do.

The report reaches only the maintainer. GitHub's own guide to this:
https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-a-vulnerability/privately-reporting-a-security-vulnerability

## What counts

Anything that lets a contribution do more than the design format allows,
for example:

- a design, or a pull request, that runs code on GitHub's runners or in a
  visitor's browser;
- a way past the scope check, the design checks or the page's
  Content-Security-Policy;
- a built site that requests anything from another origin, sets a cookie
  or stores anything on a visitor's device;
- a workflow that can be made to publish something it did not build and
  check.

How the project defends against these, and what it cannot promise, is in
[docs/decisions/0006-design-format-and-security-model.md](docs/decisions/0006-design-format-and-security-model.md).

## What happens next

The maintainer confirms the report, fixes it in a private advisory where
it needs one, and credits you in the advisory unless you ask otherwise.
