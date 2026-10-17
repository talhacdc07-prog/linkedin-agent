# LinkedIn Agent

Bu proje GitHub hesabındaki projeleri her gün kontrol eder. O gün commit veya
proje ilerlemesi varsa bunun üzerinden LinkedIn'de paylaşmaya hazır tek bir
gönderi taslağı üretir; hiç ilerleme yoksa gönderi üretmez.

## Klasör yapısı

```text
linkedin-agent/
├── agents/
│   ├── github_activity.py
│   ├── github_analyzer.py
│   └── linkedin_writer.py
├── output/
└── .github/
    └── workflows/
        └── linkedin-agent.yml
```

## Günlük çalışma

GitHub Actions workflow'u her gün 18:00 UTC'de çalışır. `GITHUB_OWNER`
değeri workflow içinde ayarlanmıştır. Public repository'lere ek olarak private
repository'leri tarayabilmesi için GitHub repository secrets bölümünde
`GH_READ_TOKEN` adlı, yalnızca okuma yetkili bir GitHub token'ı bulunmalıdır.
O gün hiçbir repository'de commit yoksa workflow başarılı şekilde tamamlanır
ama LinkedIn taslağı oluşturmaz.

## Yerel çalıştırma

```powershell
python agents/github_activity.py
python agents/linkedin_writer.py
Get-Content output/linkedin_post.md
```

İlk komut `output/github_activity.json`, ikinci komut ise yalnızca aktivite
varsa `output/linkedin_post.md` dosyasını oluşturur.

### Private repository erişimi

GitHub'da **Settings > Developer settings > Personal access tokens** bölümünden
fine-grained bir token oluşturun. Token'ı gerekli private repository'lere
verin ve en azından **Contents: Read-only** ile **Metadata: Read-only**
izinlerini seçin. Token'ı repository secrets bölümünde şu adla kaydedin:

```text
GH_READ_TOKEN
```

Token'ı koda veya workflow dosyasına yazmayın. Token eklenmezse public
repository'ler yine taranabilir, private repository'ler taranamaz.

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
