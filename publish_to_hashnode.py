#!/usr/bin/env python3
"""
publish_to_hashnode.py — Publish blog posts to Hashnode via GraphQL API.

Usage:
    python blog/publish_to_hashnode.py --token <YOUR_API_TOKEN> --publication <PUBLICATION_ID>
    python blog/publish_to_hashnode.py  # prompts interactively

Prerequisites:
    1. Create a Hashnode account at hashnode.com
    2. Create a publication (blog) — note the publication ID from the URL
       e.g. https://hashnode.com/<username> → Settings → Publication ID shown there
    3. Generate an API token: hashnode.com/settings/developer → Personal Access Tokens → New Token

Finding your publication ID:
    - Go to your Hashnode blog settings
    - The publication ID is a 24-character hex string shown in the URL or Settings → General
    - Alternatively, use --find-publication to list all publications for your account

Posts are read from the blog/ directory (markdown files with YAML frontmatter).
Already-published posts are tracked in blog/.published.json to avoid duplicates.
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package not installed.")
    print("Run: pip install requests")
    sys.exit(1)

_HERE        = Path(__file__).parent
_PUBLISHED   = _HERE / ".published.json"
_API_URL     = "https://gql.hashnode.com"
_HEADERS_TPL = {"Authorization": "{token}", "Content-Type": "application/json"}

_PUBLISH_MUTATION = """
mutation PublishPost($input: PublishPostInput!) {
  publishPost(input: $input) {
    post {
      id
      title
      slug
      url
    }
  }
}
"""

_FIND_PUBLICATIONS = """
query {
  me {
    publications(first: 10) {
      edges {
        node {
          id
          title
          url
        }
      }
    }
  }
}
"""


# ── Frontmatter parser ─────────────────────────────────────────────────────────

def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML-style frontmatter from markdown. Returns (meta, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    front = text[3:end].strip()
    body  = text[end + 4:].strip()
    meta: dict = {}
    for line in front.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        val = val.strip().strip('"')
        if val.startswith("[") and val.endswith("]"):
            meta[key.strip()] = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",") if v.strip()]
        else:
            meta[key.strip()] = val
    return meta, body


def _load_posts() -> list[dict]:
    """Load all markdown files from the blog/ directory (skip this script and .published.json)."""
    posts = []
    for path in sorted(_HERE.glob("*.md")):
        if path.name.startswith("."):
            continue
        text = path.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(text)
        if not meta.get("title"):
            print(f"  SKIP {path.name} — no title in frontmatter")
            continue
        posts.append({
            "file":     path.name,
            "title":    meta.get("title", ""),
            "subtitle": meta.get("subtitle", ""),
            "tags":     meta.get("tags", []),
            "body":     body,
        })
    return posts


def _load_published() -> dict:
    if _PUBLISHED.exists():
        return json.loads(_PUBLISHED.read_text(encoding="utf-8"))
    return {}


def _save_published(published: dict) -> None:
    _PUBLISHED.write_text(json.dumps(published, indent=2), encoding="utf-8")


# ── API calls ──────────────────────────────────────────────────────────────────

def _gql(token: str, query: str, variables: dict | None = None) -> dict:
    headers = {**_HEADERS_TPL, "Authorization": token}
    payload: dict = {"query": query}
    if variables:
        payload["variables"] = variables
    r = requests.post(_API_URL, headers=headers, json=payload, timeout=30)
    if not r.text.strip():
        raise RuntimeError(
            f"Hashnode API returned HTTP {r.status_code} with an empty body.\n"
            "  → Check that your API token is correct and has not expired.\n"
            "  → Token must be a Personal Access Token from hashnode.com/settings/developer"
        )
    if r.status_code != 200:
        raise RuntimeError(f"Hashnode API HTTP {r.status_code}: {r.text[:400]}")
    data = r.json()
    if "errors" in data:
        msgs = "; ".join(e.get("message", str(e)) for e in data["errors"])
        raise RuntimeError(f"Hashnode API error: {msgs}")
    return data


def find_publications(token: str) -> None:
    data = _gql(token, _FIND_PUBLICATIONS)
    edges = data.get("data", {}).get("me", {}).get("publications", {}).get("edges", [])
    if not edges:
        print("  No publications found for this account.")
        return
    print("\n  Your Hashnode publications:")
    print("  " + "-" * 60)
    for edge in edges:
        node = edge["node"]
        print(f"  ID    : {node['id']}")
        print(f"  Title : {node['title']}")
        print(f"  URL   : {node['url']}")
        print()


def publish_post(token: str, publication_id: str, post: dict) -> dict:
    tags = [{"name": t, "slug": t.lower().replace(" ", "-")} for t in post.get("tags", [])]
    variables = {
        "input": {
            "title":         post["title"],
            "subtitle":      post.get("subtitle", ""),
            "contentMarkdown": post["body"],
            "publicationId": publication_id,
            "tags":          tags,
        }
    }
    data = _gql(token, _PUBLISH_MUTATION, variables)
    return data["data"]["publishPost"]["post"]


# ── Interactive prompt ─────────────────────────────────────────────────────────

def _prompt(label: str, secret: bool = False) -> str:
    if secret:
        import getpass
        return getpass.getpass(f"  {label}: ").strip()
    return input(f"  {label}: ").strip()


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish blog/ markdown files to Hashnode",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--token",       help="Hashnode Personal Access Token")
    parser.add_argument("--publication", help="Hashnode Publication ID (24-char hex)")
    parser.add_argument("--find-publication", action="store_true",
                        help="List all publications for this account, then exit")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be published without actually publishing")
    parser.add_argument("--force", action="store_true",
                        help="Re-publish posts that were already published")
    args = parser.parse_args()

    print()
    print("  Personal Portfolio Tracker — Hashnode Publisher")
    print("  " + "-" * 50)

    token = args.token or _prompt("Hashnode API token", secret=True)
    if not token:
        print("  ERROR: token is required.")
        sys.exit(1)

    if args.find_publication:
        find_publications(token)
        return

    publication_id = args.publication or _prompt("Publication ID")
    if not publication_id:
        print("  ERROR: publication ID is required.")
        print("  Use --find-publication to list your publications.")
        sys.exit(1)

    posts     = _load_posts()
    published = _load_published()

    if not posts:
        print("  No posts found in blog/ directory.")
        return

    print(f"\n  Found {len(posts)} post(s):\n")
    for p in posts:
        status = "[done]" if (p["file"] in published and not args.force) else "[publish]"
        print(f"  {status}  {p['file']}")
        print(f"             {p['title']}")
    print()

    if args.dry_run:
        print("  --dry-run: no posts published.")
        return

    confirm = input("  Publish now? [Y/n]: ").strip().lower()
    if confirm == "n":
        print("  Aborted.")
        return

    print()
    results = []
    for post in posts:
        if post["file"] in published and not args.force:
            print(f"  SKIP   {post['file']} (already published — use --force to re-publish)")
            continue
        print(f"  POST   {post['title']} … ", end="", flush=True)
        try:
            result = publish_post(token, publication_id, post)
            published[post["file"]] = {
                "id":          result["id"],
                "url":         result["url"],
                "slug":        result["slug"],
                "published_at": date.today().isoformat(),
            }
            _save_published(published)
            print(f"✅  {result['url']}")
            results.append((post["file"], result["url"]))
        except Exception as e:
            print(f"❌  ERROR: {e}")

    if results:
        print()
        print("  Published posts:")
        for fname, url in results:
            print(f"    {fname}")
            print(f"    → {url}")
    print()


if __name__ == "__main__":
    main()
