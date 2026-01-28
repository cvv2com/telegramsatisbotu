# 🎁 Telegram Gift Card Satış Botu / Telegram Gift Card Sales Bot

Telegram üzerinden gift card satışı yapabileceğiniz, kolay kullanımlı bir bot.

A user-friendly bot for selling gift cards on Telegram.

## ✨ Özellikler / Features

- 🌐 **Multi-language support** (Türkçe / English)
- 🎁 Gift card listeleme ve kategorilere ayırma / List gift cards by categories
- 💳 Kolay satın alma işlemi / Easy purchase process
- 📦 **Automatic stock management** with low stock alerts
- 🎫 **Coupon and discount codes** support
- 📋 **Bulk card addition** via CSV/JSON files
- 📜 **User order history** tracking
- 💰 **Payment integration** (PayPal, Crypto: BTC/ETH/LTC)
- 👤 Kullanıcı dostu arayüz / User-friendly interface
- ⚙️ Admin paneli ile yönetim / Admin panel management
- 📊 Satış istatistikleri / Sales statistics
- 🔒 Güvenli kod paylaşımı / Secure code sharing
- 📱 Telegram'ın tüm özelliklerini kullanma / Full Telegram features

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

# Payment Configuration (Optional)
PAYPAL_EMAIL=your_paypal_email@example.com
BTC_WALLET=your_bitcoin_wallet_address
ETH_WALLET=your_ethereum_wallet_address
LTC_WALLET=your_litecoin_wallet_address

