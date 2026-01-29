# 🤖 Telegram Dijital Ürün Satış Botu

Bu proje, Telegram üzerinden otomatik olarak **Gift Card (Hediye Kartı)** ve dijital ürün satışı yapmanızı sağlayan gelişmiş bir bottur. Kullanıcılar kripto para ile bakiye yükleyebilir, ürünleri inceleyebilir ve satın aldıkları ürünlerin kodlarını/görsellerini anında teslim alabilirler.

## ✨ Özellikler

- **🛒 Otomatik Teslimat:** Satın alınan ürün bilgileri (Kod, PIN, SKT) anında kullanıcıya iletilir.
- **🖼️ G��rsel Desteği:** Ürünlerin ön ve arka yüz görsellerini gönderebilir.
- **💳 Bakiye Sistemi:** Kripto para (BTC, ETH, USDT, LTC) ile bakiye yükleme simülasyonu.
- **⚙️ Admin Paneli:** Stok ekleme, kullanıcı yönetimi ve istatistikler.
- **🔢 Otomatik Üretim:** Kart numarası ve PIN gibi bilgileri otomatik oluşturma seçeneği.
- **🇹🇷 Çoklu Dil:** Türkçe ve İngilizce dil desteği altyapısı.

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
   - `BOT_TOKEN`: BotFather'dan aldığınız token.
   - `ADMIN_IDS`: Admin yetkisi verilecek kullanıcıların ID'leri.
   - `CRYPTO_WALLETS`: Ödeme alınacak cüzdan adresleriniz.

4. **Botu başlatın:**
   ```bash
   python bot.py
   ```
   *(Alternatif olarak `start.bat` veya `start.sh` dosyalarını da kullanabilirsiniz.)*

## 📚 Dokümantasyon

Daha detaylı bilgi için proje içindeki diğer rehberlere göz atabilirsiniz:
- [Hızlı Başlangıç Rehberi (QUICKSTART.md)](QUICKSTART.md)
- [Geliştirici Detayları (IMPLEMENTATION_DETAILS.md)](IMPLEMENTATION_DETAILS.md)

---

## 🆕 Son Güncellemeler (Versiyon 2.0)

### Otomatik Kart Oluşturma
Sistem artık kart detaylarını (Numara, SKT, PIN) otomatik üretebilir. `config.py` üzerinden `GIFT_CARD_CONFIG` ayarını aktif etmeniz yeterlidir.

### Ön/Arka Yüz Desteği
Ürünlere artık hem ön hem de arka yüz görseli eklenebilir. Eski tek görselli sistem de desteklenmeye devam etmektedir.

### Satın Alma Geçmişi
Yeni `gift_card_purchases` tablosu ile kullanıcıların satın aldığı tüm kartların detaylı geçmişi tutulmaktadır.

---

## 🔄 Migrasyon Rehberi (Eski Sürümden Geçiş)

Eğer eski sürümü kullanıyorsanız, yeni özelliklere geçiş yapmak için aşağıdaki adımları izleyebilirsiniz. Sistem geriye dönük uyumludur, yani zorunlu değişiklik yapmadan da kullanmaya devam edebilirsiniz.

### Veritabanı Güncellemesi
Botu yeniden başlattığınızda yeni tablolar otomatik oluşturulur. Manuel işlem gerekmez.

### Config Dosyası Örneği (Yeni Format)
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
