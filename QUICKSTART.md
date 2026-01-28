# Quick Start Guide

Hızlıca botunuzu başlatmak için bu adımları takip edin.

## 5 Dakikada Başlangıç

### 1. Bot Token Alın (2 dakika)

1. Telegram'da [@BotFather](https://t.me/BotFather)'a gidin
2. `/newbot` yazın
3. Bot adını ve kullanıcı adını belirleyin
4. Token'ı kopyalayın

### 2. Kurulum (2 dakika)

```bash
# Repository'yi klonlayın
git clone https://github.com/cvv2com/telegramsatisbotu.git
cd telegramsatisbotu

# Otomatik kurulum
chmod +x setup.sh
./setup.sh

# Konfigürasyon dosyası oluşturun
cp config.example.py config.py
nano config.py  # Token'ınızı ve cüzdan adreslerinizi ekleyin
```

### 3. Bot'u Başlatın (1 dakika)

```bash
# Konfigürasyonu doğrulayın
python3 verify.py

# Bot'u başlatın
python3 bot.py
```

## İlk Test

1. Telegram'da botunuzu bulun
2. `/start` gönderin
3. Menüyü görmelisiniz!

## Sonraki Adımlar

- 📖 Detaylı bilgi için: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🇹🇷 Türkçe dokümantasyon: [README_TR.md](README_TR.md)
- 🇬🇧 English documentation: [README.md](README.md)

## Önemli Notlar

⚠️ **Ödeme Kontrolü**: Kullanıcılar kripto para gönderdikten sonra:
```bash
python3 admin.py add <user_id> <miktar>
```

⚠️ **Gift Card Görselleri**: `gift_cards/` klasörüne görsel ekleyin

⚠️ **Güvenlik**: `config.py` dosyasını güvende tutun!

## Sorun mu var?

1. `python3 verify.py` çalıştırın - konfigürasyonu kontrol eder
2. [DEPLOYMENT.md](DEPLOYMENT.md) dosyasındaki Troubleshooting bölümüne bakın
3. GitHub'da issue açın

## Admin Komutları

```bash
# Tüm kullanıcıları listele
python3 admin.py users

# Kullanıcı bilgilerini gör
python3 admin.py user 123456789

# Bakiye ekle
python3 admin.py add 123456789 100.00

# İstatistikleri gör
python3 admin.py stats
```

İyi satışlar! 🎉