# Stock Management
LOW_STOCK_THRESHOLD=5
```

**Not:** Telegram ID'nizi öğrenmek için [@userinfobot](https://t.me/userinfobot) kullanabilirsiniz.

### Adım 5: Botu başlatın

**Kolay Yol (Otomatik):**

Linux/Mac:
```bash
./start.sh
```

Windows:
```
start.bat
```

Bu scriptler otomatik olarak:
- Sanal ortam oluşturur
- Bağımlılıkları yükler
- .env kontrolü yapar
- Botu başlatır

**Manuel Yol:**

```bash
python bot.py
```

## 📖 Kullanım / Usage

### Kullanıcılar için / For Users

1. Botu Telegram'da açın ve `/start` komutunu gönderin / Open the bot on Telegram and send `/start`
2. Dil seçimi yapın (🇹🇷 Türkçe / 🇬🇧 English) / Select your language
3. "🎁 Gift Card'ları Görüntüle" veya "📂 Kategoriler" butonlarını kullanın / Use "View Gift Cards" or "Categories" buttons
4. Beğendiğiniz gift card'ı seçin / Select your preferred gift card
5. "Satın Al" butonuna tıklayın / Click "Buy Now"
6. İndirim kodunuz varsa girin / Enter discount code if you have one
7. Ödeme yöntemini seçin / Choose payment method
8. Onaylayın ve kodunuzu alın! 🎉 / Confirm and get your code!

### Kullanıcı Komutları / User Commands

- `/start` - Botu başlat / Start the bot
- `/help` - Yardım mesajını göster / Show help message
- `/myorders` - Sipariş geçmişimi göster / View order history
- `/language` - Dil değiştir / Change language

### Adminler için / For Admins

#### Admin paneline erişim / Admin Panel Access

1. `/start` komutuyla botu başlatın / Start the bot with `/start`
2. "⚙️ Admin Panel" butonuna tıklayın / Click "Admin Panel" button

#### Yeni gift card ekleme / Adding New Gift Cards

Komut formatı / Command format:
```
/addcard <isim> | <açıklama> | <fiyat> | <kategori> | <kod> | <stok>
/addcard <name> | <description> | <price> | <category> | <code> | <stock>
```

Örnek / Example:
```
/addcard Steam 100TL | Steam cüzdanınıza 100TL yükleyin | 95 | Steam | XXXX-YYYY-ZZZZ | 10
/addcard Netflix 10$ | 1 Month Subscription | 10 | Entertainment | NF-12345 | 5
```

**Parametreler / Parameters:**
- `isim/name`: Gift card adı / Gift card name
- `açıklama/description`: Kısa açıklama / Short description
- `fiyat/price`: Satış fiyatı (sadece rakam) / Sale price (number only)
- `kategori/category`: Kategori adı / Category name
- `kod/code`: Gift card kodu / Gift card code
- `stok/stock`: Stok miktarı / Stock quantity (default: 1)

#### Toplu kart ekleme / Bulk Card Addition

Komut / Command:
```
/bulkaddcard
```

Sonra CSV veya JSON dosyası gönderin / Then send a CSV or JSON file:

**CSV Format:**
```csv
name,description,price,category,code,stock
Netflix 10$,1 Month,10,Entertainment,NF-123,5
Steam 20$,Steam Wallet,20,Gaming,ST-456,10
```

**JSON Format:**
```json
[
  {
    "name": "Netflix 10$",
    "description": "1 Month",
    "price": 10,
    "category": "Entertainment",
    "code": "NF-123",
    "stock": 5
  }
]
```

#### Kupon oluşturma / Creating Coupons

Komut formatı / Command format:
```
/addcoupon <kod> | <tip> | <değer> | <max_kullanım> | <gün>
/addcoupon <code> | <type> | <value> | <max_uses> | <days>
```

Örnek / Example:
```
/addcoupon YENI2024 | percentage | 10 | 100 | 30
/addcoupon NEW2024 | percentage | 10 | 100 | 30
```

**Parametreler / Parameters:**
- `tip/type`: `percentage` (yüzde) veya `fixed` (sabit tutar)
- `değer/value`: İndirim miktarı / Discount amount
- `max_kullanım/max_uses`: Maksimum kullanım sayısı / Maximum number of uses (optional)
- `gün/days`: Geçerlilik süresi (gün) / Validity period in days (optional)

#### Diğer admin komutları / Other Admin Commands

- `/deletecard <ID>` - Kart silme / Delete card
- `/deletecoupon <ID>` - Kupon silme / Delete coupon
- **Tüm kartları listele / List all cards**: Admin panelinden / From admin panel
- **İstatistikler / Statistics**: Admin panelinden / From admin panel

## 🔧 Yapılandırma / Configuration

### config.py

Temel yapılandırma ayarları `config.py` dosyasında bulunur / Basic configuration settings are in `config.py`:

- `BOT_TOKEN`: Telegram bot token
- `ADMIN_IDS`: Admin kullanıcı ID listesi / Admin user ID list
- `DATABASE_FILE`: Veritabanı dosya adı / Database file name
- `CURRENCY`: Para birimi simgesi / Currency symbol
- `PAYPAL_EMAIL`: PayPal hesabı / PayPal account (optional)
- `CRYPTO_WALLETS`: Kripto para cüzdan adresleri / Crypto wallet addresses (optional)
- `LOW_STOCK_THRESHOLD`: Düşük stok uyarı eşiği / Low stock alert threshold

## 📁 Proje Yapısı / Project Structure

```
telegramsatisbotu/
├── bot.py              # Ana bot dosyası / Main bot file
├── config.py           # Yapılandırma ayarları / Configuration settings
├── database.py         # Veritabanı yönetimi / Database management
├── translations.py     # Çoklu dil desteği / Multi-language support
├── requirements.txt    # Python bağımlılıkları / Python dependencies
├── .env.example        # Örnek ortam değişkenleri / Example environment variables
├── .gitignore         # Git ignore dosyası / Git ignore file
└── README.md          # Bu dosya / This file
```

## 💾 Veritabanı / Database

Bot, JSON tabanlı basit bir veritabanı kullanır (`gift_cards.json`). Bu dosya otomatik olarak oluşturulur ve aşağıdaki bilgileri içerir:

The bot uses a simple JSON-based database (`gift_cards.json`). This file is automatically created and contains:

- Gift card bilgileri / Gift card information
- Kategoriler / Categories
- Sipariş geçmişi / Order history
- Kuponlar / Coupons
- Kullanıcı tercihleri (dil) / User preferences (language)

## 🔒 Güvenlik / Security

- Admin komutları sadece `ADMIN_IDS` listesindeki kullanıcılar tarafından kullanılabilir / Admin commands can only be used by users in the `ADMIN_IDS` list
- Gift card kodları Telegram'ın spoiler özelliği ile gizli olarak paylaşılır / Gift card codes are shared securely using Telegram's spoiler feature
- Kodlar satın alma sonrasında paylaşılır / Codes are shared after purchase
- Bot token ve admin ID'leri ortam değişkenlerinde saklanır / Bot token and admin IDs are stored in environment variables
- Thread-safe veritabanı işlemleri / Thread-safe database operations
- Stok kontrolü ile aynı kartın birden fazla satılması engellenir / Stock control prevents duplicate sales
- Tüm kritik işlemler için hata yakalama ve loglama / Error catching and logging for all critical operations

### Güvenlik Önerileri / Security Recommendations

1. **Üretim Ortamı İçin / For Production:**
   - Gift card kodlarını veritabanında şifreli saklayın / Encrypt gift card codes in database
   - Gerçek ödeme entegrasyonu kullanın (Stripe, PayPal, vb.) / Use real payment integration (Stripe, PayPal, etc.)
   - SSL/TLS sertifikası ile HTTPS kullanın / Use HTTPS with SSL/TLS certificate
   - Düzenli yedekleme yapın / Perform regular backups
   - Rate limiting ekleyin / Add rate limiting

2. **Kullanıcı Verisi / User Data:**
   - GDPR ve gizlilik yasalarına uyum sağlayın / Comply with GDPR and privacy laws
   - Kullanıcı verilerini koruyun / Protect user data
   - Veri saklama politikası belirleyin / Define data retention policy

## 🤝 Katkıda Bulunma / Contributing

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

Contributions are welcome! Feel free to submit a pull request.

## 📝 Lisans / License

Bu proje açık kaynaklıdır ve MIT lisansı altında lisanslanmıştır.

This project is open source and licensed under the MIT License.

## ⚠️ Uyarı / Warning

Bu bot eğitim amaçlıdır. Gerçek para transferi için ödeme entegrasyonu eklemeniz önerilir.

This bot is for educational purposes. It is recommended to add payment integration for real money transfers.

## 📞 Destek / Support

Herhangi bir sorunuz veya sorununuz varsa, lütfen bir issue açın.

If you have any questions or issues, please open an issue.

## 🎯 Yeni Özellikler / New Features (v2.0)

- ✅ ~~Ödeme entegrasyonu (Stripe, PayPal, vs.)~~ - PayPal and Crypto support added
- ✅ ~~Otomatik stok yönetimi~~ - Stock management implemented
- ✅ ~~Toplu kart ekleme~~ - Bulk card addition via CSV/JSON
- ✅ ~~Kullanıcı sipariş geçmişi~~ - Order history tracking
- ✅ ~~Kupon ve indirim kodları~~ - Coupon system implemented
- ✅ ~~Çoklu dil desteği~~ - Turkish and English support
- [ ] Web dashboard for admins
- [ ] Email notifications
- [ ] Advanced analytics

---

Made with ❤️ for Telegram bot enthusiasts
