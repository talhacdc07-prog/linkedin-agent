"""Publish a generated post to LinkedIn through the official Posts API."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://api.linkedin.com/rest/posts"


def publish_post(post: str, access_token: str, author_urn: str, version: str) -> str:
    payload = {
        "author": author_urn,
        "commentary": post,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    request = Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "LinkedIn-Version": version,
            "X-Restli-Protocol-Version": "2.0.0",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            post_id = response.headers.get("x-restli-id", "")
            if response.status not in (200, 201):
                raise RuntimeError(f"LinkedIn returned unexpected HTTP status {response.status}")
            return post_id
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LinkedIn publish failed (HTTP {error.code}): {details}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach LinkedIn: {error.reason}") from error


def main() -> None:
    input_path = Path(os.environ.get("POST_INPUT", "output/linkedin_post.md"))
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    author_urn = os.environ.get("LINKEDIN_AUTHOR_URN")
    version = os.environ.get("LINKEDIN_VERSION", "202601")

    missing = [
        name
        for name, value in (
            ("LINKEDIN_ACCESS_TOKEN", access_token),
            ("LINKEDIN_AUTHOR_URN", author_urn),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing required environment variable(s): " + ", ".join(missing)
        )
    if not input_path.is_file():
        raise FileNotFoundError(f"Post file not found: {input_path}")

    post_id = publish_post(
        input_path.read_text(encoding="utf-8").strip(),
        access_token,
        author_urn,
        version,
    )
    print(f"LinkedIn post published successfully. Post ID: {post_id or 'not returned'}")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
