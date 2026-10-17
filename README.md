# LinkedIn Agent

Bu proje GitHub repository'sini analiz eder ve analiz sonucundan LinkedIn'de
paylaşmaya hazır bir gönderi taslağı üretir.

## Klasör yapısı

```text
linkedin-agent/
├── agents/
│   ├── github_analyzer.py
│   └── linkedin_writer.py
├── output/
└── .github/
    └── workflows/
        └── linkedin-agent.yml
```

## Yerel çalıştırma

Repository kökünde:

```powershell
python agents/github_analyzer.py
python agents/linkedin_writer.py
Get-Content output/linkedin_post.md
```

İlk komut `output/repository_analysis.json`, ikinci komut ise
`output/linkedin_post.md` dosyasını oluşturur.

## GitHub Actions

Workflow `main` branch'ine yapılan her push'ta veya GitHub Actions ekranındaki
**Run workflow** seçeneğiyle çalışır. Önce repository analiz edilir, sonra
LinkedIn gönderisi üretilir ve Actions özetinde gösterilir. Özet içindeki
bağlantıyla mevcut kişisel LinkedIn hesabının paylaşım ekranını açıp gönderiyi
onaylayarak yayınlarsınız.

## Kullanım

1. GitHub'a push yapın veya Actions içinden workflow'u manuel çalıştırın.
2. **Actions > LinkedIn Agent** içinden tamamlanan çalışmayı açın.
3. Gönderi taslağını **Summary** bölümünden kopyalayın.
4. Aynı bölümdeki LinkedIn bağlantısını açın, metni yapıştırın ve **Post**
   düğmesine basın.

Bu akış yeni LinkedIn hesabı veya şirket sayfası gerektirmez. GitHub Actions
sunucusu sizin bilgisayarınızın tarayıcısını açamayacağı için son paylaşım
onayı mevcut kişisel hesabınızda manuel verilir. LinkedIn access token,
şifre veya Developer uygulaması eklemeniz gerekmez.
