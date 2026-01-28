# Gift Card System Migration Guide

## Mevcut Sistemden Yeni Sisteme Geçiş

Bu rehber, eski gift card sisteminden yeni numerik detay ve ön/arka görsel sistemine geçiş için hazırlanmıştır.

## 🔄 Değişiklik Özeti

### Önceki Sistem
```python
GIFT_CARDS = {
    "mc_50": {
        "name": "Mastercard Gift Card $50",
        "amount": 50.0,
        "image_path": "gift_cards/mastercard_50.jpg",
        "description": "Mastercard $50 Gift Card"
    }
}
```

### Yeni Sistem
```python
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
    }
}
```

## ⚠️ Önemli: Geriye Dönük Uyumluluk

**İyi Haber**: Eski formatınız hala çalışacak! Hiçbir şeyi değiştirmek zorunda değilsiniz.

Ancak yeni özellikleri kullanmak isterseniz, aşağıdaki adımları izleyin.

## 📋 Adım Adım Geçiş

### Adım 1: Veritabanını Güncelle

Bot'u çalıştırdığınızda yeni tablo otomatik oluşur, ama elle de yapabilirsiniz:

```bash
# Bot'u durdurun
# Veritabanını yedekleyin
cp bot_database.db bot_database.db.backup

# Bot'u başlatın (yeni tablo otomatik oluşur)
python bot.py
```

Veya manuel:
```sql
sqlite3 bot_database.db << 'EOF'
CREATE TABLE IF NOT EXISTS gift_card_purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    card_id TEXT,
    card_name TEXT,
    card_number TEXT,
    exp_date TEXT,
    pin TEXT,
    amount REAL,
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
EOF
```

### Adım 2: Görselleri Hazırla

Her gift card için ön ve arka görsel hazırlayın:

```bash
# Mevcut görselleri yedekleyin
cd gift_cards
mkdir backup
cp *.jpg backup/

# Yeni görselleri ekleyin
# Örnek:
# mastercard_50.jpg -> mastercard_50_front.jpg (ön yüz)
#                   -> mastercard_50_back.jpg (arka yüz)
```

**Not**: Tek görseliniz varsa, onu `_front.jpg` olarak kopyalayabilirsiniz:
```bash
cp mastercard_50.jpg mastercard_50_front.jpg
```

### Adım 3: Kart Bilgilerini Oluştur

Her gift card için:

1. **Kart Numarası Oluştur** (16 hane)
   - Mastercard: 5'le başlar (örn: 5543554475829811)
   - Visa: 4'le başlar (örn: 4532123456789012)
   - Diğer: İstediğiniz format

2. **Son Kullanma Tarihi** (MM/YY)
   - Örnek: 02/27, 12/28, 06/29

3. **PIN Kodu** (3-4 hane)
   - Örnek: 097, 234, 5678

**Güvenlik**: Bu bilgileri güvenli bir yerde saklayın ve her kart için benzersiz kullanın.

### Adım 4: config.py'yi Güncelle

```python
# Eski format (hala çalışır)
"mc_50_old": {
    "name": "Mastercard Gift Card $50 (Old)",
    "amount": 50.0,
    "image_path": "gift_cards/mastercard_50.jpg",
    "description": "Mastercard $50 Gift Card"
}

# Yeni format (önerilen)
"mc_50": {
    "name": "Mastercard Gift Card $50",
    "amount": 50.0,
    "card_number": "5543554475829811",
    "exp_date": "02/27",
    "pin": "097",
    "image_front": "gift_cards/mastercard_50_front.jpg",
    "image_back": "gift_cards/mastercard_50_back.jpg",
    "description": "Mastercard $50 Gift Card"
}
```

### Adım 5: Test Et

```bash
# Bot'u yeniden başlat
python bot.py

# Test hesabıyla:
# 1. /start
# 2. Buy Gift Card
# 3. Yeni formatı seç
# 4. Her iki görselin de geldiğini kontrol et
# 5. Kart bilgilerinin göründüğünü kontrol et
```

## 🎯 Geçiş Stratejileri

### Strateji 1: Kademeli Geçiş (Önerilen)

```python
GIFT_CARDS = {
    # Yeni format gift card'lar
    "mc_50_v2": {
        "name": "Mastercard Gift Card $50 (New)",
        "amount": 50.0,
        "card_number": "5543554475829811",
        "exp_date": "02/27",
        "pin": "097",
        "image_front": "gift_cards/mastercard_50_front.jpg",
        "image_back": "gift_cards/mastercard_50_back.jpg",
        "description": "Mastercard $50 Gift Card - Full Details"
    },
    
    # Eski format (kullanıcılar alışkın)
    "mc_50": {
        "name": "Mastercard Gift Card $50",
        "amount": 50.0,
        "image_path": "gift_cards/mastercard_50.jpg",
        "description": "Mastercard $50 Gift Card"
    }
}
```

