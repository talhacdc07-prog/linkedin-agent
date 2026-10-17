# LinkedIn Agent

Bu proje GitHub repository'sini analiz eder ve analiz sonucundan LinkedIn'de
paylaşmaya hazır bir gönderi taslağı üretir.

## Klasör yapısı

```text
linkedin-agent/
├── agents/
│   ├── github_analyzer.py
│   ├── linkedin_writer.py
│   └── linkedin_publisher.py
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
LinkedIn gönderisi üretilir ve resmi LinkedIn Posts API ile otomatik olarak
yayınlanır.

## LinkedIn kurulumu

1. LinkedIn Developer Portal'da bir uygulama oluşturun ve uygulamaya
   **Share on LinkedIn** ürününü ekleyin.
2. OAuth 2.0 ile bir kullanıcı erişim token'ı alın. Token'ın en azından
   `w_member_social` yetkisine sahip olması gerekir.
3. LinkedIn profil URN'inizi `urn:li:person:...` biçiminde belirleyin.
4. GitHub repository ayarlarında **Settings > Secrets and variables >
   Actions** bölümünde şu repository secrets değerlerini ekleyin:

   - `LINKEDIN_ACCESS_TOKEN`: LinkedIn OAuth access token
   - `LINKEDIN_AUTHOR_URN`: Gönderinin yayınlanacağı profil URN'i

   İsteğe bağlı repository variable:

   - `LINKEDIN_VERSION`: API sürümü; varsayılan `202601`

Token'ı dosyaya, workflow metnine veya commit'e yazmayın. Token süresi
dolduğunda yeni OAuth token alıp secret'ı güncelleyin.

Workflow başarısız olursa LinkedIn API'nin HTTP hata mesajını Actions log'unda
açıkça gösterir; eksik secret durumunda da yayınlama adımı hata ile durur.
