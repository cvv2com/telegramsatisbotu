# 📖 Implementation Details - MC/Visa Gift Card System

Bu dokümanda MC/Visa Gift Card Bot'un teknik detaylarını, mimari kararları ve implementasyon detaylarını bulabilirsiniz.

## 🏗️ Sistem Mimarisi

### Genel Bakış

```
┌─────────────────┐
│  Telegram User  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  telegram_bot.py│ ◄─── Ana bot uygulaması
└────────┬────────┘
         │
         ├──────► ┌─────────────┐
         │        │ database.py │ ◄─── Veri yönetimi
         │        └─────────────┘
         │
         ├──────► ┌────────────────┐
         │        │translations.py │ ◄─── Çoklu dil
         │        └────────────────┘
         │
         └──────► ┌──────────┐
                  │config.py │ ◄─── Ayarlar
                  └──────────┘
```

### Dosya Yapısı

#### telegram_bot.py
Ana Telegram bot uygulaması. Python-telegram-bot kütüphanesi kullanır.

**Önemli fonksiyonlar:**
- `start()`: Kullanıcıyı karşılar, ana menüyü gösterir
- `buy_cards_start()`: Kart satın alma akışını başlatır
- `view_balance()`: Kullanıcı bakiyesini gösterir
- `purchase_confirmed()`: Satın alma işlemini tamamlar

**Conversation States:**
```python
SELECTING_CARD_TYPE = 0   # Kart türü seçimi
ENTERING_QUANTITY = 1      # Adet girişi
CONFIRMING_PURCHASE = 2    # Onay
ENTERING_BALANCE = 3       # Bakiye girişi
```

#### database.py
JSON tabanlı veritabanı yönetimi. Thread-safe işlemler için lock kullanır.

**Veri Yapısı:**
```json
{
  "gift_cards": [
    {
      "id": 1,
      "name": "MC Gift Card $20",
      "price": 20.0,
      "category": "MC Numeric",
      "card_number": "5123456789012345",
      "exp_date": "12/25",
      "pin": "123",
      "status": "available",
      "stock": 1
    }
  ],
  "users": {
    "123456789": {
      "balance": 100.0,
      "language": "tr"
    }
  },
  "gift_card_purchases": [...],
  "orders": [...]
}
```

**Önemli metodlar:**
- `generate_card_number(card_type)`: Kart numarası üretir
- `add_mc_numeric_card(quantity)`: MC numerik kartlar ekler
- `purchase_cards_by_quantity(user_id, card_type, quantity)`: Satın alma işlemi
- `get_user_balance(user_id)`: Kullanıcı bakiyesi

#### config.py
Sistem konfigürasyonu.

**Önemli ayarlar:**
```python
GIFT_CARD_CONFIG = {
    "minimum_balance": 20.0,
    "numeric_card_price": 20.0,
    "picture_card_price": 50.0,
    "pin_length": 3
}
```

#### translations.py
Çoklu dil desteği. Türkçe ve İngilizce.

**Kullanım:**
```python
from translations import get_text
text = get_text('welcome', 'tr', name="Ali")
```

## 💳 Kart Üretim Sistemi

### MC (Mastercard) Kartlar

**BIN (Bank Identification Number):** 5 ile başlar

```python
def generate_card_number(card_type='mc'):
    prefix = '5'  # MC kartlar 5 ile başlar
    remaining = generate_random_digits(15)
    return prefix + remaining
```

**Örnek:**
- Kart No: `5548223511489855`
- SKT: `02/27`
- PIN: `353`

### Visa Kartlar

**BIN:** 4 ile başlar

```python
def generate_card_number(card_type='visa'):
    prefix = '4'  # Visa kartlar 4 ile başlar
    remaining = generate_random_digits(15)
    return prefix + remaining
```

**Örnek:**
- Kart No: `4548223511489855`
- SKT: `02/23`
- PIN: `090`

### SKT (Son Kullanma Tarihi)

MM/YY formatında, varsayılan 24 ay sonra:

```python
def generate_expiration_date(months_valid=24):
    exp_date = datetime.now() + timedelta(days=months_valid * 30)
    return exp_date.strftime('%m/%y').upper()
```

### PIN Kodu

3 haneli rastgele:

```python
def generate_pin(length=3):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])
```

## 🔐 Güvenlik Konuları

### 1. Rastgele Sayı Üretimi

**Mevcut:** `random` modülü (test için)
```python
import random
pin = ''.join([str(random.randint(0, 9)) for _ in range(3)])
```

