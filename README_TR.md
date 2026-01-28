# Telegram Gift Card Satış Botu

Telegram üzerinden otomatik gift card satışı yapan bir bot. Kripto para ile ödeme alıp, kullanıcılara gift card satar.

**🐧 Ubuntu/cPanel-WHM Kullanıcıları:** Ubuntu ve cPanel/WHM kurulu sunucular için özel kurulum talimatları için [UBUNTU_CPANEL_INSTALL.md](UBUNTU_CPANEL_INSTALL.md) dosyasına bakın.

**🪟 Windows Kullanıcıları:** Windows için özel kurulum talimatları için [WINDOWS.md](WINDOWS.md) dosyasına bakın.

## Özellikler

### Kullanıcı Özellikleri
- 🎉 `/start` komutu ile karşılama ve ana menü
- 💰 Bakiye kontrolü (yeni kullanıcılar 0 bakiye ile başlar)
- 💎 Kripto para ile bakiye yükleme (BTC, ETH, USDT, LTC)
- 🎁 Gift card satın alma (Mastercard, Visa, Amazon, Steam, Google Play)
- 🎟️ Kupon kodu kullanarak indirim kazanma
- 📊 İşlem geçmişi
- 🔒 SQLite veritabanı ile güvenli veri saklama
- 🤖 Otomatik gift card görseli gönderimi

### Yönetici Özellikleri
- 📤 **Toplu Ürün İçe Aktarma** - CSV veya JSON dosyası ile yüzlerce ürünü tek seferde ekleyin
- 🎟️ **Kupon Yönetimi** - `/addcoupon` komutu ile indirim kuponu oluşturun
- 👥 Kullanıcı yönetimi (admin.py ile)
- 💰 Manuel bakiye yükleme
- 📈 Satış istatistikleri

### Platform Desteği
- 🪟 Windows desteği (batch dosyaları ile)
- 🐧 Ubuntu/cPanel-WHM desteği
- 🐧 Genel Linux/Mac desteği

## Kurulum

### Platform Seçimi

Kurulum için işletim sisteminize göre uygun rehberi seçin:

- **🐧 Ubuntu + cPanel/WHM Sunucu**: [UBUNTU_CPANEL_INSTALL.md](UBUNTU_CPANEL_INSTALL.md) - Detaylı Ubuntu ve cPanel/WHM kurulum rehberi
- **🪟 Windows**: [WINDOWS.md](WINDOWS.md) - Windows özel kurulum rehberi
- **🐧 Genel Linux/Mac**: Aşağıdaki genel talimatları takip edin
- **🚀 Gelişmiş Kurulum**: [DEPLOYMENT.md](DEPLOYMENT.md) - Docker, systemd ve diğer seçenekler

### 1. Gereksinimler

Python 3.8 veya üzeri gereklidir.

### 2. Kurulum

**Windows Kullanıcıları için:**
```cmd
# Kurulum scriptini çalıştırın
setup.bat
```
Ardından `config.py` dosyasını bot token'ınız ile düzenleyin ve `start.bat` ile başlatın. Detaylar için [WINDOWS.md](WINDOWS.md) dosyasına bakın.

**Linux/Mac Kullanıcıları için:**
```bash
# Setup scriptini çalıştırın
chmod +x setup.sh
./setup.sh

# Veya manuel:
pip install -r requirements.txt
cp config.example.py config.py
```

### 3. Bot Token'ı Alın

1. Telegram'da [@BotFather](https://t.me/BotFather) ile konuşun
2. `/newbot` komutu ile yeni bir bot oluşturun
3. Bot token'ınızı alın

### 4. Konfigürasyon

`config.py` dosyasını düzenleyin:

```python
# Bot token'ınızı ekleyin
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Kripto cüzdan adreslerinizi ekleyin
CRYPTO_WALLETS = {
    "btc": "your_btc_wallet_address",
    "eth": "your_eth_wallet_address",
    "usdt": "your_usdt_wallet_address",
    "ltc": "your_ltc_wallet_address",
}
```

### 5. Gift Card Görsellerini Ekleyin

