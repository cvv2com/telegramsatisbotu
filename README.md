# 🤖 Telegram MC/Visa Gift Card Bot - Versiyon 3.0 + Cryptomus Integration

Bu proje, Telegram üzerinden otomatik olarak **MC (Mastercard) ve Visa Gift Card** satışı yapmanızı sağlayan gelişmiş bir bottur. Kullanıcılar **Cryptomus** üzerinden kripto para ile ödeme yaparak (Bitcoin, Ethereum, USDT), adet bazında gift card satın alabilir ve kart bilgilerini anında teslim alabilirler.

## ✨ Özellikler

- **💳 MC ve Visa Kartları:** Numerik ve resimli olmak üzere iki formatta gift card desteği
- **🔢 Adet Bazlı Sipariş:** Kullanıcılar tutar değil, adet olarak sipariş verir
- **💰 Kripto Ödeme Sistemi:** Cryptomus entegrasyonu ile Bitcoin, Ethereum ve USDT (TRC-20) desteği
- **🔔 Otomatik Bildirimler:** Ödeme onaylandığında Telegram üzerinden anında bildirim
- **📊 MySQL Veritabanı:** Kalıcı ödeme kayıtları ve detaylı geçmiş
- **🔢 Otomatik Üretim:** 
  - MC kartları: 5 ile başlayan 16 haneli numara
  - Visa kartları: 4 ile başlayan 16 haneli numara
  - MM/YY formatında SKT
  - 3 haneli PIN kodu
- **🖼️ Görsel Desteği:** Picture kartlar için ön ve arka yüz görselleri
- **⚙️ Admin Paneli:** Stok ekleme, bakiye yönetimi, ödeme geçmişi ve istatistikler
- **🇹🇷 Çoklu Dil:** Türkçe ve İngilizce tam dil desteği
- **🔒 Güvenli:** Tüm API anahtarları ENV değişkenlerinde saklanır

## 💰 Fiyatlandırma

| Kart Türü | Fiyat | Açıklama |
|-----------|-------|----------|
| MC Numerik | $20/adet | Kart numarası, SKT ve PIN |
| Visa Numerik | $20/adet | Kart numarası, SKT ve PIN |
| MC Resimli | $50/adet | Ön/arka görsel + bilgiler |
| Visa Resimli | $50/adet | Ön/arka görsel + bilgiler |

