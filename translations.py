"""
Multi-language support for the bot
Çoklu dil desteği
"""

TRANSLATIONS = {
    'tr': {
        # Main menu
        'welcome': '🎉 Hoş geldiniz {name}!\n\nBu bot ile MC ve Visa hediye kartları satın alabilirsiniz.\n\n💳 Minimum yükleme: $20\n🎁 Numerik kartlar: $20/adet\n🖼️ Resimli kartlar: $50/adet\n\nDaha fazla bilgi için /help kullanın.',
        'main_menu': '🏠 Ana Menü',
        'view_balance': '💰 Bakiye',
        'add_balance': '➕ Bakiye Yükle',
        'buy_cards': '🎁 Kart Satın Al',
        'my_purchases': '📦 Satın Alımlarım',
        'admin_panel': '⚙️ Admin Paneli',
        'back': '🔙 Geri',
        'language': '🌐 Dil',
        
        # Balance
        'current_balance': '💰 **Mevcut Bakiye:** ${balance:.2f}',
        'minimum_balance_required': '⚠️ Minimum bakiye: $20.00',
        'balance_too_low': '❌ Yetersiz bakiye! Minimum $20 yükleme yapmalısınız.',
        'balance_added': '✅ Bakiye eklendi! Yeni bakiye: ${balance:.2f}',
        'enter_amount': 'Yüklemek istediğiniz tutarı girin (minimum $20):',
        'invalid_amount': '❌ Geçersiz tutar. Lütfen $20 veya daha fazla bir sayı girin.',
        
        # Card types
        'select_card_type': '🎁 **Kart Türü Seçin:**\n\n💳 Numerik Kartlar: $20/adet\n🖼️ Resimli Kartlar: $50/adet',
        'mc_numeric': '💳 MC Numerik ($20/adet)',
        'visa_numeric': '💳 Visa Numerik ($20/adet)',
        'mc_picture': '🖼️ MC Resimli ($50/adet)',
        'visa_picture': '🖼️ Visa Resimli ($50/adet)',
        
        # Quantity
        'enter_quantity': '📦 Kaç adet {card_type} satın almak istiyorsunuz?\n\n💰 Birim fiyat: ${price:.2f}\n💵 Mevcut bakiye: ${balance:.2f}',
        'invalid_quantity': '❌ Geçersiz adet. Lütfen pozitif bir sayı girin.',
        'insufficient_balance': '❌ Yetersiz bakiye!\n\n📊 Gerekli: ${required:.2f}\n💰 Mevcut: ${available:.2f}\n➖ Eksik: ${shortage:.2f}',
        'insufficient_stock': '❌ Stokta yeterli kart yok!\n\n📦 Mevcut: {available}\n🛒 İstenen: {requested}',
        
        # Purchase
        'purchase_confirmation': '🎁 **Satın Alma Onayı**\n\n📦 Kart türü: {card_type}\n🔢 Adet: {quantity}\n💰 Toplam: ${total:.2f}\n💵 Kalan bakiye: ${remaining:.2f}\n\nOnaylıyor musunuz?',
        'confirm': '✅ Onayla',
        'cancel': '❌ İptal',
        'purchase_success': '✅ **Satın Alma Başarılı!**\n\n{quantity} adet {card_type} satın aldınız.\n💰 Ödenen: ${amount:.2f}\n💵 Kalan bakiye: ${balance:.2f}\n\n📨 Kart bilgileriniz aşağıda:',
        'card_details': '\n\n━━━━━━━━━━━━━━━━━━\n🎁 **Kart #{index}**\n💳 Numara: `{card_number}`\n📅 SKT: `{exp_date}`\n🔢 PIN: `{pin}`',
        'card_details_picture': '\n\n━━━━━━━━━━━━━━━━━━\n🎁 **Kart #{index}**\n💳 Numara: `{card_number}`\n📅 SKT: `{exp_date}`\n🔢 PIN: `{pin}`\n🖼️ Ön yüz: {front}\n🖼️ Arka yüz: {back}',
        'purchase_error': '❌ Satın alma sırasında hata oluştu.',
        'purchase_cancelled': '❌ Satın alma iptal edildi.',
        
        # Purchases history
        'no_purchases': '📦 Henüz satın alımınız bulunmamaktadır.',
        'purchases_title': '📦 **Satın Alımlarım** ({count} kart)\n\n',
        'purchase_item': '🎁 {name}\n💳 ****{last4}\n📅 {date}\n💰 ${price:.2f}\n\n',
        
        # Admin
        'unauthorized': '⛔ Bu komutu kullanma yetkiniz yok.',
        'admin_stats': '⚙️ **Admin Paneli - MC/Visa Sistem**\n\n📊 **İstatistikler:**\n\n💳 MC Numerik:\n  • Mevcut: {mc_numeric_available}\n  • Satılan: {mc_numeric_sold}\n\n💳 Visa Numerik:\n  • Mevcut: {visa_numeric_available}\n  • Satılan: {visa_numeric_sold}\n\n🖼️ MC Resimli:\n  • Mevcut: {mc_picture_available}\n  • Satılan: {mc_picture_sold}\n\n🖼️ Visa Resimli:\n  • Mevcut: {visa_picture_available}\n  • Satılan: {visa_picture_sold}\n\n💰 Toplam Gelir: ${revenue:.2f}\n\nKomutlar:\n/addmcnumeric <adet> - MC numerik ekle\n/addvisanumeric <adet> - Visa numerik ekle\n/addmcpicture <id> - MC resimli ekle\n/addvisapicture <id> - Visa resimli ekle\n/addbalance <user_id> <tutar> - Bakiye ekle',
        
        # Add cards (Admin)
        'addcard_success': '✅ {count} adet {card_type} başarıyla eklendi!',
        'addcard_error': '❌ Kart eklenirken hata oluştu: {error}',
        'addcard_usage': '❌ Kullanım: {command} <adet>',
        'addpicture_usage': '❌ Kullanım: {command} <id>\n\nÖrnek: /addmcpicture 1\nGörseller: /giftcards/mc1front.jpg ve /giftcards/mc1back.jpg',
        
        # Add balance (Admin)
        'addbalance_usage': '❌ Kullanım: /addbalance <user_id> <tutar>',
        'addbalance_success': '✅ {user_id} kullanıcısına ${amount:.2f} eklendi.\nYeni bakiye: ${balance:.2f}',
        'addbalance_error': '❌ Bakiye eklenirken hata: {error}',
        'user_not_found': '❌ Kullanıcı bulunamadı.',
        
        # Help
        'help': '📚 **Yardım - MC/Visa Gift Card Bot**\n\n**Kullanıcı Komutları:**\n/start - Botu başlat\n/help - Yardım mesajı\n/balance - Bakiye görüntüle\n/buy - Kart satın al\n/purchases - Satın alımlarım\n\n**Nasıl Kullanılır:**\n1️⃣ Minimum $20 bakiye yükleyin\n2️⃣ Kart türünü seçin (MC/Visa)\n3️⃣ Numerik veya Resimli seçin\n4️⃣ Adet girin\n5️⃣ Satın alın!\n\n**Fiyatlar:**\n💳 Numerik: $20/adet\n🖼️ Resimli: $50/adet\n\n**Admin Komutları:**\n/admin - Admin paneli\n/addmcnumeric - MC numerik ekle\n/addvisanumeric - Visa numerik ekle\n/addmcpicture - MC resimli ekle\n/addvisapicture - Visa resimli ekle\n/addbalance - Kullanıcıya bakiye ekle',
        
        # Language
        'select_language': '🌐 **Dil Seçimi / Language Selection**\n\nLütfen dilinizi seçin / Please select your language:',
        'language_changed': '✅ Dil Türkçe olarak ayarlandı.',
    },
    'en': {
        # Main menu
        'welcome': '🎉 Welcome {name}!\n\nYou can buy MC and Visa gift cards with this bot.\n\n💳 Minimum balance: $20\n🎁 Numeric cards: $20/each\n🖼️ Picture cards: $50/each\n\nUse /help for more information.',
        'main_menu': '🏠 Main Menu',
        'view_balance': '💰 Balance',
        'add_balance': '➕ Add Balance',
        'buy_cards': '🎁 Buy Cards',
        'my_purchases': '📦 My Purchases',
        'admin_panel': '⚙️ Admin Panel',
        'back': '🔙 Back',
        'language': '🌐 Language',
        
        # Balance
        'current_balance': '💰 **Current Balance:** ${balance:.2f}',
        'minimum_balance_required': '⚠️ Minimum balance: $20.00',
        'balance_too_low': '❌ Insufficient balance! You must deposit at least $20.',
        'balance_added': '✅ Balance added! New balance: ${balance:.2f}',
        'enter_amount': 'Enter the amount to deposit (minimum $20):',
        'invalid_amount': '❌ Invalid amount. Please enter $20 or more.',
        
        # Card types
        'select_card_type': '🎁 **Select Card Type:**\n\n💳 Numeric Cards: $20/each\n🖼️ Picture Cards: $50/each',
        'mc_numeric': '💳 MC Numeric ($20/each)',
        'visa_numeric': '💳 Visa Numeric ($20/each)',
        'mc_picture': '🖼️ MC Picture ($50/each)',
        'visa_picture': '🖼️ Visa Picture ($50/each)',
        
        # Quantity
        'enter_quantity': '📦 How many {card_type} do you want to buy?\n\n💰 Unit price: ${price:.2f}\n💵 Current balance: ${balance:.2f}',
        'invalid_quantity': '❌ Invalid quantity. Please enter a positive number.',
        'insufficient_balance': '❌ Insufficient balance!\n\n📊 Required: ${required:.2f}\n💰 Available: ${available:.2f}\n➖ Short: ${shortage:.2f}',
        'insufficient_stock': '❌ Not enough cards in stock!\n\n📦 Available: {available}\n🛒 Requested: {requested}',
        
        # Purchase
        'purchase_confirmation': '🎁 **Purchase Confirmation**\n\n📦 Card type: {card_type}\n🔢 Quantity: {quantity}\n💰 Total: ${total:.2f}\n💵 Remaining balance: ${remaining:.2f}\n\nDo you confirm?',
        'confirm': '✅ Confirm',
        'cancel': '❌ Cancel',
        'purchase_success': '✅ **Purchase Successful!**\n\nYou bought {quantity} {card_type}.\n💰 Paid: ${amount:.2f}\n💵 Remaining balance: ${balance:.2f}\n\n📨 Your card details below:',
        'card_details': '\n\n━━━━━━━━━━━━━━━━━━\n🎁 **Card #{index}**\n💳 Number: `{card_number}`\n📅 Exp: `{exp_date}`\n🔢 PIN: `{pin}`',
        'card_details_picture': '\n\n━━━━━━━━━━━━━━━━━━\n🎁 **Card #{index}**\n💳 Number: `{card_number}`\n📅 Exp: `{exp_date}`\n🔢 PIN: `{pin}`\n🖼️ Front: {front}\n🖼️ Back: {back}',
        'purchase_error': '❌ Error during purchase.',
        'purchase_cancelled': '❌ Purchase cancelled.',
        
        # Purchases history
        'no_purchases': '📦 You have no purchases yet.',
        'purchases_title': '📦 **My Purchases** ({count} cards)\n\n',
        'purchase_item': '🎁 {name}\n💳 ****{last4}\n📅 {date}\n💰 ${price:.2f}\n\n',
        
        # Admin
        'unauthorized': '⛔ You are not authorized to use this command.',
        'admin_stats': '⚙️ **Admin Panel - MC/Visa System**\n\n📊 **Statistics:**\n\n💳 MC Numeric:\n  • Available: {mc_numeric_available}\n  • Sold: {mc_numeric_sold}\n\n💳 Visa Numeric:\n  • Available: {visa_numeric_available}\n  • Sold: {visa_numeric_sold}\n\n🖼️ MC Picture:\n  • Available: {mc_picture_available}\n  • Sold: {mc_picture_sold}\n\n🖼️ Visa Picture:\n  • Available: {visa_picture_available}\n  • Sold: {visa_picture_sold}\n\n💰 Total Revenue: ${revenue:.2f}\n\nCommands:\n/addmcnumeric <quantity> - Add MC numeric\n/addvisanumeric <quantity> - Add Visa numeric\n/addmcpicture <id> - Add MC picture\n/addvisapicture <id> - Add Visa picture\n/addbalance <user_id> <amount> - Add balance',
        
        # Add cards (Admin)
        'addcard_success': '✅ Successfully added {count} {card_type}!',
        'addcard_error': '❌ Error adding card: {error}',
        'addcard_usage': '❌ Usage: {command} <quantity>',
        'addpicture_usage': '❌ Usage: {command} <id>\n\nExample: /addmcpicture 1\nImages: /giftcards/mc1front.jpg and /giftcards/mc1back.jpg',
        
        # Add balance (Admin)
        'addbalance_usage': '❌ Usage: /addbalance <user_id> <amount>',
        'addbalance_success': '✅ Added ${amount:.2f} to user {user_id}.\nNew balance: ${balance:.2f}',
        'addbalance_error': '❌ Error adding balance: {error}',
        'user_not_found': '❌ User not found.',
        
        # Help
        'help': '📚 **Help - MC/Visa Gift Card Bot**\n\n**User Commands:**\n/start - Start the bot\n/help - Help message\n/balance - View balance\n/buy - Buy cards\n/purchases - My purchases\n\n**How to Use:**\n1️⃣ Deposit minimum $20 balance\n2️⃣ Select card type (MC/Visa)\n3️⃣ Choose Numeric or Picture\n4️⃣ Enter quantity\n5️⃣ Purchase!\n\n**Prices:**\n💳 Numeric: $20/each\n🖼️ Picture: $50/each\n\n**Admin Commands:**\n/admin - Admin panel\n/addmcnumeric - Add MC numeric\n/addvisanumeric - Add Visa numeric\n/addmcpicture - Add MC picture\n/addvisapicture - Add Visa picture\n/addbalance - Add balance to user',
        
        # Language
        'select_language': '🌐 **Language Selection / Dil Seçimi**\n\nPlease select your language / Lütfen dilinizi seçin:',
        'language_changed': '✅ Language set to English.',
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