`gift_cards` klasörü oluşturun ve gift card görsellerini ekleyin:

```bash
mkdir gift_cards
```

Gift card görselleri:
- `gift_cards/mastercard_50.jpg`
- `gift_cards/mastercard_100.jpg`
- `gift_cards/visa_30.jpg`
- `gift_cards/visa_50.jpg`
- `gift_cards/amazon_25.jpg`
- `gift_cards/amazon_50.jpg`
- `gift_cards/steam_20.jpg`
- `gift_cards/google_play_25.jpg`

### 6. Botu Çalıştırın

```bash
python bot.py
```

## Kullanım

### Kullanıcı Adımları

1. **Başlangıç**: `/start` komutu ile botu başlatın
2. **Bakiye Kontrolü**: "Balance" butonuna tıklayarak bakiyenizi görün
3. **Bakiye Yükleme**: 
   - "How to Buy" butonuna tıklayın
   - Bir kripto para seçin (BTC, ETH, USDT, LTC)
   - Gösterilen cüzdan adresine ödeme yapın
   - Ödeme onaylandıktan sonra bakiyeniz otomatik yüklenir
4. **Gift Card Satın Alma**:
   - "Buy Gift Card" butonuna tıklayın
   - İstediğiniz gift card'ı seçin
   - Bakiyenizden otomatik olarak düşülür
   - Gift card görseli size otomatik gönderilir

### Admin İşlemleri

#### Yönetici Kimliği Ekleme

`config.py` dosyasında admin kullanıcı ID'lerini belirtin:

```python
# Admin User IDs (Telegram user ID'leri)
# Kendi ID'nizi öğrenmek için @userinfobot ile konuşun
ADMIN_IDS = [123456789, 987654321]
```

#### Toplu Ürün İçe Aktarma

Yüzlerce ürünü tek seferde eklemek için CSV veya JSON dosyası kullanın.

**1. `/import` komutu ile başlatın:**
```
/import
```

**2. CSV veya JSON dosyası gönderin:**

**CSV Format:**
```csv
name,description,price,category,code,stock
Netflix 10$,1 Month,10,Entertainment,NF-123,5
Steam 20$,Steam Wallet,20,Gaming,ST-456,10
Amazon 50$,Gift Card,50,Shopping,AMZ-789,3
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
  },
  {
    "name": "Steam 20$",
    "description": "Steam Wallet",
    "price": 20,
    "category": "Gaming",
    "code": "ST-456",
    "stock": 10
  }
]
```

#### Kupon Oluşturma

İndirim kuponu oluşturmak için `/addcoupon` komutunu kullanın.

**Komut Formatı:**
```
/addcoupon <code> <type> <value> [min_purchase] [max_uses] [expiry_days]
```

**Parametreler:**
- `code`: Kupon kodu (örn: SUMMER2024)
- `type`: İndirim tipi (`percent` veya `fixed`)
- `value`: İndirim değeri (yüzde veya sabit tutar)
- `min_purchase`: Minimum alış tutarı (opsiyonel, varsayılan: 0)
- `max_uses`: Maksimum kullanım sayısı (opsiyonel, varsayılan: sınırsız)
- `expiry_days`: Geçerlilik süresi gün olarak (opsiyonel, varsayılan: 30)

**Örnekler:**

```bash
# %20 indirim kuponu, min 10$, max 100 kullanım, 30 gün geçerli
/addcoupon WELCOME20 percent 20 10 100 30

# 10$ sabit indirim, min 50$, sınırsız kullanım, 60 gün geçerli
/addcoupon SAVE10 fixed 10 50 -1 60

# %15 indirim, minimum alış yok, 50 kez kullanılabilir
/addcoupon SPECIAL15 percent 15 0 50
```

#### Manuel Bakiye Yükleme

`admin.py` scriptini kullanın:

```bash
# Kullanıcıya $100 ekle
python admin.py add 123456789 100.00
```

Veya doğrudan SQL kullanarak:

