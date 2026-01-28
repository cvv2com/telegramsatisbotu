# Telegram Gift Card Satış Botu

Telegram üzerinden otomatik gift card satışı yapan bir bot. Kripto para ile ödeme alıp, kullanıcılara gift card satar.

**🪟 Windows Kullanıcıları:** Windows için özel kurulum talimatları için [WINDOWS.md](WINDOWS.md) dosyasına bakın.

## Özellikler

- 🎉 `/start` komutu ile karşılama ve ana menü
- 💰 Bakiye kontrolü (yeni kullanıcılar 0 bakiye ile başlar)
- 💎 Kripto para ile bakiye yükleme (BTC, ETH, USDT, LTC)
- 🎁 Gift card satın alma (Mastercard, Visa, Amazon, Steam, Google Play)
- 📊 İşlem geçmişi
- 🔒 SQLite veritabanı ile güvenli veri saklama
- 🤖 Otomatik gift card görseli gönderimi
- 🪟 Windows desteği (batch dosyaları ile)

## Kurulum

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

#### Manuel Bakiye Yükleme

Bir kullanıcıya manuel olarak bakiye yüklemek için SQLite veritabanını kullanabilirsiniz:

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