Zamanla eski formatı kaldırabilirsiniz.

### Strateji 2: Hemen Geçiş

Tüm gift card'ları aynı anda güncelleyin:

```bash
# 1. Bot'u durdurun
# 2. Veritabanını yedekleyin
# 3. Görselleri hazırlayın
# 4. config.py'yi güncelleyin
# 5. Test edin
# 6. Bot'u başlatın
```

### Strateji 3: Hibrit Yaklaşım

Bazı kartlar yeni format, bazıları eski:

```python
GIFT_CARDS = {
    # Premium kartlar - Yeni format
    "mc_100": {
        "name": "Mastercard Gift Card $100",
        "amount": 100.0,
        "card_number": "5543554475829822",
        "exp_date": "03/27",
        "pin": "198",
        "image_front": "gift_cards/mastercard_100_front.jpg",
        "image_back": "gift_cards/mastercard_100_back.jpg",
        "description": "Premium Mastercard"
    },
    
    # Ucuz kartlar - Eski format
    "amazon_25": {
        "name": "Amazon Gift Card $25",
        "amount": 25.0,
        "image_path": "gift_cards/amazon_25.jpg",
        "description": "Amazon $25"
    }
}
```

## ✅ Geçiş Kontrol Listesi

Geçişi tamamladınızdan emin olmak için:

- [ ] Veritabanı yedeklendi
- [ ] Yeni tablo oluşturuldu (`gift_card_purchases`)
- [ ] Mevcut görseller yedeklendi
- [ ] Ön yüz görselleri hazırlandı
- [ ] Arka yüz görselleri hazırlandı (opsiyonel)
- [ ] Her kart için kart numarası oluşturuldu
- [ ] Her kart için son kullanma tarihi belirlendi
- [ ] Her kart için PIN kodu oluşturuldu
- [ ] config.py güncellendi
- [ ] Test edildi (hem eski hem yeni format)
- [ ] Kullanıcılara duyuru yapıldı
- [ ] Dokümantasyon güncellendi

## 🔙 Geri Alma (Rollback)

Sorun olursa eski sisteme dönmek için:

```bash
# Bot'u durdurun
# Eski veritabanını geri yükleyin
cp bot_database.db.backup bot_database.db

# Eski config.py'yi geri yükleyin
# (yedek almayı unutmayın!)

# Bot'u başlatın
python bot.py
```

## 📊 Karşılaştırma

| Özellik | Eski Sistem | Yeni Sistem |
|---------|-------------|-------------|
| Kart Numarası | ❌ | ✅ |
| Son Kullanma | ❌ | ✅ |
| PIN | ❌ | ✅ |
| Ön Görsel | ✅ | ✅ |
| Arka Görsel | ❌ | ✅ |
| Veritabanı Kaydı | Kısmi | ✅ Tam |
| Geriye Dönük Uyumluluk | N/A | ✅ |

## ❓ Sık Sorulan Sorular

**S: Eski format gift card'larım çalışmaya devam eder mi?**
C: Evet! Sistem geriye dönük uyumlu.

**S: Tüm kartları aynı anda güncellemem gerekiyor mu?**
C: Hayır, kademeli geçiş yapabilirsiniz.

**S: Sadece ön görsel kullanabilir miyim?**
C: Evet, arka görsel opsiyonel.

**S: Gerçek kart numaraları kullanmalı mıyım?**
C: Hayır! Sahte ama benzersiz numaralar oluşturun.

**S: Eski müşterilerim etkilenir mi?**
C: Hayır, mevcut işlemler ve bakiyeler korunur.

**S: Görseller yoksa ne olur?**
C: Bot sadece kart bilgilerini metin olarak gönderir.

## 📞 Destek

Sorun yaşarsanız:
1. Test scriptini çalıştırın: `python test_gift_card.py`
2. Log'ları kontrol edin
3. GIFT_CARD_ENHANCEMENT.md dosyasını okuyun
4. GitHub'da issue açın

## 🎉 Sonuç

Geçiş tamamlandığında:
- ✅ Daha profesyonel görünüm
- ✅ Daha iyi takip
- ✅ Gelişmiş güvenlik
- ✅ Daha mutlu müşteriler

Başarılar! 🚀