```python
import sqlite3

conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

# Kullanıcıya $100 ekle
user_id = 123456789  # Kullanıcı ID'si
amount = 100.0

cursor.execute(
    'UPDATE users SET balance = balance + ? WHERE user_id = ?',
    (amount, user_id)
)

cursor.execute(
    'INSERT INTO transactions (user_id, transaction_type, amount, description) VALUES (?, ?, ?, ?)',
    (user_id, 'deposit', amount, 'Manuel bakiye yükleme')
)

conn.commit()
conn.close()
```

## Veritabanı Yapısı

### Users Tablosu
- `user_id`: Telegram kullanıcı ID (PRIMARY KEY)
- `username`: Kullanıcı adı
- `balance`: Mevcut bakiye (USD)
- `created_at`: Kayıt tarihi

### Transactions Tablosu
- `id`: İşlem ID (AUTO INCREMENT)
- `user_id`: Kullanıcı ID
- `transaction_type`: İşlem tipi (deposit/purchase)
- `amount`: İşlem tutarı
- `description`: İşlem açıklaması
- `created_at`: İşlem tarihi

### Gift Card Purchases Tablosu
- `id`: Satın alma ID
- `user_id`: Kullanıcı ID
- `card_id`: Kart ID
- `card_name`: Kart adı
- `card_number`: Kart numarası
- `exp_date`: Son kullanma tarihi
- `pin`: PIN kodu
- `amount`: Tutar
- `purchased_at`: Satın alma tarihi

### Products Tablosu (Yeni)
- `id`: Ürün ID
- `name`: Ürün adı
- `description`: Açıklama
- `price`: Fiyat
- `category`: Kategori
- `code`: Ürün kodu (UNIQUE)
- `stock`: Stok miktarı
- `created_at`: Oluşturma tarihi
- `updated_at`: Güncelleme tarihi

### Coupons Tablosu (Yeni)
- `id`: Kupon ID
- `code`: Kupon kodu (UNIQUE)
- `discount_type`: İndirim tipi (percent/fixed)
- `discount_value`: İndirim değeri
- `min_purchase`: Minimum alış tutarı
- `max_uses`: Maksimum kullanım sayısı
- `used_count`: Kullanım sayısı
- `expiry_date`: Son kullanma tarihi
- `active`: Aktif durumu
- `created_at`: Oluşturma tarihi

### Coupon Usage Tablosu (Yeni)
- `id`: Kullanım ID
- `coupon_id`: Kupon ID
- `user_id`: Kullanıcı ID
- `discount_amount`: İndirim tutarı
- `used_at`: Kullanım tarihi


## Güvenlik Notları

- ⚠️ `config.py` dosyasını asla GitHub'a yüklemeyin
- ⚠️ Bot token'ınızı kimseyle paylaşmayın
- ⚠️ Cüzdan adreslerinizi düzenli kontrol edin
- ⚠️ Veritabanı yedeklerini düzenli alın
- ⚠️ Ödemelerin onaylanması için manuel kontrol sistemi ekleyin

## Özelleştirme

### Yeni Gift Card Ekleme

`config.py` dosyasındaki `GIFT_CARDS` sözlüğüne yeni gift card ekleyin:

```python
"new_card": {
    "name": "Yeni Gift Card $75",
    "amount": 75.0,
    "image_path": "gift_cards/new_card_75.jpg",
    "description": "Yeni $75 Gift Card"
}
```

### Yeni Kripto Para Ekleme

`config.py` dosyasındaki `CRYPTO_WALLETS` sözlüğüne yeni kripto para ekleyin:

```python
"doge": "your_dogecoin_wallet_address"
```

## Sorun Giderme

### Bot çalışmıyor
- Bot token'ınızın doğru olduğundan emin olun
- İnternet bağlantınızı kontrol edin
- Python sürümünüzü kontrol edin (3.8+)

### Gift card görseli gönderilmiyor
- `gift_cards` klasörünün olduğundan emin olun
- Görsel dosya adlarının `config.py` ile eşleştiğinden emin olun
- Görsel dosyalarının okuma izinlerini kontrol edin

## Lisans

Bu proje açık kaynak kodludur ve serbestçe kullanılabilir.

## Destek

Sorularınız için issue açabilirsiniz.