**Üretim için önerilen:** `secrets` modülü
```python
import secrets
pin = ''.join([str(secrets.randbelow(10)) for _ in range(3)])
```

### 2. Bot Token Güvenliği

- `config.py` dosyasını `.gitignore`'a ekleyin
- Environment variables kullanın:
  ```python
  import os
  BOT_TOKEN = os.getenv('BOT_TOKEN')
  ```

### 3. Admin Yetkilendirme

Her admin komutunda kontrol:
```python
if user_id not in ADMIN_IDS:
    return "Unauthorized"
```

### 4. Veritabanı Thread Safety

Lock kullanımı:
```python
with self._lock:
    # Critical section
    self.data['users'][user_id]['balance'] += amount
    self._save()
```

## 💰 Bakiye Sistemi

### Bakiye Yönetimi

**Akış:**
1. Kullanıcı bakiye yükleme isteği gönderir
2. Bot ödeme bilgileri gösterir (simülasyon)
3. Admin/sistem bakiye onaylar
4. `add_balance(user_id, amount)` çağrılır

**Gerçek implementasyon için:**
- Stripe/PayPal webhook'ları
- Kripto para gateway entegrasyonu
- Manuel onay sistemi

### Bakiye Kontrolü

Satın alma öncesi:
```python
balance = db.get_user_balance(user_id)
total_price = quantity * price_per_card

if balance < total_price:
    return "Insufficient balance"
```

### Bakiye Kesintisi

Atomik işlem:
```python
with self._lock:
    if current_balance < amount:
        return False
    self.data['users'][user_id]['balance'] -= amount
    self._save()
    return True
```

## 🛒 Satın Alma Akışı

### 1. Kart Türü Seçimi

```
┌─────────────────────┐
│  🎁 Kart Satın Al   │
└──────────┬──────────┘
           │
           ├──► 💳 MC Numerik ($20)
           ├──► 💳 Visa Numerik ($20)
           ├──► 🖼️ MC Resimli ($50)
           └──► 🖼️ Visa Resimli ($50)
```

### 2. Adet Girişi

Kullanıcıdan metin input:
```python
quantity = int(update.message.text)
total = quantity * price_per_card
```

### 3. Bakiye Kontrolü

```python
if balance < total:
    show_insufficient_balance_message()
    return
```

### 4. Stok Kontrolü

```python
available = db.get_cards_by_category(category, status='available')
if len(available) < quantity:
    show_insufficient_stock_message()
    return
```

### 5. Onay

Inline keyboard ile:
```
┌─────────────────────────────┐
│ Toplam: $40                 │
│ Kalan bakiye: $60           │
│                             │
│ [✅ Onayla]  [❌ İptal]    │
└─────────────────────────────┘
```

### 6. İşlem

```python
success, message, cards = db.purchase_cards_by_quantity(
    user_id, 
    card_type, 
    quantity
)

if success:
    # Kart bilgilerini gönder
    for card in cards:
        send_card_details(card)
```

## 🖼️ Resimli Kart Sistemi

### Görsel Yönetimi

**Dosya isimlendirme:**
```
giftcards/
├── mc1front.jpg      # MC kart 1 ön yüz
├── mc1back.jpg       # MC kart 1 arka yüz
├── visa1front.jpg    # Visa kart 1 ön yüz
└── visa1back.jpg     # Visa kart 1 arka yüz
```

### Kart Ekleme

```python
card_id = db.add_mc_picture_card(1)
# Otomatik paths:
# image_front: /giftcards/mc1front.jpg
# image_back: /giftcards/mc1back.jpg
```

### Görsel Gösterimi

```python
images = db.get_card_images(card)
if images['front']:
    await bot.send_photo(photo=images['front'])
if images['back']:
    await bot.send_photo(photo=images['back'])
```

## 📊 İstatistikler ve Raporlama

### Admin İstatistikleri

```python
mc_numeric_available = len([c for c in mc_numeric if c['status'] == 'available'])
mc_numeric_sold = len([c for c in mc_numeric if c['status'] == 'sold'])
revenue = sum(c['price'] for c in all_cards if c['status'] == 'sold')
```

### Satın Alma Geçmişi

Her satın alma kaydedilir:
```python
purchase = {
    'id': purchase_id,
    'user_id': user_id,
    'card_id': card_id,
    'card_number': card['card_number'],
    'exp_date': card['exp_date'],
    'pin': card['pin'],
    'amount': card['price'],
    'purchased_at': datetime.now().isoformat()
}
```

## 🌐 Çoklu Dil Desteği

