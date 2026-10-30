"""Each template's and showcase site's likes, from GitHub Discussions (ADR-0021).

  python tools/likes.py --out likes.json [--no-create] [--api URL]

The gallery's like button is a post in the repository's Discussions, in
the category named Likes, one per template and per showcase site: an
upvote or a 👍 on the post is a like, the two added together, since a
visitor reaches for either (the owner's choice, ADR-0021, Changes). This tool, run by the deploy workflow before the
gallery is built, makes the post for any template or site that has none,
counts each post's upvotes and 👍, rewrites the text of any post of its
own that still says otherwise, and writes likes.json for build.py --likes:

  {"designs/frost": {"url": "https://github.com/.../discussions/7", "likes": 3}}

A post counts only if the workflow's own account or the repository's
owner wrote it, so a look-alike post by anyone else is ignored; each post
carries its item in a marker, never matched by title. GitHub allows one
upvote and one 👍 per account, so one person counts at most twice. Names reach GitHub as GraphQL variables and only in
titles, which notify no one.

The page itself makes no request: the counts are written into its HTML
when it is built, so they change when the gallery is next published
(scope floor lines 2 and 3). A problem with Discussions never stops a
publish: it is reported as a warning, likes.json is written empty, and
each card links to the Likes category with no count.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATEGORY = "Likes"
MARKER = re.compile(r"<!-- portfolio-gallery likes: ((?:designs|showcase)/[a-z0-9-]+) -->")
WORKFLOW = {"github-actions", "github-actions[bot]"}

REPOSITORY = """query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    id hasDiscussionsEnabled
    discussionCategories(first: 100) { nodes { id name } }
  }
}"""
POSTS = """query($owner: String!, $name: String!, $category: ID!, $after: String) {
  repository(owner: $owner, name: $name) {
    discussions(first: 100, categoryId: $category, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes { id number url body upvoteCount author { login } reactionGroups { content reactors { totalCount } } }
    }
  }
}"""
REWRITE = """mutation($id: ID!, $body: String!) {
  updateDiscussion(input: {discussionId: $id, body: $body}) { discussion { number } }
}"""
CREATE = """mutation($repository: ID!, $category: ID!, $title: String!, $body: String!) {
  createDiscussion(input: {repositoryId: $repository, categoryId: $category, title: $title, body: $body}) {
    discussion { number url }
  }
}"""


class Trouble(Exception):
    """Discussions cannot be read or written; the gallery is built without counts."""


def items() -> dict[str, tuple[str, str]]:
    """Every template and showcase site: key -> (title, what a like likes)."""
    found = {}
    for path in sorted((ROOT / "designs").glob("*/design.json")):
        name = json.loads(path.read_text(encoding="utf-8"))["name"]
        found[f"designs/{path.parent.name}"] = (f"{name} (template)", "this template")
    for path in sorted((ROOT / "showcase").glob("*/entry.json")):
        name = json.loads(path.read_text(encoding="utf-8"))["name"]
        found[f"showcase/{path.parent.name}"] = (f"{name} (showcase)", "this portfolio site")
    return found


def text(what: str, key: str) -> str:
    """A post's text: how to like, and the marker naming its item."""
    return (f"To like {what}, click the upvote arrow beside this post, or give it a 👍. "
            f"The gallery counts both when it is next published.\n\n"
            f"<!-- portfolio-gallery likes: {key} -->")