## 🚀 Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- MySQL 5.7 veya üzeri
- Bir Telegram Bot Token'ı (BotFather'dan alınır)
- Cryptomus Merchant hesabı (https://cryptomus.com)

### Adım Adım Kurulum

1. **Repoyu indirin:**
   ```bash
   git clone https://github.com/cvv2com/telegramsatisbotu.git
   cd telegramsatisbotu
   ```

2. **Gerekli paketleri yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

3. **MySQL veritabanı kurun:**
   ```bash
   # MySQL'e bağlanın
   mysql -u root -p
   
   # Veritabanı oluşturun
   CREATE DATABASE telegram_sales_bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'botuser'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON telegram_sales_bot.* TO 'botuser'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   
   # Tabloları oluşturun
   python mysql_payment_db.py
   ```

4. **Cryptomus hesabı oluşturun:**
   - https://cryptomus.com adresinden kayıt olun
   - Merchant hesabınızı doğrulayın (KYB)
   - API ayarlarından Merchant ID ve API Key'leri alın

5. **Ayarları yapın:**
   `.env.example` dosyasını `.env` olarak kopyalayın ve düzenleyin:
   ```bash
   cp .env.example .env
   nano .env
   ```
   
   Aşağıdaki bilgileri girin:
   - `TELEGRAM_BOT_TOKEN`: BotFather'dan aldığınız token
   - `ADMIN_IDS`: Admin yetkisi verilecek kullanıcıların ID'leri
   - `CRYPTOMUS_MERCHANT_ID`: Cryptomus Merchant UUID
   - `CRYPTOMUS_PAYMENT_API_KEY`: Cryptomus Payment API Key
   - `MYSQL_*`: MySQL bağlantı bilgileri

6. **Webhook URL'ini yapılandırın:**
   `telegram_bot.py` içinde webhook URL'ini güncelleyin:
   ```python
   webhook_url = "https://your-domain.com/webhook/cryptomus"
   ```

7. **Servisleri başlatın:**
   
   **Terminal 1 - Webhook Handler:**
   ```bash
   python webhook_handler.py
   ```
   
   **Terminal 2 - Telegram Bot:**
   ```bash
   python telegram_bot.py
   ```

## 📖 Cryptomus Entegrasyonu

Detaylı Cryptomus entegrasyon rehberi için: **[CRYPTOMUS_INTEGRATION.md](CRYPTOMUS_INTEGRATION.md)**

### Desteklenen Kripto Paralar

- **Bitcoin (BTC)** - Bitcoin network
- **Ethereum (ETH)** - Ethereum network  
- **USDT** - Tether on Tron (TRC-20)

### Ödeme Akışı

1. Kullanıcı ödeme oluşturur
2. Cryptomus ödeme linki sağlar
3. Kullanıcı kripto ile ödeme yapar
4. Webhook otomatik olarak bildirim alır
5. Bakiye güncellenir
6. Telegram bildirimi gönderilir

4. **Görselleri ekleyin (isteğe bağlı):**
   Picture kartlar için görsel eklemek istiyorsanız:
   ```bash
   # Görselleri giftcards klasörüne ekleyin
   # Örnek: giftcards/mc1front.jpg, giftcards/mc1back.jpg
   ```

5. **Botu başlatın:**
   ```bash
   python telegram_bot.py
   ```

## 📚 Kullanım

### Kullanıcılar İçin

1. **Başlangıç:** `/start` komutu ile botu başlatın
2. **Ödeme Oluştur:** "💰 Create Payment" butonuna tıklayın
3. **Kripto Seç:** Bitcoin, Ethereum veya USDT seçin
4. **Miktar Gir:** Minimum $20 (maksimum $10,000)
5. **Ödeme Yap:** Cryptomus ödeme sayfasına yönlendirilirsiniz
6. **Onay Bekle:** Ödeme onaylandığında otomatik bildirim alırsınız
7. **Kart Al:** Bakiyeniz yüklendikten sonra kart satın alabilirsiniz

### Telegram Bot Komutları

**Kullanıcı Komutları:**
- `/start` - Botu başlat
- `/payment_history` - Ödeme geçmişinizi görüntüleyin

**Admin Komutları:**
- `/admin_payments [sayfa]` - Tüm ödemeleri listele
- `/payment_stats` - Ödeme istatistiklerini görüntüle

### Admin Komutları

Admin paneline erişmek için `.env` dosyasında `ADMIN_IDS` listesinde olmalısınız.

#### CLI Komutları (admin.py)

```bash
# İstatistikleri görüntüle
python admin.py stats

# MC numerik kart ekle (10 adet)
python admin.py addmcnumeric 10

# Visa numerik kart ekle (5 adet)
python admin.py addvisanumeric 5

# MC resimli kart ekle (ID: 1)
python admin.py addmcpicture 1

# Visa resimli kart ekle (ID: 2)
python admin.py addvisapicture 2

# Kullanıcıya bakiye ekle
python admin.py addbalance 123456789 100.50

# Tüm kullanıcıları listele
python admin.py users
```

## 🆕 Versiyon 3.1 - Cryptomus Integration

### Yeni Özellikler

- ✅ **Cryptomus Entegrasyonu:** PayPal yerine kripto para ödeme desteği
- ✅ **MySQL Veritabanı:** Kalıcı ödeme kayıtları
- ✅ **Otomatik Webhook:** Ödeme durumu otomatik güncellenir
- ✅ **Telegram Bildirimleri:** Ödeme onayı anında bildirilir
- ✅ **Admin Ödeme Paneli:** Tüm ödemeleri görüntüleme ve yönetme
- ✅ **Güvenli Konfigürasyon:** Tüm API anahtarları ENV değişkenlerinde

## 🆕 Versiyon 3.0 Değişiklikleri

### Tamamen Yeniden Yapılandırıldı

- ❌ **Kaldırıldı:** Netflix, Amazon vb. genel gift cardlar
- ✅ **Eklendi:** MC ve Visa özel gift card sistemi
- ✅ **Eklendi:** Adet bazlı sipariş sistemi
- ✅ **Eklendi:** Minimum $20 bakiye zorunluluğu
- ✅ **Eklendi:** Numerik ve resimli kart seçenekleri
- ✅ **Güncellendi:** 3 haneli PIN sistemi
- ✅ **Güncellendi:** MC kartlar 5 ile başlar
- ✅ **Güncellendi:** Visa kartlar 4 ile başlar

### Yeni Sistem Özellikleri

1. **Bakiye Yönetimi**
   - Kullanıcılar önce bakiye yükler
   - Minimum yükleme: $20
   - Bakiyeden otomatik kesinti

2. **Adet Bazlı Sipariş**
   - Tutar değil, adet seçilir
   - 1 numerik kart = $20
   - 1 resimli kart = $50

3. **Otomatik Kart Üretimi**
   - Gerçek BIN numaraları kullanılır
   - MC: 5 ile başlar (16 hane)
   - Visa: 4 ile başlar (16 hane)
   - SKT: MM/YY formatı
   - PIN: 3 haneli

## 📂 Proje Yapısı

```
telegramsatisbotu/
├── telegram_bot.py              # Ana bot uygulaması
├── webhook_handler.py           # Cryptomus webhook server (Flask)
├── cryptomus_payment.py         # Cryptomus API client
├── cryptomus_service.py         # Üst seviye ödeme servisi
├── mysql_payment_db.py          # MySQL veritabanı handler
├── database.py                  # JSON veritabanı (gift cards)
├── payment_handler.py           # Legacy payment handler
├── config.py                    # Konfigürasyon (ENV yükleme)
├── .env                         # Gizli anahtarlar (GIT'e eklenmez!)
├── .env.example                 # ENV şablon dosyası
├── translations.py              # Türkçe/İngilizce çeviriler
├── admin.py                     # Admin CLI araçları
├── giftcards/                   # Gift card görselleri
│   ├── README.md               # Görsel isimlendirme kılavuzu
│   ├── mc1front.jpg            # Örnek MC ön yüz
│   ├── mc1back.jpg             # Örnek MC arka yüz
│   ├── visa1front.jpg          # Örnek Visa ön yüz
│   └── visa1back.jpg           # Örnek Visa arka yüz
├── requirements.txt             # Python bağımlılıkları
├── README.md                    # Bu dosya
└── CRYPTOMUS_INTEGRATION.md     # Detaylı entegrasyon rehberi
```

## 🔒 Güvenlik Notları

### Genel Güvenlik
- **API Anahtarları:** Tüm API anahtarları `.env` dosyasında saklanır ve asla kod içine yazılmaz
- **`.env` Dosyası:** `.gitignore` ile Git'e eklenmez, paylaşılmaz
- **Webhook İmzalama:** Cryptomus webhook'ları HMAC-MD5 ile doğrulanır
- **HTTPS Zorunlu:** Webhook endpoint'leri HTTPS ile çalışmalıdır
- **MySQL Şifreleri:** Güçlü şifreler kullanın
- **Admin Yetkileri:** Sadece güvendiğiniz kişilere admin yetkisi verin

### Üretim İçin Öneriler
- **Secrets Modülü:** `database.py` içinde `random` yerine `secrets` modülü kullanın
- **Rate Limiting:** Webhook endpoint'lerine rate limiting ekleyin
- **IP Whitelisting:** Cryptomus IP'lerini whitelist'e ekleyin
- **Monitoring:** Ödeme ve sistem loglarını düzenli kontrol edin
- **Backup:** Veritabanı backup'ı düzenli alın
- **Firewall:** MySQL portunu (3306) sadece localhost'a açın

## 📖 Dokümantasyon

Daha detaylı bilgi için:
- [Cryptomus Entegrasyon Rehberi (CRYPTOMUS_INTEGRATION.md)](CRYPTOMUS_INTEGRATION.md)
- [Hızlı Başlangıç Rehberi (QUICKSTART.md)](QUICKSTART.md)
- [Geliştirici Detayları (IMPLEMENTATION_DETAILS.md)](IMPLEMENTATION_DETAILS.md)

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için lütfen önce bir issue açarak neyi değiştirmek istediğinizi belirtin.

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📧 İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.
