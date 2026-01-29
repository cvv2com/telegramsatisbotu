# 🚀 Hızlı Başlangıç Rehberi - MC/Visa Gift Card Bot

Bu rehber, MC/Visa Gift Card Bot'u hızlıca kurup çalıştırmanız için adım adım talimatlar içermektedir.

## ⚡ 5 Dakikada Kurulum

### 1. Gerekli Yazılımları İndirin

```bash
# Python 3.8+ kurulu olduğundan emin olun
python --version

# Git ile projeyi klonlayın
git clone https://github.com/cvv2com/telegramsatisbotu.git
cd telegramsatisbotu
```

### 2. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Telegram Bot Oluşturun

1. Telegram'da [@BotFather](https://t.me/BotFather)'ı açın
2. `/newbot` komutunu gönderin
3. Bot için bir isim seçin (örn: "MC Visa Cards Bot")
4. Bot için bir kullanıcı adı seçin (örn: "mc_visa_cards_bot")
5. BotFather size bir token verecek (örn: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 4. Admin ID'nizi Öğrenin

1. Telegram'da [@userinfobot](https://t.me/userinfobot)'u açın
2. Bota mesaj gönderin
3. Size gönderdiği user ID'yi not edin (örn: `123456789`)

### 5. Konfigürasyonu Düzenleyin

`config.py` dosyasını açın ve aşağıdaki bilgileri güncelleyin:

```python
# Telegram Bot Token
BOT_TOKEN = "BURAYA_TOKEN_YAPIŞTIRIN"

# Admin User IDs
ADMIN_IDS = [123456789]  # Kendi user ID'nizi buraya yazın
```

### 6. Botu Başlatın

```bash
python telegram_bot.py
```

Tebrikler! 🎉 Botunuz artık çalışıyor.

## 📱 İlk Kullanım

### Kullanıcı Olarak Test

1. Telegram'da botunuzu bulun (kullanıcı adıyla arama yapın)
2. `/start` komutunu gönderin
3. Ana menüden "💰 Bakiye" seçin
4. "➕ Bakiye Yükle" butonuna tıklayın
5. `100` yazın (test için $100 bakiye)
6. Şimdi "🎁 Kart Satın Al" yapabilirsiniz

### Admin Olarak Kart Ekleme

Terminal/komut satırında:

```bash
# 10 adet MC numerik kart ekle
python admin.py addmcnumeric 10

# 10 adet Visa numerik kart ekle
python admin.py addvisanumeric 10

# İstatistikleri görüntüle
python admin.py stats
```

## 🎯 Temel Senaryolar

### Senaryo 1: Numerik Kart Satışı

1. **Kullanıcı:** Bottan $20 minimum bakiye yükler
2. **Kullanıcı:** "🎁 Kart Satın Al" seçer
3. **Kullanıcı:** "💳 MC Numerik" veya "💳 Visa Numerik" seçer
4. **Kullanıcı:** Adet girer (örn: `2`)
5. **Bot:** Toplam $40 olduğunu gösterir
6. **Kullanıcı:** Onaylar
7. **Bot:** 2 kartın bilgilerini gönderir (numara, SKT, PIN)

### Senaryo 2: Resimli Kart Satışı

1. **Admin:** Resimli kart ekler:
   ```bash
   python admin.py addmcpicture 1
   ```
2. **Admin:** Görselleri yükler:
   - `giftcards/mc1front.jpg`
   - `giftcards/mc1back.jpg`
3. **Kullanıcı:** $50 bakiye yükler
4. **Kullanıcı:** "🖼️ MC Resimli" seçer
5. **Kullanıcı:** `1` adet girer
6. **Bot:** Kart bilgileri ve görselleri gönderir

## 🔧 Yaygın Sorunlar ve Çözümler

### Sorun 1: Bot başlamıyor

**Çözüm:**
```bash
# Token'ın doğru olduğundan emin olun
# config.py dosyasını kontrol edin
python -c "from config import BOT_TOKEN; print(BOT_TOKEN)"
```

### Sorun 2: Admin komutları çalışmıyor

**Çözüm:**
- `config.py`'de ADMIN_IDS listesinde olduğunuzdan emin olun
- User ID'nizin doğru olduğunu kontrol edin

### Sorun 3: Stokta kart yok

**Çözüm:**
```bash
# Kart ekleyin
python admin.py addmcnumeric 10
python admin.py addvisanumeric 10
```

### Sorun 4: Bakiye eklenemiyor (test için)

**Çözüm:**
```bash
# Admin olarak CLI'dan bakiye ekleyin
python admin.py addbalance KULLANICI_ID 100
```

## 📊 İlk Günler İçin Öneriler

### 1. Test Kartları Oluşturun

```bash
# Her türden 5'er adet test kartı ekleyin
python admin.py addmcnumeric 5
python admin.py addvisanumeric 5
```

### 2. Kendinize Test Bakiyesi Ekleyin

```bash
# Kendi user ID'nize $200 test bakiyesi
python admin.py addbalance KULLANICI_ID 200
```

### 3. Tüm Kart Türlerini Test Edin

- MC Numerik satın alın
- Visa Numerik satın alın
- Farklı adetler deneyin (1, 2, 5)
- Yetersiz bakiye durumunu test edin

### 4. Admin Panelini İnceleyin

Telegram botunda:
- "⚙️ Admin Paneli" butonuna tıklayın
- İstatistikleri görün
- Komutları not edin

## 🎓 İleri Seviye

### Otomatik Başlatma (Linux/Mac)

`/etc/systemd/system/giftcardbot.service`:

```ini
[Unit]
Description=MC/Visa Gift Card Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/telegramsatisbotu
ExecStart=/usr/bin/python3 telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Aktif et:
```bash
sudo systemctl enable giftcardbot
sudo systemctl start giftcardbot
```

### Ödeme Gateway Entegrasyonu

Gerçek para işlemleri için `telegram_bot.py`'de `add_balance_amount` fonksiyonunu güncelleyin:
- Stripe API
- PayPal API
- Kripto para ödeme gateway'i

### Görsel Yönetimi

Resimli kartlar için:

1. Görselleri hazırlayın (JPG, 800x500 px önerilir)
2. `giftcards/` klasörüne koyun
3. İsimlendirme: `mc1front.jpg`, `mc1back.jpg`
4. Kartı ekleyin: `python admin.py addmcpicture 1`

## 📞 Yardım

Daha fazla bilgi için:
- [Ana README](README.md)
- [Geliştirici Detayları](IMPLEMENTATION_DETAILS.md)
- [GitHub Issues](https://github.com/cvv2com/telegramsatisbotu/issues)

---

**Hayırlı işler! 🚀**