### Dil Seçimi

Kullanıcı tercihi veritabanında saklanır:
```python
db.set_user_language(user_id, 'tr')  # veya 'en'
```

### Metin Getirme

```python
lang = db.get_user_language(user_id)
text = get_text('welcome', lang, name=user.first_name)
```

### Yeni Dil Ekleme

`translations.py`'ye ekleyin:
```python
TRANSLATIONS = {
    'tr': {...},
    'en': {...},
    'es': {  # Yeni dil
        'welcome': '¡Bienvenido {name}!',
        ...
    }
}
```

## 🔧 Bakım ve Güncelleme

### Veritabanı Yedekleme

```bash
# JSON dosyasını kopyala
cp gift_cards.db.json gift_cards.db.json.backup

# Otomatik yedekleme (cron)
0 0 * * * cp /path/to/gift_cards.db.json /backups/$(date +\%Y\%m\%d).json
```

### Log Yönetimi

Bot log seviyesi ayarı:
```python
logging.basicConfig(
    level=logging.INFO,  # veya DEBUG, WARNING
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Performans İzleme

```python
import time

@functools.wraps(f)
def timed(f):
    start = time.time()
    result = f(*args, **kwargs)
    logger.info(f"{f.__name__} took {time.time()-start:.2f}s")
    return result
```

## 📈 Ölçeklendirme Önerileri

### 1. Veritabanı

JSON yerine:
- SQLite: Orta ölçek (1000+ kullanıcı)
- PostgreSQL: Büyük ölçek (10000+ kullanıcı)
- Redis: Cache katmanı

### 2. Asenkron İşlemler

Uzun işlemler için:
```python
async def long_operation():
    await asyncio.sleep(1)  # Simüle edilmiş işlem
    return result
```

### 3. Queue Sistemi

Celery ile arka plan işleri:
```python
@celery.task
def generate_bulk_cards(quantity):
    # Arka planda çalışır
    pass
```

### 4. CDN

Görsel dosyalar için:
- AWS S3 + CloudFront
- Cloudinary
- imgix

## 🧪 Test Önerileri

### Unit Tests

```python
def test_card_generation():
    card_num = generate_card_number('mc')
    assert card_num[0] == '5'
    assert len(card_num) == 16

def test_balance_deduction():
    db.add_balance(user_id, 100)
    assert db.deduct_balance(user_id, 50) == True
    assert db.get_user_balance(user_id) == 50
```

### Integration Tests

```python
def test_purchase_flow():
    # Bakiye ekle
    db.add_balance(user_id, 100)
    
    # Kart ekle
    db.add_mc_numeric_card(5)
    
    # Satın al
    success, msg, cards = db.purchase_cards_by_quantity(
        user_id, 'mc_numeric', 2
    )
    
    assert success == True
    assert len(cards) == 2
    assert db.get_user_balance(user_id) == 60
```

## 📞 Sorun Giderme

### Debug Modu

```python
# telegram_bot.py
logging.basicConfig(level=logging.DEBUG)

# Detaylı loglar
logger.debug(f"User {user_id} balance: {balance}")
logger.debug(f"Available cards: {len(available_cards)}")
```

### Yaygın Hatalar

1. **"Bot token invalid"**
   - Token'ı config.py'de kontrol edin
   - Boşluk veya satır sonu yok

2. **"Database permission denied"**
   - JSON dosya yazma izni
   - `chmod 644 gift_cards.db.json`

3. **"Conversation timeout"**
   - ConversationHandler timeout ayarı
   - Kullanıcıdan input bekleme süresi

## 🚀 İleri Seviye Özellikler

### Webhook Modu

Polling yerine webhook:
```python
application.run_webhook(
    listen='0.0.0.0',
    port=8443,
    url_path='bot',
    webhook_url='https://yourdomain.com/bot'
)
```

### Ödeme Gateway Entegrasyonu

```python
async def process_payment(user_id, amount):
    # Stripe örneği
    intent = stripe.PaymentIntent.create(
        amount=int(amount * 100),
        currency='usd'
    )
    return intent.client_secret
```

### Rate Limiting

```python
from functools import wraps
import time

def rate_limit(max_per_minute=5):
    def decorator(f):
        calls = []
        @wraps(f)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - 60]
            if len(calls) >= max_per_minute:
                raise Exception("Rate limit exceeded")
            calls.append(now)
            return f(*args, **kwargs)
        return wrapper
    return decorator
```

---

**Bu dokümantasyon sürekli güncellenmektedir. Katkılarınızı bekliyoruz!**
