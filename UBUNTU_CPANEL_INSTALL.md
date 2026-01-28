# Ubuntu + cPanel/WHM Server Kurulum Rehberi

Telegram Gift Card Satış Botu için Ubuntu işletim sistemi ve cPanel/WHM yüklü sunucularda kurulum rehberi.

## 📋 Ön Gereksinimler

### Sistem Gereksinimleri
- **İşletim Sistemi**: Ubuntu 20.04 LTS veya 22.04 LTS
- **cPanel/WHM**: Kurulu ve çalışır durumda
- **Python**: 3.8 veya üzeri (genellikle sistem Python'u kullanılır)
- **RAM**: Minimum 512 MB (1 GB önerilir)
- **Disk**: En az 1 GB boş alan
- **Root veya Sudo Erişimi**: Gerekli

### cPanel/WHM Ortamında Özel Hususlar
- cPanel ortamında Python yolları standart olmayabilir
- Sanal ortam (virtual environment) kullanımı şiddetle önerilir
- Dosya izinleri ve sahiplik önemlidir
- Service yönetimi için systemd kullanılır

## 🔧 Adım 1: Sistem Hazırlığı

### 1.1 Sistem Güncellemesi

SSH ile sunucuya bağlanın ve sistem paketlerini güncelleyin:

```bash
# Root kullanıcısı ile
sudo apt update && sudo apt upgrade -y
```

### 1.2 Gerekli Paketleri Yükleyin

```bash
# Temel geliştirme araçları ve Python gereksinimleri
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y git wget curl
sudo apt install -y build-essential libssl-dev libffi-dev
```

### 1.3 Python Versiyonunu Kontrol Edin

```bash
python3 --version
# Çıktı: Python 3.8.x veya üzeri olmalı
```

## 👤 Adım 2: Kullanıcı Hesabı Oluşturma

cPanel ortamında, bot'u ayrı bir kullanıcı altında çalıştırmak en iyi pratiktir.

### 2.1 WHM'den Yeni Hesap Oluşturma (Önerilen)

1. WHM'e giriş yapın (https://sunucunuz.com:2087)
2. **Account Functions** → **Create a New Account**
3. Hesap bilgilerini doldurun:
   - Domain: `telegram-bot.yourdomain.com` (veya subdomain)
   - Username: `tgbot` (örnek)
   - Password: Güçlü bir şifre
4. Hesabı oluşturun

### 2.2 Manuel Kullanıcı Oluşturma (Alternatif)

```bash
# Yeni kullanıcı oluştur
sudo useradd -m -s /bin/bash tgbot

# Şifre belirle
sudo passwd tgbot

# Kullanıcıya sudo yetkisi ver (gerekirse)
sudo usermod -aG sudo tgbot
```

## 📦 Adım 3: Bot Kurulumu

### 3.1 Kullanıcı Hesabına Geçiş

```bash
# tgbot kullanıcısına geç
sudo su - tgbot
```

### 3.2 Çalışma Dizini Oluşturma

cPanel ortamında home dizini genellikle şöyledir:
- WHM hesabı: `/home/tgbot/`
- Manuel kullanıcı: `/home/tgbot/`

```bash
# Ana dizinde çalışma alanı oluştur
cd ~
mkdir -p telegram-bot
cd telegram-bot
```

### 3.3 Repository'yi Klonlama

```bash
git clone https://github.com/cvv2com/telegramsatisbotu.git
cd telegramsatisbotu
```

### 3.4 Virtual Environment Oluşturma

**ÖNEMLİ**: cPanel ortamında mutlaka virtual environment kullanın!

**⚠️ DİKKAT: Root olarak pip install yapmayın!**
Virtual environment kullanmadan sistem genelinde paket yüklemek:
- Sistem paket yöneticisiyle çakışmalara neden olur
- İzin sorunlarına yol açabilir
- Farklı projelerin bağımlılıklarını karıştırır
- Güvenlik riski oluşturur

```bash
# Virtual environment oluştur
python3 -m venv venv

# Virtual environment'ı aktif et
source venv/bin/activate

# Pip'i güncelle
pip install --upgrade pip
```

### 3.5 Bağımlılıkları Yükleme

```bash
# Virtual environment aktif iken
pip install -r requirements.txt
```

Başarılı kurulum sonrası şunu görmelisiniz:
```
Successfully installed python-telegram-bot-21.9 ...
```

## ⚙️ Adım 4: Bot Konfigürasyonu

### 4.1 Telegram Bot Token Alma

1. Telegram'da [@BotFather](https://t.me/BotFather) ile konuşun
2. `/newbot` komutunu gönderin
3. Bot adını ve kullanıcı adını belirleyin
4. Token'ı kopyalayın (örnek: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 4.2 Konfigürasyon Dosyası Oluşturma

```bash
# config.example.py'yi kopyala
cp config.example.py config.py

# Nano veya vim ile düzenle
nano config.py
```

### 4.3 Konfigürasyon Ayarları

`config.py` dosyasını düzenleyin:

```python
# Telegram Bot Token
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # Kendi token'ınız

# Kripto Para Cüzdan Adresleri
CRYPTO_WALLETS = {
    "btc": "sizin_btc_adresiniz",
    "eth": "sizin_eth_adresiniz",
    "usdt": "sizin_usdt_adresiniz",
    "ltc": "sizin_ltc_adresiniz",
}

# Gift Card Yapılandırması (örnek)
GIFT_CARDS = {
    "mc_50": {
        "name": "Mastercard Gift Card $50",
        "amount": 50.0,
        "card_number": "5543554475829811",
        "exp_date": "02/27",
        "pin": "097",
        "image_front": "gift_cards/mastercard_50_front.jpg",
        "image_back": "gift_cards/mastercard_50_back.jpg",
        "description": "Mastercard $50 Gift Card"
    },
    # Diğer kartları ekleyin...
}
```

Kaydedin ve çıkın (Nano'da: Ctrl+X, Y, Enter)

### 4.4 Gift Card Görsellerini Ekleme

```bash
# gift_cards klasörü zaten var, görselleri ekleyin
# FTP, SFTP veya WHM File Manager kullanabilirsiniz

# Örnek: wget ile indirme
cd gift_cards/
# Görsellerinizi buraya ekleyin
cd ..
```

### 4.5 Dosya İzinlerini Ayarlama

```bash
# Güvenlik için doğru izinler
chmod 600 config.py  # Sadece sahip okuyabilir
chmod 755 bot.py admin.py verify.py
chmod 755 gift_cards/
```

## 🔍 Adım 5: Konfigürasyonu Test Etme

```bash
# Virtual environment aktif olmalı
python3 verify.py
```

Çıktıda şunları görmelisiniz:
- ✅ config.py found
- ✅ Bot token is set
- ✅ Crypto wallets configured
- ✅ Gift cards configured

## 🚀 Adım 6: Bot'u İlk Defa Çalıştırma

### Manuel Test

```bash
# Virtual environment aktif iken
python3 bot.py
```

Başarılı başlatma:
```
Bot başlatılıyor...
```

**Test Etme:**
1. Telegram'da botunuzu bulun
2. `/start` gönderin
3. Menüyü görmelisiniz

Test başarılıysa, Ctrl+C ile durdurun.

## 🔄 Adım 7: Systemd Service Kurulumu

Bot'un arka planda sürekli çalışması için systemd service oluşturun.

### 7.1 Service Dosyası Oluşturma

```bash
# Root kullanıcısına geç
exit  # tgbot kullanıcısından çık

# Service dosyası oluştur
sudo nano /etc/systemd/system/telegram-gift-bot.service
```

### 7.2 Service İçeriği

```ini
[Unit]
Description=Telegram Gift Card Sales Bot
After=network.target

[Service]
Type=simple
User=tgbot
Group=tgbot
WorkingDirectory=/home/tgbot/telegram-bot/telegramsatisbotu
Environment="PATH=/home/tgbot/telegram-bot/telegramsatisbotu/venv/bin"
ExecStart=/home/tgbot/telegram-bot/telegramsatisbotu/venv/bin/python3 /home/tgbot/telegram-bot/telegramsatisbotu/bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**DİKKAT**: Yolları kendi kurulumunuza göre düzenleyin!

### 7.3 Service'i Aktif Etme

```bash
# Systemd'yi yeniden yükle
sudo systemctl daemon-reload

# Service'i başlangıçta çalışacak şekilde ayarla
sudo systemctl enable telegram-gift-bot

# Service'i başlat
sudo systemctl start telegram-gift-bot

# Durumunu kontrol et
sudo systemctl status telegram-gift-bot
```

Başarılı çıktı:
```
● telegram-gift-bot.service - Telegram Gift Card Sales Bot
   Loaded: loaded (/etc/systemd/system/telegram-gift-bot.service; enabled)
   Active: active (running) since ...
```

### 7.4 Service Yönetimi

```bash
# Durumu kontrol et
sudo systemctl status telegram-gift-bot

# Durdur
sudo systemctl stop telegram-gift-bot

# Başlat
sudo systemctl start telegram-gift-bot

# Yeniden başlat
sudo systemctl restart telegram-gift-bot

# Logları görüntüle
sudo journalctl -u telegram-gift-bot -f

# Son 100 satırı göster
sudo journalctl -u telegram-gift-bot -n 100
```

## 🔐 Adım 8: Güvenlik Ayarları

### 8.1 Firewall Ayarları (UFW)

```bash
# UFW durumunu kontrol et
sudo ufw status

# SSH'ı aktif et (bağlantı kopmasın!)
sudo ufw allow 22/tcp

# cPanel/WHM portlarını aç
sudo ufw allow 2083/tcp  # cPanel HTTPS
sudo ufw allow 2087/tcp  # WHM HTTPS

# Firewall'ı aktif et
sudo ufw enable
```

### 8.2 Dosya İzinleri

```bash
# Bot dizinindeki tüm dosyalar için
cd /home/tgbot/telegram-bot/telegramsatisbotu

# Sahipliği ayarla
sudo chown -R tgbot:tgbot .

# Dizin izinleri
find . -type d -exec chmod 755 {} \;

# Dosya izinleri
find . -type f -exec chmod 644 {} \;

# Çalıştırılabilir scriptler
chmod 755 bot.py admin.py verify.py setup.sh

# config.py'yi koru
chmod 600 config.py
```

### 8.3 Veritabanı Yedekleme

```bash
# Yedekleme dizini oluştur
mkdir -p ~/backups

# Otomatik yedekleme scripti
nano ~/backup-bot.sh
```

Script içeriği:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/tgbot/backups"
BOT_DIR="/home/tgbot/telegram-bot/telegramsatisbotu"

# Veritabanını yedekle
cp $BOT_DIR/bot_database.db $BACKUP_DIR/bot_database_$DATE.db

# Eski yedekleri temizle (30 günden eski)
find $BACKUP_DIR -name "bot_database_*.db" -mtime +30 -delete

echo "Backup completed: bot_database_$DATE.db"
```

Çalıştırılabilir yap:
```bash
chmod +x ~/backup-bot.sh
```

### 8.4 Cron ile Otomatik Yedekleme

```bash
# Crontab düzenle
crontab -e

# Günlük saat 03:00'de yedekleme
0 3 * * * /home/tgbot/backup-bot.sh >> /home/tgbot/backup.log 2>&1
```

## 🛠️ Adım 9: cPanel/WHM Entegrasyonu

### 9.1 WHM'den Monitoring

WHM'de service durumunu izlemek için:

1. WHM'e giriş yapın
2. **Service Configuration** → **Service Manager**
3. Telegram bot service'inizi listede görebilirsiniz

### 9.2 Resource Limitleri

cPanel ortamında resource limitleri önemlidir:

```bash
# Kullanıcı limitlerini kontrol et
sudo -u tgbot ulimit -a

# Process limiti artırmak için (gerekirse)
sudo nano /etc/security/limits.conf

# Ekle:
tgbot soft nofile 4096
tgbot hard nofile 8192
```

### 9.3 cPanel File Manager ile Erişim

Bot dosyalarına WHM/cPanel File Manager'dan erişebilirsiniz:

1. cPanel'e giriş yapın
2. **File Manager**'ı açın
3. `telegram-bot/telegramsatisbotu/` dizinine gidin
4. Dosyaları düzenleyebilir veya görüntüleyebilirsiniz

**NOT**: config.py gibi hassas dosyaları File Manager'dan düzenlerken dikkatli olun!

## 💼 Adım 10: Admin İşlemleri

### 10.1 Kullanıcı Yönetimi

```bash
# tgbot kullanıcısı olarak
cd ~/telegram-bot/telegramsatisbotu
source venv/bin/activate

# Tüm kullanıcıları listele
python3 admin.py users

# Kullanıcı detayları
python3 admin.py user 123456789

# Bakiye ekle
python3 admin.py add 123456789 100.00

# İstatistikler
python3 admin.py stats
```

### 10.2 Log İzleme

```bash
# Canlı log izleme
sudo journalctl -u telegram-gift-bot -f

# Son hataları göster
sudo journalctl -u telegram-gift-bot -p err -n 50

# Belirli tarih aralığı
sudo journalctl -u telegram-gift-bot --since "2024-01-01" --until "2024-01-31"
```

## 🔧 Sorun Giderme

### Yaygın Sorunlar ve Çözümleri

#### 1. Bot Başlamıyor

```bash
# Service durumunu kontrol et
sudo systemctl status telegram-gift-bot

# Detaylı log
sudo journalctl -u telegram-gift-bot -n 100 --no-pager

# Manuel test
cd /home/tgbot/telegram-bot/telegramsatisbotu
source venv/bin/activate
python3 bot.py
```

#### 2. "No module named 'telegram'" Hatası

```bash
# Virtual environment aktif mi kontrol et
which python3
# Çıktı: /home/tgbot/telegram-bot/telegramsatisbotu/venv/bin/python3 olmalı

# Değilse aktif et
source venv/bin/activate

# Bağımlılıkları tekrar yükle
pip install -r requirements.txt
```

#### 3. İzin Sorunları

```bash
# Sahipliği düzelt
sudo chown -R tgbot:tgbot /home/tgbot/telegram-bot/telegramsatisbotu

# İzinleri düzelt
chmod 755 /home/tgbot/telegram-bot/telegramsatisbotu
chmod 600 /home/tgbot/telegram-bot/telegramsatisbotu/config.py
```

#### 4. Veritabanı Hatası

```bash
# Veritabanı izinlerini kontrol et
ls -la bot_database.db

# Yeniden oluştur (DİKKAT: Veriler silinir!)
rm bot_database.db
python3 bot.py  # Yeni veritabanı oluşturulur
```

#### 5. Port Çakışması

cPanel ortamında bazı portlar kullanımda olabilir. Bot Telegram API kullandığı için port çakışması olmaz, ancak reverse proxy kullanıyorsanız:

```bash
# Port kullanımını kontrol et
sudo netstat -tlnp | grep python3

# Process'i durdur
sudo systemctl stop telegram-gift-bot
```

### cPanel Özel Sorunlar

#### Python Versiyonu Sorunları

```bash
# Sistemdeki tüm Python versiyonları
ls -la /usr/bin/python*

# Alternatif Python kullan
/usr/bin/python3.8 -m venv venv
```

#### CloudLinux LVE Limitleri

CloudLinux kullanıyorsanız:

```bash
# LVE limitlerini kontrol et
sudo lvectl list

# Limit artırma (WHM'den de yapılabilir)
sudo lvectl set tgbot --pmem=512M --vmem=1G
```

## 📊 İzleme ve Bakım

### Günlük Kontroller

```bash
# Service durumu
sudo systemctl status telegram-gift-bot

# Son loglar
sudo journalctl -u telegram-gift-bot -n 50

# Disk kullanımı
du -sh ~/telegram-bot/telegramsatisbotu/
df -h
```

### Haftalık Bakım

```bash
# Log rotasyonu (systemd otomatik yapar, kontrol için)
sudo journalctl --vacuum-time=7d

# Veritabanı yedekleme
~/backup-bot.sh

# Sistem güncellemeleri
sudo apt update && sudo apt upgrade
```

### Aylık Bakım

```bash
# Bot güncelleme
cd ~/telegram-bot/telegramsatisbotu
git pull origin main
source venv/bin/activate
pip install -U -r requirements.txt
sudo systemctl restart telegram-gift-bot

# Yedekleme kontrolü
ls -lh ~/backups/
```

## 📈 Performans Optimizasyonu

### 1. Python Optimizasyonu

```bash
# Optimize edilmiş bytecode
python3 -OO bot.py
```

Service dosyasında:
```ini
ExecStart=/home/tgbot/.../venv/bin/python3 -OO /home/tgbot/.../bot.py
```

### 2. SQLite Optimizasyonu

Veritabanı büyürse:

```bash
# Veritabanını optimize et
sqlite3 bot_database.db "VACUUM;"
```

### 3. Log Yönetimi

```ini
# Service dosyasında log seviyesi
Environment="LOG_LEVEL=WARNING"
```

## 🆘 Destek ve Kaynaklar

### Yararlı Komutlar Özeti

```bash
# Service yönetimi
sudo systemctl {start|stop|restart|status} telegram-gift-bot

# Log görüntüleme
sudo journalctl -u telegram-gift-bot -f

# Admin işlemleri
python3 admin.py {users|user|add|stats}

# Yedekleme
~/backup-bot.sh

# Virtual environment
source venv/bin/activate
deactivate
```

### Dokümantasyon

- Ana README: [README_TR.md](README_TR.md)
- Windows Kurulumu: [WINDOWS.md](WINDOWS.md)
- Genel Deployment: [DEPLOYMENT.md](DEPLOYMENT.md)
- Gift Card Özellikleri: [GIFT_CARD_ENHANCEMENT.md](GIFT_CARD_ENHANCEMENT.md)

### Loglara Nereden Bakılır

```bash
# Systemd logları
/var/log/journal/

# cPanel/WHM logları
/usr/local/cpanel/logs/

# Bot logları
sudo journalctl -u telegram-gift-bot
```

## ✅ Kurulum Kontrol Listesi

Kurulumu tamamladığınızda kontrol edin:

- [ ] Ubuntu sistemi güncel
- [ ] Python 3.8+ kurulu
- [ ] Git kurulu
- [ ] Bot kullanıcısı oluşturuldu
- [ ] Repository klonlandı
- [ ] Virtual environment oluşturuldu
- [ ] Bağımlılıklar yüklendi
- [ ] config.py oluşturuldu ve düzenlendi
- [ ] Bot token eklendi
- [ ] Cüzdan adresleri eklendi
- [ ] Gift card görselleri eklendi
- [ ] Dosya izinleri ayarlandı
- [ ] verify.py başarılı
- [ ] Manuel test başarılı
- [ ] Systemd service oluşturuldu
- [ ] Service aktif ve çalışıyor
- [ ] Firewall ayarlandı
- [ ] Yedekleme yapılandırıldı
- [ ] Cron job eklendi
- [ ] Telegram'da test edildi

## 🎉 Sonuç

Tebrikler! Bot artık Ubuntu + cPanel/WHM sunucunuzda çalışıyor.

### Sonraki Adımlar

1. **Test Edin**: Telegram'da bot'unuzla işlem yapın
2. **İzleyin**: İlk 24 saatte logları yakından takip edin
3. **Optimize Edin**: Performansı gözlemleyin ve gerekirse ayarlayın
4. **Duyurun**: Kullanıcılarınıza bot'un hazır olduğunu bildirin

### Güvenlik Hatırlatmaları

⚠️ **Önemli Güvenlik Notları:**
- config.py dosyasını asla paylaşmayın
- Bot token'ınızı güvende tutun
- Düzenli yedekleme yapın
- Logları kontrol edin
- Sistem güncellemelerini takip edin
- SSL sertifikası kullanın (Let's Encrypt)

**Başarılar!** 🚀

---

**Versiyon**: 1.0  
**Son Güncelleme**: 2026-01-28  
**Platform**: Ubuntu 20.04/22.04 + cPanel/WHM  
**Durum**: Production Ready ✅
