# Windows Kurulum Rehberi - Telegram Gift Card Sales Bot

Bu rehber Windows kullanıcıları için özel olarak hazırlanmıştır.

## Gereksinimler

- Windows 10 veya üzeri
- Python 3.8 veya üzeri ([İndir](https://www.python.org/downloads/))
  - **Önemli:** Python kurulurken "Add Python to PATH" seçeneğini işaretleyin!
- Telegram hesabı
- Metin editörü (Notepad++, VS Code, vb.)

## Hızlı Başlangıç (5 Dakika)

### 1. Python Kurulumu

1. [Python.org](https://www.python.org/downloads/) adresinden Python indir
2. İndirilen dosyayı çalıştır
3. **ÖNEMLİ:** "Add Python to PATH" kutucuğunu işaretle
4. "Install Now" butonuna tıkla

Kurulumu kontrol et:
```cmd
python --version
```

### 2. Bot Token Al

1. Telegram'da [@BotFather](https://t.me/BotFather) ile konuş
2. `/newbot` komutunu gönder
3. Bot adını belirle
4. Token'ı kopyala (örnek: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Projeyi Kur

Projeyi bir klasöre çıkart ve Command Prompt'u aç:

```cmd
cd C:\telegramsatisbotu-main
```

Kurulum scriptini çalıştır:
```cmd
setup.bat
```

Bu script:
- ✅ Python kurulumunu kontrol eder
- ✅ Sanal ortam (virtual environment) oluşturur
- ✅ Gerekli paketleri yükler
- ✅ config.py dosyasını oluşturur

### 4. Ayarları Yapılandır

`config.py` dosyasını aç (Notepad++ veya herhangi bir editör ile):

```python
# Bot token'ını değiştir
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # Buraya kendi token'ınızı yazın

# Kripto para cüzdan adreslerinizi ekleyin
CRYPTO_WALLETS = {
    "btc": "sizin_btc_adresiniz",
    "eth": "sizin_eth_adresiniz",
    "usdt": "sizin_usdt_adresiniz",
    "ltc": "sizin_ltc_adresiniz",
}
```

Dosyayı kaydet ve kapat.

### 5. Bot'u Başlat

```cmd
start.bat
```

Bot çalışmaya başladığında Telegram'da botunuzu bulup `/start` gönderin!

## Komutlar

### Bot'u Başlat
```cmd
start.bat
```

### Bot'u Durdur
Command Prompt penceresinde `Ctrl+C` tuşlarına bas

### Konfigürasyonu Kontrol Et
```cmd
python verify.py
```

### Admin İşlemleri

Kullanıcıları listele:
```cmd
python admin.py users
```

Kullanıcı bilgilerini gör:
```cmd
python admin.py user 123456789
```

Bakiye ekle (ödeme aldıktan sonra):
```cmd
python admin.py add 123456789 100.00
```

İstatistikleri gör:
```cmd
python admin.py stats
```

## Gift Card Görselleri Ekleme

1. `gift_cards` klasörünü aç
2. Gift card görsellerini bu klasöre kopyala:
   - `mastercard_50.jpg`
   - `visa_30.jpg`
   - `amazon_25.jpg`
   - vb.

Görseller:
- Format: JPG veya PNG
- Önerilen boyut: 800x500 piksel
- Maksimum: 5MB

## Sorun Giderme

### "Python bulunamadı" Hatası

**Çözüm:**
1. Python'u tekrar kur
2. Kurulumda "Add Python to PATH" seçeneğini işaretle
3. Command Prompt'u kapat ve tekrar aç

### "'cp' tanınan bir komut değil" Hatası

**Çözüm:** Windows'ta `copy` komutunu kullanın:
```cmd
copy config.example.py config.py
```

### "config.py bulunamadı" Hatası

**Çözüm:**
```cmd
copy config.example.py config.py
notepad config.py
```
Token'ınızı ekleyin ve kaydedin.

### "ModuleNotFoundError: No module named 'telegram'" Hatası

**Çözüm:**
```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

### Bot çalışmıyor

1. Konfigürasyonu kontrol et:
```cmd
python verify.py
```

2. Log'ları kontrol et - hata mesajlarını oku

3. Bot token'ının doğru olduğundan emin ol

### Gift Card Görseli Gönderilmiyor

1. Dosya adlarının `config.py` ile eşleştiğinden emin ol
2. Görsellerin `gift_cards` klasöründe olduğunu kontrol et
3. Dosya izinlerini kontrol et

## Arka Planda Çalıştırma

### Seçenek 1: Pencereyi Minimize Et
Start.bat ile başlattıktan sonra pencereyi minimize edin. Kapatmayın!

### Seçenek 2: NSSM (Önerilen)

1. [NSSM](https://nssm.cc/download) indir
2. NSSM ile servis oluştur:

```cmd
nssm install TelegramGiftBot "C:\telegramsatisbotu-main\venv\Scripts\python.exe" "C:\telegramsatisbotu-main\bot.py"
nssm set TelegramGiftBot AppDirectory "C:\telegramsatisbotu-main"
nssm start TelegramGiftBot
```

Servisi yönet:
```cmd
nssm stop TelegramGiftBot     REM Durdur
nssm start TelegramGiftBot    REM Başlat
nssm restart TelegramGiftBot  REM Yeniden başlat
nssm remove TelegramGiftBot   REM Kaldır
```

## Güncellemeler

Projeyi güncellemek için:

1. Yeni dosyaları indir
2. `config.py` ve `bot_database.db` dosyalarını yedekle
3. Yeni dosyaları üzerine kopyala
4. `config.py` ve `bot_database.db` dosyalarını geri koy
5. Gerekirse bağımlılıkları güncelle:
```cmd
venv\Scripts\activate
pip install -U -r requirements.txt
```

## Yedekleme

Veritabanını düzenli yedekle:

```cmd
REM Manuel yedekleme
copy bot_database.db backups\bot_database_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db

REM Otomatik yedekleme için Windows Task Scheduler kullan
```

## Performans İpuçları

- Düşük kaynak kullanımı için servisi kullan
- Veritabanını düzenli olarak optimize et
- Log dosyalarını düzenli temizle
- Sadece gerekli gift card'ları aktif tut

## Güvenlik

⚠️ **Önemli Güvenlik Notları:**

1. `config.py` dosyasını kimseyle paylaşma
2. Bot token'ını gizli tut
3. Windows Firewall'u aktif tut
4. Düzenli güvenlik güncellemelerini yap
5. Antivirüs yazılımı kullan

## Yardım

Sorun mu yaşıyorsunuz?

1. `python verify.py` çalıştırın
2. DEPLOYMENT.md dosyasını okuyun
3. GitHub'da issue açın
4. Log dosyalarını kontrol edin

## Lisans

Bu proje açık kaynak kodludur.

---

**Windows Özel Komutlar Özeti:**

```cmd
setup.bat              # İlk kurulum
start.bat              # Bot'u başlat
python verify.py       # Ayarları kontrol et
python admin.py users  # Kullanıcıları listele
python admin.py add USER_ID AMOUNT  # Bakiye ekle
```

Başarılar! 🚀