def graphql(api: str, token: str, query: str, variables: dict) -> dict:
    request = urllib.request.Request(
        f"{api}/graphql", data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "portfolio-gallery-likes"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            answer = json.load(response)
    except (urllib.error.URLError, OSError, ValueError) as error:
        raise Trouble(f"GitHub's API did not answer: {error}") from None
    if answer.get("errors"):
        raise Trouble("GitHub's API refused: " + "; ".join(e.get("message", "?") for e in answer["errors"]))
    return answer["data"]


def likes(api: str, token: str, repository: str, owner: str, create: bool) -> dict[str, dict]:
    login, _, name = repository.partition("/")
    where = {"owner": login, "name": name}
    repo = graphql(api, token, REPOSITORY, where)["repository"]
    if not repo["hasDiscussionsEnabled"]:
        raise Trouble("Discussions are off in this repository")
    category = next((c["id"] for c in repo["discussionCategories"]["nodes"] if c["name"] == CATEGORY), None)
    if not category:
        raise Trouble(f"no discussion category named {CATEGORY}")
    posts, after = {}, None
    while True:
        page = graphql(api, token, POSTS, {**where, "category": category, "after": after})
        found = page["repository"]["discussions"]
        for post in found["nodes"]:
            mark = MARKER.search(post.get("body") or "")
            author = (post.get("author") or {}).get("login")
            # Only the workflow's own posts and the owner's count; the
            # first made wins if there are two.
            if not mark or author not in WORKFLOW | {owner}:
                continue
            key = mark.group(1)
            if key in posts and posts[key]["number"] < post["number"]:
                continue
            thumbs = next((g["reactors"]["totalCount"] for g in post["reactionGroups"]
                           if g["content"] == "THUMBS_UP"), 0)
            posts[key] = {"id": post["id"], "number": post["number"], "url": post["url"],
                          "likes": post["upvoteCount"] + thumbs, "body": post.get("body") or "",
                          "own": author in WORKFLOW}
        if not found["pageInfo"]["hasNextPage"]:
            break
        after = found["pageInfo"]["endCursor"]
    counted = {}
    for key, (title, what) in items().items():
        if key not in posts and create:
            body = text(what, key)
            # One post that cannot be made leaves the others counted.
            try:
                made = graphql(api, token, CREATE, {"repository": repo["id"], "category": category,
                                                     "title": title, "body": body})["createDiscussion"]["discussion"]
            except Trouble as trouble:
                print(f"::warning::likes: could not make the post for {key}: {trouble}")
                continue
            posts[key] = {"number": made["number"], "url": made["url"], "likes": 0}
            print(f"likes: created the post for {key}, post {made['number']}")
        # A post of the workflow's own whose text says otherwise, as the
        # first ones said a 👍 alone, is rewritten; the owner's are his.
        elif (key in posts and posts[key]["own"] and create
              and posts[key]["body"].replace("\r\n", "\n").strip() != text(what, key)):
            try:
                graphql(api, token, REWRITE, {"id": posts[key]["id"], "body": text(what, key)})
                print(f"likes: rewrote the text of the post for {key}, post {posts[key]['number']}")
            except Trouble as trouble:
                print(f"::warning::likes: could not rewrite the post for {key}: {trouble}")
        if key in posts:
            counted[key] = {"url": posts[key]["url"], "likes": posts[key]["likes"]}
            print(f"likes: {key}: {posts[key]['likes']} like(s), post {posts[key]['number']}")
    return counted


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Each template's and showcase site's likes, from Discussions.")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--no-create", action="store_true", help="count only; make no post")
    parser.add_argument("--api", default=os.environ.get("GITHUB_API_URL", "https://api.github.com"))
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(errors="backslashreplace")
    token, repository = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY", "")
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER") or repository.partition("/")[0]
    try:
        if not token or "/" not in repository:
            raise Trouble("no GITHUB_TOKEN or GITHUB_REPOSITORY; run by the deploy workflow")
        counted = likes(args.api.rstrip("/"), token, repository, owner, not args.no_create)
    except Trouble as trouble:
        counted = {}
        print(f"::warning::likes: {trouble}. The gallery is built without counts, each card linking "
              f"to the category {CATEGORY}. To count likes, turn Discussions on and add the category "
              f"(docs/setup-on-github.md, ADR-0021).")
    args.out.write_text(json.dumps(counted, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"likes: {len(counted)} item(s) written to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
