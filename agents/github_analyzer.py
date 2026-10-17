"""Analyze a repository and write a compact JSON summary."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


IGNORED_DIRECTORIES = {
    ".git",
    ".github",
    ".idea",
    ".pytest_cache",
    ".venv",
    "node_modules",
    "dist",
    "build",
    "output",
    "__pycache__",
}


def analyze_repo(repo: Path) -> dict[str, Any]:
    files: list[str] = []
    extensions: dict[str, int] = {}
    total_bytes = 0

    for path in repo.rglob("*"):
        if not path.is_file() or any(part in IGNORED_DIRECTORIES for part in path.parts):
            continue
        relative = path.relative_to(repo)
        files.append(relative.as_posix())
        suffix = path.suffix.lower() or "[no extension]"
        extensions[suffix] = extensions.get(suffix, 0) + 1
        try:
            total_bytes += path.stat().st_size
        except OSError:
            continue

    files.sort()
    languages = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".jsx": "JavaScript",
        ".java": "Java",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust",
        ".php": "PHP",
        ".rb": "Ruby",
        ".html": "HTML",
        ".css": "CSS",
    }
    language_counts: dict[str, int] = {}
    for extension, count in extensions.items():
        language = languages.get(extension)
        if language:
            language_counts[language] = language_counts.get(language, 0) + count

    return {
        "repository": repo.name,
        "file_count": len(files),
        "total_bytes": total_bytes,
        "top_languages": sorted(
            language_counts.items(), key=lambda item: (-item[1], item[0])
        ),
        "extensions": dict(sorted(extensions.items())),
        "sample_files": files[:20],
    }


def main() -> None:
    repo = Path(os.environ.get("REPO_PATH", ".")).resolve()
    output_path = Path(os.environ.get("ANALYSIS_OUTPUT", "output/repository_analysis.json"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = analyze_repo(repo)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Repository analyzed: {result['file_count']} files")
    print(f"Analysis written to: {output_path}")


if __name__ == "__main__":
    main()
