# Gift Card Images Directory

Bu klasörde gift card görsellerini saklayın.

## Gerekli Görsel Dosyaları

### Yeni Format (Ön ve Arka Yüz)

Gift card'lar artık ön ve arka yüz görsellerini destekliyor:

- `mastercard_50_front.jpg` - Mastercard $50 Ön Yüz
- `mastercard_50_back.jpg` - Mastercard $50 Arka Yüz
- `visa_30_front.jpg` - Visa $30 Ön Yüz
- `visa_30_back.jpg` - Visa $30 Arka Yüz

### Eski Format (Tek Görsel - Hala Destekleniyor)

Geriye dönük uyumluluk için tek görsel de kullanılabilir:

- `amazon_25.jpg` - Amazon $25 Gift Card (tek görsel)

## Gift Card Konfigürasyonu

`config.py` dosyasında her gift card için şu bilgileri tanımlayın:

```python
GIFT_CARDS = {
    "mc_50": {
        "name": "Mastercard Gift Card $50",
        "amount": 50.0,
        "card_number": "5543554475829811",  # 16 haneli kart numarası
        "exp_date": "02/27",                 # Son kullanma tarihi (MM/YY)
        "pin": "097",                        # PIN kodu
        "image_front": "gift_cards/mastercard_50_front.jpg",
        "image_back": "gift_cards/mastercard_50_back.jpg",
        "description": "Mastercard $50 Gift Card"
    },
}
```

## Görsel Özellikleri

- Format: JPG veya PNG
- Önerilen boyut: 800x500 piksel (ön yüz), 800x500 piksel (arka yüz)
- Maksimum dosya boyutu: 5MB (her görsel için)

## Özellikler

### Yeni Özellikler (v2.0)
- ✅ 16 haneli kart numarası desteği
- ✅ Son kullanma tarihi (MM/YY formatında)
- ✅ PIN kodu desteği
- ✅ Ön ve arka yüz görselleri
- ✅ Veritabanında satın alınan kartların kaydı

### Geriye Dönük Uyumluluk
- ✅ Tek görsel (`image_path`) hala destekleniyor
- ✅ Kart numarası, tarih ve PIN opsiyonel
- ✅ Sadece ön yüz görseli kullanılabilir

## Kullanım Örnekleri

### 1. Tam Özellikli Gift Card (Önerilen)
```python
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

### 2. Sadece Ön Yüz
```python
"visa_30": {
    "name": "Visa Gift Card $30",
    "amount": 30.0,
    "card_number": "4532123456789012",
    "exp_date": "12/28",
    "pin": "234",
    "image_front": "gift_cards/visa_30_front.jpg",
    "description": "Visa $30 Gift Card"
}
```

### 3. Eski Format (Geriye Dönük Uyumluluk)
```python
"amazon_25": {
    "name": "Amazon Gift Card $25",
    "amount": 25.0,
    "card_number": "AMZN-1234-5678-9012",
    "pin": "XYZABC",
    "image_path": "gift_cards/amazon_25.jpg",
    "description": "Amazon $25 Gift Card"
}
```

## Not

Gift card görselleri yoksa, bot satın alma işlemini tamamlar ancak görsel yerine sadece kart bilgilerini (numara, tarih, PIN) metin mesajı olarak gönderir.
