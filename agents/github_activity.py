"""Collect the owner's recent GitHub activity across repositories."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_ROOT = "https://api.github.com"


def github_get(path: str, token: str | None) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "linkedin-agent",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(
        API_ROOT + path,
        headers=headers,
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API failed (HTTP {error.code}): {details}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach GitHub: {error.reason}") from error


def collect_activity(token: str, owner: str, since: datetime) -> dict[str, object]:
    repo_path = (
        "/user/repos?per_page=100&affiliation=owner&sort=pushed&direction=desc"
        if token
        else f"/users/{owner}/repos?per_page=100&type=owner&sort=pushed"
    )
    repos = github_get(repo_path, token)
    if not isinstance(repos, list):
        raise RuntimeError("GitHub returned an invalid repository list")

    projects: list[dict[str, object]] = []
    for repo in repos:
        if not isinstance(repo, dict) or repo.get("owner", {}).get("login") != owner:
            continue
        commits = github_get(
            f"/repos/{owner}/{repo['name']}/commits?author={owner}&since={since.isoformat()}&per_page=20",
            token,
        )
        if not isinstance(commits, list) or not commits:
            continue
        projects.append(
            {
                "name": repo["name"],
                "description": repo.get("description") or "",
                "commits": [
                    {
                        "message": item.get("commit", {}).get("message", "").splitlines()[0],
                        "sha": item.get("sha", ""),
                    }
                    for item in commits
                    if isinstance(item, dict)
                ],
            }
        )

    return {
        "date": since.date().isoformat(),
        "owner": owner,
        "projects": projects,
        "has_activity": bool(projects),
    }


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    owner = os.environ.get("GITHUB_OWNER")
    if not owner:
        raise RuntimeError("GITHUB_OWNER is required")

    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=24)
    output_path = Path(os.environ.get("ACTIVITY_OUTPUT", "output/github_activity.json"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(collect_activity(token, owner, since), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"GitHub activity written to {output_path}")


if __name__ == "__main__":
    main()
