"""Create a LinkedIn-ready post from a repository analysis."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def create_post(analysis: dict[str, Any]) -> str:
    repository = analysis.get("repository", "projem")
    file_count = analysis.get("file_count", 0)
    languages = [name for name, _ in analysis.get("top_languages", [])[:3]]
    language_text = ", ".join(languages) if languages else "çeşitli teknolojiler"

    return f"""🚀 Yeni proje güncellemesi: {repository}

Bugün GitHub üzerindeki projemi geliştirmeye ve daha düzenli bir geliştirme
akışı kurmaya devam ettim.

📊 Proje özeti:
• {file_count} dosya analiz edildi
• Kullanılan teknolojiler: {language_text}
• Repository analizi ve LinkedIn içerik üretimi otomatikleştirildi

Bu çalışma sayesinde kod değişikliklerini daha anlaşılır şekilde paylaşmayı,
öğrenme sürecimi kayıt altına almayı ve sürekli geliştirmeyi hedefliyorum.

Öğrenmeye ve üretmeye devam ediyorum. 💪

#Python #GitHub #YazılımGeliştirme #Automation #LearningInPublic
"""


def main() -> None:
    analysis_path = Path(os.environ.get("ANALYSIS_INPUT", "output/repository_analysis.json"))
    output_path = Path(os.environ.get("POST_OUTPUT", "output/linkedin_post.md"))
    if not analysis_path.is_file():
        raise FileNotFoundError(f"Analysis file not found: {analysis_path}")

    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(create_post(analysis), encoding="utf-8")
    print(f"LinkedIn post written to: {output_path}")


if __name__ == "__main__":
    main()
