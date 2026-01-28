# 🚀 Hızlı Başlangıç Rehberi

Bu rehber, Telegram Gift Card Satış Botunu 5 dakikada çalıştırmanıza yardımcı olacaktır.

## 1️⃣ Telegram Bot Token Alın

1. Telegram'da [@BotFather](https://t.me/BotFather) botunu açın
2. `/newbot` komutunu gönderin
3. Bot için bir isim belirleyin (örn: "Gift Card Satış")
4. Bot için bir kullanıcı adı belirleyin (örn: "giftcardsatis_bot")
5. BotFather size bir token verecek, bu tokeni kopyalayın

## 2️⃣ Telegram ID'nizi Öğrenin

1. [@userinfobot](https://t.me/userinfobot) botunu açın
2. Bota herhangi bir mesaj gönderin
3. Bot size Telegram ID'nizi verecek (örn: 123456789)

## 3️⃣ Botu Kurun

```bash
# Depoyu klonlayın
git clone https://github.com/cvv2com/telegramsatisbotu.git
cd telegramsatisbotu

# Sanal ortam oluşturun (opsiyonel ama önerilir)
python -m venv venv
source venv/bin/activate  # Linux/Mac için
# veya Windows için: venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Ortam değişkenlerini ayarlayın
cp .env.example .env
```

## 4️⃣ Ayarları Yapın

`.env` dosyasını düzenleyin:

```bash
TELEGRAM_BOT_TOKEN=sizin_bot_token_buraya
ADMIN_IDS=sizin_telegram_id_buraya
```

## 5️⃣ Botu Başlatın

```bash
python bot.py
```

Bot çalışmaya başladığında şu mesajı göreceksiniz:
```
INFO - Bot başlatılıyor...
```

## 6️⃣ Botu Test Edin

1. Telegram'da botunuzu arayın
2. `/start` komutunu gönderin
3. Admin paneline girin
4. Bir test gift card ekleyin:

```
/addcard Test Card | Test açıklama | 10 | Test | TEST-1234
```

## 🎉 Tebrikler!

Botunuz artık çalışıyor! Artık:
- ✅ Gift card ekleyebilirsiniz
- ✅ Kartları listeleyebilirsiniz
- ✅ Satış yapabilirsiniz
- ✅ İstatistikleri görüntüleyebilirsiniz

## ⚙️ İleri Düzey Ayarlar

### Birden Fazla Admin Eklemek

`.env` dosyasında ID'leri virgülle ayırın:
```
ADMIN_IDS=123456789,987654321,555666777
```

### Para Birimini Değiştirme

`config.py` dosyasında:
```python
CURRENCY = '$'  # veya '€' veya istediğiniz simge
```

### Veritabanı Konumunu Değiştirme

`config.py` dosyasında:
```python
DATABASE_FILE = '/path/to/your/database.json'
```

## 🆘 Sorun Giderme

### "Error: Invalid token"
- Bot tokeninizi kontrol edin
- `.env` dosyasında doğru girildiğinden emin olun

### "Admin paneline erişemiyorum"
- Telegram ID'nizi doğru girdiğinizden emin olun
- `.env` dosyasını düzenledikten sonra botu yeniden başlatın

### Bot mesajlara yanıt vermiyor
- Botun çalıştığından emin olun
- İnternet bağlantınızı kontrol edin
- Bot tokeninin doğru olduğunu kontrol edin

## 📚 Daha Fazla Bilgi

Detaylı bilgi için [README.md](README.md) dosyasına bakın.

---

## 🆕 Yeni Özellikler (v2.0)

### Çoklu Dil Desteği / Multi-language Support
Botunuz artık Türkçe ve İngilizce dillerini destekliyor:
```
/language - Dil değiştir
```

### Stok Yönetimi / Stock Management
Kartlarınızı stok miktarı ile ekleyin:
```
/addcard Netflix | 1 Ay Premium | 50 | Eğlence | NFLX-001 | 10
                                                           ↑↑
                                                        Stok miktarı
```

### Toplu Kart Ekleme / Bulk Card Addition
CSV veya JSON dosyası ile birden fazla kart ekleyin:
```
/bulkaddcard
(sonra CSV/JSON dosyası gönderin)
```

### Kupon Sistemi / Coupon System
İndirim kuponları oluşturun:
```
/addcoupon HOSGELDIN | percentage | 10 | 100 | 30
(Kod: HOSGELDIN, %10 indirim, max 100 kullanım, 30 gün geçerli)
```

### Sipariş Geçmişi / Order History
Kullanıcılar siparişlerini görebilir:
```
/myorders
```

### Ödeme Entegrasyonu / Payment Integration
PayPal ve Kripto para desteği için `.env` dosyasını yapılandırın:
```
PAYPAL_EMAIL=your_paypal@example.com
BTC_WALLET=your_bitcoin_wallet
ETH_WALLET=your_ethereum_wallet
LTC_WALLET=your_litecoin_wallet
```

## 🎯 Hızlı Test Senaryosu / Quick Test Scenario

1. Botu başlatın: `/start`
2. Dil seçin (Türkçe/English)
3. Test kartı ekleyin: `/addcard Test | Deneme | 5 | Test | CODE123 | 3`
4. Kupon oluşturun: `/addcoupon TEST10 | percentage | 10 | 10 | 7`
5. Admin paneline bakın
6. Kullanıcı olarak test edin (farklı hesaptan)
7. Sipariş geçmişi kontrol edin: `/myorders`

✅ Tüm özellikler çalışıyorsa hazırsınız!

