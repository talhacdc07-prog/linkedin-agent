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

    return f"""🚀 Agent'larla geliştirdiğim ilk GitHub projemi yayınladım!

Bugün GitHub üzerinde {repository} adlı projemi oluşturdum ve bu projeyi
agent'larla birlikte geliştirerek çalışan bir otomasyon akışı kurdum.

📊 Proje özeti:
• {file_count} dosya analiz edildi
• Kullanılan teknoloji: {language_text}
• GitHub repository analizi otomatikleştirildi
• Proje güncellemesinden LinkedIn gönderisi üretme akışı oluşturuldu

Bu benim agent'ları kullanarak hazırladığım ilk proje. Kod yazma, dosya yapısını
oluşturma, GitHub Actions workflow'unu hazırlama ve içerik üretme süreçlerinde
agent'lardan faydalandım.

Yazılım geliştirirken yapay zekâ destekli araçları daha bilinçli kullanmayı ve
üretmeye devam etmeyi öğreniyorum. 💪

#Python #GitHub #YazılımGeliştirme #AI #Automation #LearningInPublic
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
