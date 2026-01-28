# Gift Card Enhancement - Feature Documentation

## Yeni Özellik: Numerik Gift Card Bilgileri ve Ön/Arka Görsel Desteği

Bu güncelleme ile gift card sistemi artık gerçek kredi kartı gibi detaylı bilgiler içerecek şekilde geliştirilmiştir.

## 🎁 Yeni Özellikler

### 1. Numerik Kart Bilgileri
- **16 Haneli Kart Numarası**: Örnek: `5543554475829811`
- **Son Kullanma Tarihi**: MM/YY formatında, Örnek: `02/27`
- **PIN Kodu**: 3-4 haneli güvenlik kodu, Örnek: `097`

### 2. Ön ve Arka Görsel Desteği
- **Ön Yüz Görseli**: Kart numarası ve detayların görülebileceği ön yüz
- **Arka Yüz Görseli**: PIN kodunun ve diğer bilgilerin olduğu arka yüz
- Her iki görsel de kullanıcıya otomatik olarak gönderilir

### 3. Veritabanı Kaydı
- Tüm satın alınan gift card'lar veritabanında saklanır
- Audit trail ve müşteri geçmişi takibi
- Kayıp kart durumunda bilgilerin tekrar gönderilebilmesi

## 📝 Konfigürasyon Örnekleri

### Tam Özellikli Gift Card (Önerilen)
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

### Sadece Ön Yüz ile
```python
GIFT_CARDS = {
    "visa_30": {
        "name": "Visa Gift Card $30",
        "amount": 30.0,
        "card_number": "4532123456789012",
        "exp_date": "12/28",
        "pin": "234",
        "image_front": "gift_cards/visa_30_front.jpg",
        "description": "Visa $30 Gift Card"
    }
}
```

### Eski Format (Geriye Dönük Uyumlu)
```python
GIFT_CARDS = {
    "amazon_25": {
        "name": "Amazon Gift Card $25",
        "amount": 25.0,
        "card_number": "AMZN-1234-5678-9012",
        "pin": "XYZABC",
        "image_path": "gift_cards/amazon_25.jpg",
        "description": "Amazon $25 Gift Card"
    }
}
```

## 💬 Kullanıcı Deneyimi

### Satın Alma Sonrası Mesaj

```
✅ Satın Alma Başarılı!

🎁 Mastercard Gift Card $50
💰 Tutar: $50.00

💳 Kart Numarası: 5543554475829811
📅 Son Kullanma Tarihi: 02/27
🔐 PIN: 097

📊 Kalan Bakiye: $450.00

İyi alışverişler!
```

### Görsel Gönderimi

1. **İlk Mesaj**: Ön yüz görseli + Tüm kart bilgileri (yukarıdaki mesaj caption olarak)
2. **İkinci Mesaj**: Arka yüz görseli + "🔙 Gift Card Arka Yüz" başlığı

### Markdown Formatı

Kart numarası ve PIN kodu `backtick` formatında gönderilir, böylece:
- Kopyalanması kolay
- Görsel olarak ayrışıyor
- Güvenli görünüyor

## 🗄️ Veritabanı Yapısı

Yeni `gift_card_purchases` tablosu:

```sql
CREATE TABLE gift_card_purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    card_id TEXT,
    card_name TEXT,
    card_number TEXT,
    exp_date TEXT,
    pin TEXT,
    amount REAL,
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

Bu tablo sayesinde:
- ✅ Hangi kullanıcının hangi kartı aldığı takip edilir
- ✅ Kayıp kart durumunda bilgiler tekrar gönderilebilir
- ✅ Satış raporları oluşturulabilir
- ✅ Fraud tespiti yapılabilir

## 🔄 Geriye Dönük Uyumluluk

Eski format gift card'lar hala çalışır:
- `image_path` kullanılabilir (tek görsel)
- `card_number`, `exp_date`, `pin` opsiyonel
- `image_front` yoksa otomatik `image_path` kullanılır
- Hiç görsel yoksa sadece metin gönderilir

## 📋 Checklist: Gift Card Eklerken

Gift card eklerken yapılması gerekenler:

### 1. Kart Bilgilerini Hazırla
- [ ] 16 haneli kart numarası oluştur
- [ ] Son kullanma tarihi belirle (MM/YY)
- [ ] PIN kodu oluştur (3-4 hane)

### 2. Görselleri Hazırla
- [ ] Ön yüz görseli oluştur (800x500 piksel, max 5MB)
- [ ] Arka yüz görseli oluştur (800x500 piksel, max 5MB)
- [ ] Görselleri `gift_cards/` klasörüne kaydet
- [ ] Dosya adları: `{card_id}_front.jpg` ve `{card_id}_back.jpg`

### 3. Config'e Ekle
- [ ] `config.py` dosyasını aç
- [ ] Yeni gift card için entry ekle
- [ ] Tüm alanları doldur (name, amount, card_number, exp_date, pin, image_front, image_back)
- [ ] Kaydet

### 4. Test Et
- [ ] Bot'u yeniden başlat
- [ ] Test kullanıcısıyla satın alma yap
- [ ] Her iki görselin de geldiğini kontrol et
- [ ] Kart bilgilerinin doğru göründüğünü kontrol et

## 🔒 Güvenlik Notları

### Önemli Uyarılar
⚠️ Gerçek kart bilgileri kullanmayın! Bu sadece gift card satışı içindir.

⚠️ `config.py` dosyası `.gitignore` içinde olmalı - asla GitHub'a pushlamamalı.

⚠️ Kart numaraları ve PIN kodları güvenli bir şekilde saklanmalı.

### Best Practices
- Her gift card için benzersiz numara kullanın
- Kullanılan kartları veritabanında işaretleyin
- Satılan kartların tekrar satılmamasını sağlayın
- Düzenli yedekleme yapın

## 📊 Admin İşlemleri

### Satılan Kartları Görme

```sql
SELECT 
    user_id,
    card_name,
    card_number,
    exp_date,
    pin,
    purchased_at
FROM gift_card_purchases
ORDER BY purchased_at DESC;
```

### Kullanıcının Satın Aldığı Kartlar

```sql
SELECT * FROM gift_card_purchases 
WHERE user_id = 123456789
ORDER BY purchased_at DESC;
```

## 🚀 Avantajlar

### Kullanıcı Perspektifi
✅ Gerçek kart gibi profesyonel görünüm
✅ Tüm bilgiler tek mesajda
✅ Ön ve arka yüz görselleri
✅ Kopyalanabilir kart numarası ve PIN
✅ Anında teslimat

### Admin Perspektifi
✅ Veritabanında tam kayıt
✅ Satış takibi
✅ Kayıp kart durumunda tekrar gönderebilme
✅ Raporlama imkanı
✅ Fraud tespiti

### Teknik Perspektif
✅ Modüler yapı
✅ Geriye dönük uyumlu
✅ Kolay test edilebilir
✅ İyi dokümante edilmiş
✅ Hata yönetimi mevcut

## 📝 Sonuç

Bu güncelleme ile gift card sistemi:
- ✨ Daha profesyonel
- 🔒 Daha güvenli
- 📊 Daha takip edilebilir
- 💯 Daha kullanıcı dostu

hale gelmiştir.

---

**Versiyon**: 2.0
**Tarih**: 2026-01-28
**Durum**: Production Ready ✅
