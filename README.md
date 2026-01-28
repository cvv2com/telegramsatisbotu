# 🎁 Telegram Gift Card Satış Botu

Telegram üzerinden gift card satışı yapabileceğiniz, kolay kullanımlı bir bot.

## ✨ Özellikler

- 🎁 Gift card listeleme ve kategorilere ayırma
- 💳 Kolay satın alma işlemi
- 👤 Kullanıcı dostu arayüz
- ⚙️ Admin paneli ile yönetim
- 📊 Satış istatistikleri
- 🔒 Güvenli kod paylaşımı
- 📱 Telegram'ın tüm özelliklerini kullanma

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- Telegram Bot Token (@BotFather'dan alınacak)

### Adım 1: Repoyu klonlayın

```bash
git clone https://github.com/cvv2com/telegramsatisbotu.git
cd telegramsatisbotu
```

### Adım 2: Sanal ortam oluşturun (önerilir)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### Adım 3: Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: Ortam değişkenlerini ayarlayın

1. `.env.example` dosyasını `.env` olarak kopyalayın:
```bash
cp .env.example .env
```

2. `.env` dosyasını düzenleyin ve kendi bilgilerinizi girin:
```
TELEGRAM_BOT_TOKEN=sizin_bot_token_burada
ADMIN_IDS=sizin_telegram_id,diger_admin_id
```

**Not:** Telegram ID'nizi öğrenmek için [@userinfobot](https://t.me/userinfobot) kullanabilirsiniz.

### Adım 5: Botu başlatın

```bash
python bot.py
```

## 📖 Kullanım

### Kullanıcılar için

1. Botu Telegram'da açın ve `/start` komutunu gönderin
2. "🎁 Gift Card'ları Görüntüle" veya "📂 Kategoriler" butonlarını kullanın
3. Beğendiğiniz gift card'ı seçin
4. "Satın Al" butonuna tıklayın
5. Onaylayın ve kodunuzu alın! 🎉

### Adminler için

#### Admin paneline erişim

1. `/start` komutuyla botu başlatın
2. "⚙️ Admin Panel" butonuna tıklayın

#### Yeni gift card ekleme

Komut formatı:
```
/addcard <isim> | <açıklama> | <fiyat> | <kategori> | <kod> | [resim_url]
```

Örnek:
```
/addcard Steam 100TL | Steam cüzdanınıza 100TL yükleyin | 95 | Steam | XXXX-YYYY-ZZZZ | https://example.com/image.jpg
```

**Parametreler:**
- `isim`: Gift card adı (ör: Steam 100TL)
- `açıklama`: Kısa açıklama
- `fiyat`: Satış fiyatı (sadece rakam)
- `kategori`: Kategori adı (ör: Steam, Netflix, Spotify)
- `kod`: Gift card kodu
- `resim_url`: (Opsiyonel) Ürün görseli URL'si

#### Diğer admin işlemleri

- **Tüm kartları listele**: Admin panelinden "📋 Tüm Kartları Listele" seçeneğini kullanın
- **Kart silme**: Listeleme ekranında her kartın yanındaki "🗑️ Sil" butonunu kullanın
- **İstatistikler**: Admin panelinden "📊 İstatistikler" seçeneğini kullanın

## 🔧 Yapılandırma

### config.py

Temel yapılandırma ayarları `config.py` dosyasında bulunur:

- `BOT_TOKEN`: Telegram bot token
- `ADMIN_IDS`: Admin kullanıcı ID listesi
- `DATABASE_FILE`: Veritabanı dosya adı
- `CURRENCY`: Para birimi simgesi

## 📁 Proje Yapısı

```
telegramsatisbotu/
├── bot.py              # Ana bot dosyası
├── config.py           # Yapılandırma ayarları
├── database.py         # Veritabanı yönetimi
├── requirements.txt    # Python bağımlılıkları
├── .env.example        # Örnek ortam değişkenleri
├── .gitignore         # Git ignore dosyası
└── README.md          # Bu dosya
```

## 💾 Veritabanı

Bot, JSON tabanlı basit bir veritabanı kullanır (`gift_cards.json`). Bu dosya otomatik olarak oluşturulur ve aşağıdaki bilgileri içerir:

- Gift card bilgileri
- Kategoriler
- Sipariş geçmişi

## 🔒 Güvenlik

- Admin komutları sadece `ADMIN_IDS` listesindeki kullanıcılar tarafından kullanılabilir
- Gift card kodları sadece satın alma sonrasında paylaşılır
- Bot token ve admin ID'leri ortam değişkenlerinde saklanır

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

## 📝 Lisans

Bu proje açık kaynaklıdır ve MIT lisansı altında lisanslanmıştır.

## ⚠️ Uyarı

Bu bot eğitim amaçlıdır. Gerçek para transferi için ödeme entegrasyonu eklemeniz önerilir.

## 📞 Destek

Herhangi bir sorunuz veya sorununuz varsa, lütfen bir issue açın.

## 🎯 Gelecek Özellikler

- [ ] Ödeme entegrasyonu (Stripe, PayPal, vs.)
- [ ] Otomatik stok yönetimi
- [ ] Toplu kart ekleme
- [ ] Kullanıcı sipariş geçmişi
- [ ] Kupon ve indirim kodları
- [ ] Çoklu dil desteği

---

Made with ❤️ for Telegram bot enthusiasts
