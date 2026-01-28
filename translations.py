"""
Multi-language support for the bot
Çoklu dil desteği
"""

TRANSLATIONS = {
    'tr': {
        # Main menu
        'welcome': '🎉 Hoş geldiniz {name}!\n\nBu bot ile hediye kartı satın alabilirsiniz.\n\n🎁 Hediye Kartlarını görüntülemek için aşağıdaki butonları kullanın.\n📦 Kategorilere göre de göz atabilirsiniz.\n💳 İstediğiniz kartı seçin ve satın alma işlemini tamamlayın.\n\nDaha fazla bilgi için /help kullanın.',
        'main_menu': '🏠 Ana Menü',
        'view_cards': '🎁 Hediye Kartlarını Görüntüle',
        'categories': '📂 Kategoriler',
        'admin_panel': '⚙️ Admin Paneli',
        'back': '🔙 Geri',
        'my_orders': '📦 Siparişlerim',
        'language': '🌐 Dil',
        
        # Card listing
        'no_cards': '😔 Şu anda hediye kartı bulunmamaktadır.',
        'available_cards': '🎁 **Mevcut Hediye Kartları:**\nDetayları görmek için birini seçin.',
        'no_categories': '😔 Kategori bulunamadı.',
        'categories_list': '📂 **Kategoriler:**',
        'no_cards_in_category': '😔 **{category}** kategorisinde kart bulunamadı.',
        'category_title': '📂 Kategori: **{category}**',
        
        # Card details
        'card_unavailable': '❌ Bu kart artık mevcut değil.',
        'card_detail': '🎁 *{name}*\n\n📝 {description}\n\n📂 Kategori: {category}\n💰 Fiyat: *{price}{currency}*\n📦 Stok: {stock}',
        'buy_now': '💳 Şimdi Satın Al',
        
        # Purchase
        'card_unavailable_alert': '❌ Kart mevcut değil!',
        'out_of_stock': '❌ Üzgünüz, bu kart stokta kalmamıştır.',
        'purchase_success': '✅ **Satın Alma Başarılı!**\n\n**{name}** satın aldığınız için teşekkür ederiz.\n\n👇 **KODUNUZ AŞAĞIDADİR (Görmek için tıklayın):**\n{code}\n\n⚠️ *Lütfen bu kodu kaydedin. Bu mesaj sadece sizin için.*',
        'purchase_error': '❌ İşlem sırasında hata oluştu.',
        'new_sale_admin': '💰 **Yeni Satış!**\nKullanıcı: {user}\nÜrün: {item}\nFiyat: {price}{currency}',
        
        # Coupon
        'enter_coupon': 'İndirim kodunuz varsa girin (yoksa "skip" yazın):',
        'coupon_applied': '✅ Kupon uygulandı! İndirim: {discount}',
        'coupon_invalid': '❌ Geçersiz kupon kodu.',
        'coupon_expired': '❌ Kupon süresi dolmuş.',
        'coupon_max_uses': '❌ Kupon kullanım limiti doldu.',
        
        # Admin
        'unauthorized': '⛔ Bu komutu kullanma yetkiniz yok.',
        'unauthorized_alert': '⛔ Sadece yetkili personel!',
        'admin_stats': '⚙️ **Admin Paneli**\n\n📊 **İstatistikler:**\nToplam Kart: {total}\nMevcut: {available}\nSatılan: {sold}\nToplam Gelir: {revenue}{currency}\n\nYeni kart eklemek için `/addcard` komutunu kullanın.\nKart silmek için `/deletecard <ID>` komutunu kullanın.',
        'low_stock_alert': '⚠️ **Düşük Stok Uyarısı!**\n\nAşağıdaki kartların stoku azalmış:\n{cards}',
        
        # Add card
        'addcard_format_error': '❌ **Yanlış Format!**\n\nKullanım:\n`/addcard İsim | Açıklama | Fiyat | Kategori | Kod | Stok`\n\nÖrnek:\n`/addcard Netflix 10$ | 1 Aylık Üyelik | 10 | Eğlence | NF-12345 | 5`',
        'addcard_price_error': '❌ Fiyat bir sayı olmalıdır (ör: 10 veya 10.5)',
        'addcard_success': '✅ **Hediye kartı başarıyla eklendi!**\n\n🎁 {name}\n💰 {price}{currency}\n📦 Stok: {stock}\nID: {id}',
        'addcard_error': '❌ Kart eklenirken bir hata oluştu.',
        
        # Delete card
        'deletecard_format_error': '❌ Kullanım: `/deletecard <ID>`',
        'deletecard_success': '✅ Kart ID: {id} başarıyla silindi.',
        'deletecard_not_found': '❌ Kart ID: {id} bulunamadı.',
        
        # Bulk add
        'bulkaddcard_usage': '📦 **Toplu Kart Ekleme**\n\nCSV veya JSON formatında dosya gönderin.\n\n**CSV Format:**\n```\nname,description,price,category,code,stock\nNetflix 10$,1 Aylık,10,Eğlence,NF-123,5\n```\n\n**JSON Format:**\n```json\n[\n  {\n    "name": "Netflix 10$",\n    "description": "1 Aylık",\n    "price": 10,\n    "category": "Eğlence",\n    "code": "NF-123",\n    "stock": 5\n  }\n]\n```',
        'bulkaddcard_success': '✅ Toplu ekleme tamamlandı!\n\n✅ Başarılı: {success}\n❌ Hatalı: {errors}',
        'bulkaddcard_errors': '\n\n**Hatalar:**\n{error_list}',
        'bulkaddcard_send_file': 'Lütfen CSV veya JSON dosyası gönderin.',
        'bulkaddcard_error': '❌ Dosya işlenirken hata oluştu: {error}',
        
        # Orders
        'no_orders': '📦 Henüz siparişiniz bulunmamaktadır.',
        'my_orders_title': '📦 **Siparişlerim**\n\n',
        'order_item': '🎁 {name}\n💰 {price}{currency}\n📅 {date}\n\n',
        
        # Coupons (Admin)
        'addcoupon_usage': '❌ Kullanım: `/addcoupon KOD | TİP | DEĞER | MAKS_KULLANIM | SÜRE`\n\nTİP: percentage veya fixed\nÖrnek: `/addcoupon YENI2024 | percentage | 10 | 100 | 30`\n(30 gün geçerli, %10 indirim, max 100 kullanım)',
        'addcoupon_success': '✅ Kupon oluşturuldu!\n\nKod: {code}\nİndirim: {discount}\nMax Kullanım: {max_uses}\nSüre: {expires}',
        'addcoupon_error': '❌ Kupon oluşturulurken hata: {error}',
        
        # Help
        'help': '📚 *Yardım*\n\n*Kullanıcı Komutları:*\n/start - Botu başlat\n/help - Bu yardım mesajını göster\n/myorders - Sipariş geçmişimi göster\n/language - Dil seçimi\n\n*Admin Komutları:*\n/addcard - Yeni hediye kartı ekle\n/deletecard - Hediye kartı sil\n/bulkaddcard - Toplu kart ekle\n/addcoupon - Kupon oluştur\n/deletecoupon - Kupon sil\n\n*Nasıl Kullanılır:*\n1️⃣ Kategorileri görüntüle\n2️⃣ Bir Hediye Kartı seç\n3️⃣ Detayları kontrol et\n4️⃣ Satın Al\'a tıkla\n5️⃣ Kodunuzu alın!\n\nDestek için admin ile iletişime geçin.',
        
        # Language
        'select_language': '🌐 **Dil Seçimi / Language Selection**\n\nLütfen dilinizi seçin / Please select your language:',
        'language_changed': '✅ Dil Türkçe olarak ayarlandı.',
        
        # Payment
        'select_payment_method': '💳 **Ödeme Yöntemi Seçin**\n\nToplam: {price}{currency}',
        'payment_method_paypal': '💰 PayPal',
        'payment_method_crypto': '₿ Kripto Para',
        'payment_method_manual': '👤 Manuel Ödeme',
        'paypal_instructions': '💰 **PayPal Ödemesi**\n\nLütfen {price}{currency} tutarını şu PayPal hesabına gönderin:\n{paypal_email}\n\nÖdeme sonrası işlem ID\'sini gönderin.',
        'crypto_select': '₿ **Kripto Para Seçin:**',
        'crypto_btc': '₿ Bitcoin (BTC)',
        'crypto_eth': '💎 Ethereum (ETH)',
        'crypto_ltc': '🔷 Litecoin (LTC)',
        'crypto_instructions': '{crypto} **Ödemesi**\n\nLütfen {amount} {crypto} gönderin:\n\n`{wallet}`\n\nÖdeme sonrası TX hash\'ini gönderin.',
        'payment_pending': '⏳ Ödemeniz işleme alındı. Onay sonrası kodunuz gönderilecek.',
        'payment_confirmed': '✅ Ödeme onaylandı!',
    },
    'en': {
        # Main menu
        'welcome': '🎉 Welcome {name}!\n\nYou can buy gift cards using this bot.\n\n🎁 Use the buttons below to view Gift Cards.\n📦 You can also browse by categories.\n💳 Select the card you want and complete the purchase.\n\nUse /help for more information.',
        'main_menu': '🏠 Main Menu',
        'view_cards': '🎁 View Gift Cards',
        'categories': '📂 Categories',
        'admin_panel': '⚙️ Admin Panel',
        'back': '🔙 Back',
        'my_orders': '📦 My Orders',
        'language': '🌐 Language',
        
        # Card listing
        'no_cards': '😔 No gift cards available at the moment.',
        'available_cards': '🎁 **Available Gift Cards:**\nSelect one to see details.',
        'no_categories': '😔 No categories found.',
        'categories_list': '📂 **Categories:**',
        'no_cards_in_category': '😔 No cards found in **{category}** category.',
        'category_title': '📂 Category: **{category}**',
        
        # Card details
        'card_unavailable': '❌ This card is no longer available.',
        'card_detail': '🎁 *{name}*\n\n📝 {description}\n\n📂 Category: {category}\n💰 Price: *{price}{currency}*\n📦 Stock: {stock}',
        'buy_now': '💳 Buy Now',
        
        # Purchase
        'card_unavailable_alert': '❌ Card unavailable!',
        'out_of_stock': '❌ Sorry, this card is out of stock.',
        'purchase_success': '✅ **Purchase Successful!**\n\nThank you for buying **{name}**.\n\n👇 **YOUR CODE IS BELOW (Click to reveal):**\n{code}\n\n⚠️ *Please save this code. This message is for you only.*',
        'purchase_error': '❌ Error processing transaction.',
        'new_sale_admin': '💰 **New Sale!**\nUser: {user}\nItem: {item}\nPrice: {price}{currency}',
        
        # Coupon
        'enter_coupon': 'Enter your discount code (or type "skip"):',
        'coupon_applied': '✅ Coupon applied! Discount: {discount}',
        'coupon_invalid': '❌ Invalid coupon code.',
        'coupon_expired': '❌ Coupon has expired.',
        'coupon_max_uses': '❌ Coupon usage limit reached.',
        
        # Admin
        'unauthorized': '⛔ You are not authorized to use this command.',
        'unauthorized_alert': '⛔ Authorized personnel only!',
        'admin_stats': '⚙️ **Admin Panel**\n\n📊 **Statistics:**\nTotal Cards: {total}\nAvailable: {available}\nSold: {sold}\nTotal Revenue: {revenue}{currency}\n\nUse `/addcard` command to add new cards.\nUse `/deletecard <ID>` command to delete cards.',
        'low_stock_alert': '⚠️ **Low Stock Alert!**\n\nThe following cards are running low:\n{cards}',
        
        # Add card
        'addcard_format_error': '❌ **Incorrect Format!**\n\nUsage:\n`/addcard Name | Description | Price | Category | Code | Stock`\n\nExample:\n`/addcard Netflix 10$ | 1 Month Sub | 10 | Entertainment | NF-12345 | 5`',
        'addcard_price_error': '❌ Price must be a number (e.g., 10 or 10.5)',
        'addcard_success': '✅ **Gift card added successfully!**\n\n🎁 {name}\n💰 {price}{currency}\n📦 Stock: {stock}\nID: {id}',
        'addcard_error': '❌ An error occurred while adding the card.',
        
        # Delete card
        'deletecard_format_error': '❌ Usage: `/deletecard <ID>`',
        'deletecard_success': '✅ Card ID: {id} deleted successfully.',
        'deletecard_not_found': '❌ Card ID: {id} not found.',
        
        # Bulk add
        'bulkaddcard_usage': '📦 **Bulk Card Addition**\n\nSend a CSV or JSON file.\n\n**CSV Format:**\n```\nname,description,price,category,code,stock\nNetflix 10$,1 Month,10,Entertainment,NF-123,5\n```\n\n**JSON Format:**\n```json\n[\n  {\n    "name": "Netflix 10$",\n    "description": "1 Month",\n    "price": 10,\n    "category": "Entertainment",\n    "code": "NF-123",\n    "stock": 5\n  }\n]\n```',
        'bulkaddcard_success': '✅ Bulk addition completed!\n\n✅ Successful: {success}\n❌ Failed: {errors}',
        'bulkaddcard_errors': '\n\n**Errors:**\n{error_list}',
        'bulkaddcard_send_file': 'Please send a CSV or JSON file.',
        'bulkaddcard_error': '❌ Error processing file: {error}',
        
        # Orders
        'no_orders': '📦 You have no orders yet.',
        'my_orders_title': '📦 **My Orders**\n\n',
        'order_item': '🎁 {name}\n💰 {price}{currency}\n📅 {date}\n\n',
        
        # Coupons (Admin)
        'addcoupon_usage': '❌ Usage: `/addcoupon CODE | TYPE | VALUE | MAX_USES | DAYS`\n\nTYPE: percentage or fixed\nExample: `/addcoupon NEW2024 | percentage | 10 | 100 | 30`\n(Valid 30 days, 10% discount, max 100 uses)',
        'addcoupon_success': '✅ Coupon created!\n\nCode: {code}\nDiscount: {discount}\nMax Uses: {max_uses}\nExpires: {expires}',
        'addcoupon_error': '❌ Error creating coupon: {error}',
        
        # Help
        'help': '📚 *Help*\n\n*User Commands:*\n/start - Start the bot\n/help - Show this help message\n/myorders - View order history\n/language - Language selection\n\n*Admin Commands:*\n/addcard - Add a new gift card\n/deletecard - Delete a gift card\n/bulkaddcard - Bulk add cards\n/addcoupon - Create a coupon\n/deletecoupon - Delete a coupon\n\n*How to Use:*\n1️⃣ View Categories\n2️⃣ Select a Gift Card\n3️⃣ Check Details\n4️⃣ Click Buy\n5️⃣ Get your Code!\n\nContact admin for support.',
        
        # Language
        'select_language': '🌐 **Language Selection / Dil Seçimi**\n\nPlease select your language / Lütfen dilinizi seçin:',
        'language_changed': '✅ Language set to English.',
        
        # Payment
        'select_payment_method': '💳 **Select Payment Method**\n\nTotal: {price}{currency}',
        'payment_method_paypal': '💰 PayPal',
        'payment_method_crypto': '₿ Cryptocurrency',
        'payment_method_manual': '👤 Manual Payment',
        'paypal_instructions': '💰 **PayPal Payment**\n\nPlease send {price}{currency} to this PayPal account:\n{paypal_email}\n\nSend the transaction ID after payment.',
        'crypto_select': '₿ **Select Cryptocurrency:**',
        'crypto_btc': '₿ Bitcoin (BTC)',
        'crypto_eth': '💎 Ethereum (ETH)',
        'crypto_ltc': '🔷 Litecoin (LTC)',
        'crypto_instructions': '{crypto} **Payment**\n\nPlease send {amount} {crypto} to:\n\n`{wallet}`\n\nSend the TX hash after payment.',
        'payment_pending': '⏳ Your payment is being processed. Code will be sent after confirmation.',
        'payment_confirmed': '✅ Payment confirmed!',
    }
}

def get_text(key: str, language: str = 'tr', **kwargs) -> str:
    """Get translated text
    Args:
        key: Translation key
        language: Language code ('tr' or 'en')
        **kwargs: Format parameters for the text
    """
    lang_dict = TRANSLATIONS.get(language, TRANSLATIONS['tr'])
    text = lang_dict.get(key, TRANSLATIONS['tr'].get(key, key))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    return text
