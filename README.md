# 🤖 Telegram MC/Visa Gift Card Bot - Versiyon 3.0

Bu proje, Telegram üzerinden otomatik olarak **MC (Mastercard) ve Visa Gift Card** satışı yapmanızı sağlayan gelişmiş bir bottur. Kullanıcılar minimum $20 bakiye yükleyerek, adet bazında gift card satın alabilir ve kart bilgilerini anında teslim alabilirler.

## ✨ Özellikler

- **💳 MC ve Visa Kartları:** Numerik ve resimli olmak üzere iki formatta gift card desteği
- **🔢 Adet Bazlı Sipariş:** Kullanıcılar tutar değil, adet olarak sipariş verir
- **💰 Bakiye Sistemi:** $20 minimum bakiye yükleme zorunluluğu
- **🔢 Otomatik Üretim:** 
  - MC kartları: 5 ile başlayan 16 haneli numara
  - Visa kartları: 4 ile başlayan 16 haneli numara
  - MM/YY formatında SKT
  - 3 haneli PIN kodu
- **🖼️ Görsel Desteği:** Picture kartlar için ön ve arka yüz görselleri
- **⚙️ Admin Paneli:** Stok ekleme, bakiye yönetimi ve istatistikler
- **🇹🇷 Çoklu Dil:** Türkçe ve İngilizce tam dil desteği

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
- Bir Telegram Bot Token'ı (BotFather'dan alınır)

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

3. **Ayarları yapın:**
   `config.py` dosyasını açın ve kendi bilgilerinizi girin:
   - `BOT_TOKEN`: BotFather'dan aldığınız token
   - `ADMIN_IDS`: Admin yetkisi verilecek kullanıcıların ID'leri
   - `CRYPTO_WALLETS`: Ödeme alınacak cüzdan adresleriniz

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
2. **Bakiye Yükle:** Minimum $20 bakiye yükleyin
3. **Kart Seç:** MC veya Visa, numerik veya resimli seçin
4. **Adet Gir:** Kaç adet kart almak istediğinizi belirtin
5. **Satın Al:** Onaylayın ve kart bilgilerinizi alın

### Admin Komutları

Admin paneline erişmek için config.py'de ADMIN_IDS listesinde olmalısınız.

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
├── telegram_bot.py          # Ana bot uygulaması
├── database.py              # Veritabanı ve kart yönetimi
├── config.py                # Konfigürasyon ayarları
├── translations.py          # Türkçe/İngilizce çeviriler
├── admin.py                 # Admin CLI araçları
├── giftcards/              # Gift card görselleri
│   ├── README.md           # Görsel isimlendirme kılavuzu
│   ├── mc1front.jpg        # Örnek MC ön yüz
│   ├── mc1back.jpg         # Örnek MC arka yüz
│   ├── visa1front.jpg      # Örnek Visa ön yüz
│   └── visa1back.jpg       # Örnek Visa arka yüz
├── requirements.txt         # Python bağımlılıkları
└── README.md               # Bu dosya
```

## 🔒 Güvenlik Notları

- **Üretim için:** `database.py` dosyasındaki `random` modülü yerine `secrets` modülü kullanın
- **Bot Token:** config.py dosyasını asla paylaşmayın
- **Admin IDs:** Sadece güvendiğiniz kişilere admin yetkisi verin
- **Bakiye:** Gerçek para işlemleri için ödeme gateway entegrasyonu gereklidir

## 📖 Dokümantasyon

Daha detaylı bilgi için:
- [Hızlı Başlangıç Rehberi (QUICKSTART.md)](QUICKSTART.md)
- [Geliştirici Detayları (IMPLEMENTATION_DETAILS.md)](IMPLEMENTATION_DETAILS.md)

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için lütfen önce bir issue açarak neyi değiştirmek istediğinizi belirtin.

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📧 İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.
