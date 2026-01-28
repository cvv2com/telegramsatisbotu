"""
Ana bot dosyası - Main bot file
Telegram Gift Card Satış Botu / Telegram Gift Card Sales Bot
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes, ConversationHandler
)

import config
from database import GiftCardDB

# Logging ayarla
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Veritabanı
db = GiftCardDB(config.DATABASE_FILE)

# Conversation states
ADD_CARD_NAME, ADD_CARD_DESC, ADD_CARD_PRICE, ADD_CARD_CATEGORY, ADD_CARD_CODE, ADD_CARD_IMAGE = range(6)

def is_admin(user_id: int) -> bool:
    """Kullanıcının admin olup olmadığını kontrol et"""
    return user_id in config.ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start komutu - Hoş geldin mesajı"""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🎁 Gift Card'ları Görüntüle", callback_data='view_cards')],
        [InlineKeyboardButton("📂 Kategoriler", callback_data='categories')],
    ]
    
    if is_admin(user.id):
        keyboard.append([InlineKeyboardButton("⚙️ Admin Panel", callback_data='admin_panel')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
🎉 Hoş geldiniz {user.first_name}!

Bu bot üzerinden gift card satın alabilirsiniz.

🎁 Gift Card'ları görüntülemek için aşağıdaki butonları kullanın.
📦 Kategorilere göre arama yapabilirsiniz.
💳 Satın almak istediğiniz kartı seçin ve işlemi tamamlayın.
"""
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Button callback handler"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'view_cards':
        await show_all_cards(query, context)
    elif query.data == 'categories':
        await show_categories(query, context)
    elif query.data == 'admin_panel':
        await admin_panel(query, context)
    elif query.data.startswith('category_'):
        category = query.data.replace('category_', '')
        await show_cards_by_category(query, context, category)
    elif query.data.startswith('buy_'):
        card_id = int(query.data.replace('buy_', ''))
        await buy_card(query, context, card_id)
    elif query.data.startswith('confirm_buy_'):
        card_id = int(query.data.replace('confirm_buy_', ''))
        await confirm_purchase(query, context, card_id)
    elif query.data.startswith('view_card_'):
        card_id = int(query.data.replace('view_card_', ''))
        await view_card_details(query, context, card_id)
    elif query.data == 'add_card':
        await start_add_card(query, context)
    elif query.data == 'list_all_cards':
        await admin_list_cards(query, context)
    elif query.data == 'stats':
        await show_stats(query, context)
    elif query.data.startswith('delete_'):
        card_id = int(query.data.replace('delete_', ''))
        await delete_card(query, context, card_id)
    elif query.data == 'back_to_main':
        await back_to_main(query, context)

async def show_all_cards(query, context):
    """Tüm müsait kartları göster"""
    cards = db.get_all_cards(status='available')
    
    if not cards:
        await query.edit_message_text("😔 Şu anda satışta gift card bulunmuyor.")
        return
    
    text = "🎁 *Mevcut Gift Card'lar:*\n\n"
    keyboard = []
    
    for card in cards:
        text += f"🎫 *{card['name']}*\n"
        text += f"💰 Fiyat: {card['price']}{config.CURRENCY}\n"
        text += f"📂 Kategori: {card['category']}\n\n"
        
        keyboard.append([InlineKeyboardButton(
            f"🛒 {card['name']} - {card['price']}{config.CURRENCY}",
            callback_data=f"view_card_{card['id']}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data='back_to_main')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_categories(query, context):
    """Kategorileri göster"""
    categories = db.get_categories()
    
    if not categories:
        await query.edit_message_text(
            "📂 Henüz kategori eklenmemiş.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Ana Menü", callback_data='back_to_main')
            ]])
        )
        return
    
    keyboard = []
    for category in categories:
        cards_count = len(db.get_cards_by_category(category, status='available'))
        keyboard.append([InlineKeyboardButton(
            f"📂 {category} ({cards_count})",
            callback_data=f"category_{category}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data='back_to_main')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("📂 *Kategoriler:*", reply_markup=reply_markup, parse_mode='Markdown')

async def show_cards_by_category(query, context, category):
    """Kategoriye göre kartları göster"""
    cards = db.get_cards_by_category(category, status='available')
    
    if not cards:
        await query.edit_message_text(
            f"😔 {category} kategorisinde satışta card yok.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Kategoriler", callback_data='categories')
            ]])
        )
        return
    
    text = f"🎁 *{category} Kategorisi*\n\n"
    keyboard = []
    
    for card in cards:
        text += f"🎫 *{card['name']}*\n"
        text += f"💰 {card['price']}{config.CURRENCY}\n\n"
        
        keyboard.append([InlineKeyboardButton(
            f"🛒 {card['name']} - {card['price']}{config.CURRENCY}",
            callback_data=f"view_card_{card['id']}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Kategoriler", callback_data='categories')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def view_card_details(query, context, card_id):
    """Kart detaylarını göster"""
    card = db.get_card_by_id(card_id)
    
    if not card or card['status'] != 'available':
        await query.edit_message_text(
            "😔 Bu kart artık mevcut değil.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Ana Menü", callback_data='back_to_main')
            ]])
        )
        return
    
    text = f"🎁 *{card['name']}*\n\n"
    text += f"📝 {card['description']}\n\n"
    text += f"💰 Fiyat: *{card['price']}{config.CURRENCY}*\n"
    text += f"📂 Kategori: {card['category']}\n"
    
    keyboard = [
        [InlineKeyboardButton("✅ Satın Al", callback_data=f"buy_{card['id']}")],
        [InlineKeyboardButton("🔙 Geri", callback_data='view_cards')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if card['image_url']:
        try:
            await query.message.reply_photo(
                photo=card['image_url'],
                caption=text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            await query.message.delete()
        except:
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def buy_card(query, context, card_id):
    """Satın alma onayı"""
    card = db.get_card_by_id(card_id)
    
    if not card or card['status'] != 'available':
        await query.edit_message_text(
            "😔 Bu kart artık mevcut değil.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Ana Menü", callback_data='back_to_main')
            ]])
        )
        return
    
    text = f"🎁 *{card['name']}*\n\n"
    text += f"💰 Tutar: *{card['price']}{config.CURRENCY}*\n\n"
    text += "⚠️ *Önemli:*\n"
    text += "Satın alma işlemini onayladığınızda, gift card kodu size gönderilecektir.\n"
    text += "Bu işlem geri alınamaz!\n\n"
    text += "Devam etmek istiyor musunuz?"
    
    keyboard = [
        [InlineKeyboardButton("✅ Evet, Satın Al", callback_data=f"confirm_buy_{card['id']}")],
        [InlineKeyboardButton("❌ İptal", callback_data=f"view_card_{card['id']}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def confirm_purchase(query, context, card_id):
    """Satın almayı onayla ve kodu gönder"""
    user = query.from_user
    card = db.get_card_by_id(card_id)
    
    if not card or card['status'] != 'available':
        await query.edit_message_text(
            "😔 Bu kart artık mevcut değil.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Ana Menü", callback_data='back_to_main')
            ]])
        )
        return
    
    # Kartı satılmış olarak işaretle
    db.mark_as_sold(card_id, user.id)
    db.add_order(user.id, card_id, card['price'])
    
    # Kullanıcıya kodu gönder
    success_text = f"✅ *Satın Alma Başarılı!*\n\n"
    success_text += f"🎁 {card['name']}\n"
    success_text += f"💰 {card['price']}{config.CURRENCY}\n\n"
    success_text += f"🎫 *Gift Card Kodu:*\n`{card['code']}`\n\n"
    success_text += "Teşekkür ederiz! 🎉"
    
    await query.edit_message_text(success_text, parse_mode='Markdown')
    
    # Admin'lere bildirim gönder
    for admin_id in config.ADMIN_IDS:
        try:
            admin_text = f"💰 *Yeni Satış!*\n\n"
            admin_text += f"👤 Alıcı: {user.first_name} (@{user.username or 'N/A'})\n"
            admin_text += f"🎁 Ürün: {card['name']}\n"
            admin_text += f"💵 Tutar: {card['price']}{config.CURRENCY}"
            
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_text,
                parse_mode='Markdown'
            )
        except:
            pass

async def admin_panel(query, context):
    """Admin paneli"""
    user = query.from_user
    
    if not is_admin(user.id):
        await query.answer("⛔ Bu özelliğe erişim yetkiniz yok!", show_alert=True)
        return
    
    keyboard = [
        [InlineKeyboardButton("➕ Yeni Gift Card Ekle", callback_data='add_card')],
        [InlineKeyboardButton("📋 Tüm Kartları Listele", callback_data='list_all_cards')],
        [InlineKeyboardButton("📊 İstatistikler", callback_data='stats')],
        [InlineKeyboardButton("🔙 Ana Menü", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "⚙️ *Admin Panel*\n\nYapılacak işlemi seçin:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def start_add_card(query, context):
    """Gift card ekleme başlat"""
    user = query.from_user
    
    if not is_admin(user.id):
        await query.answer("⛔ Bu özelliğe erişim yetkiniz yok!", show_alert=True)
        return
    
    await query.edit_message_text(
        "➕ *Yeni Gift Card Ekleme*\n\n"
        "Lütfen `/addcard` komutunu kullanın:\n\n"
        "`/addcard <isim> | <açıklama> | <fiyat> | <kategori> | <kod> | [resim_url]`\n\n"
        "Örnek:\n"
        "`/addcard Steam 100TL | Steam cüzdan kodu | 100 | Steam | XXXX-YYYY-ZZZZ | https://...`",
        parse_mode='Markdown'
    )

async def add_card_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gift card ekle komutu"""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("⛔ Bu özelliğe erişim yetkiniz yok!")
        return
    
    try:
        # Parse command
        text = update.message.text.replace('/addcard ', '')
        parts = [p.strip() for p in text.split('|')]
        
        if len(parts) < 5:
            await update.message.reply_text(
                "❌ Hatalı format!\n\n"
                "Kullanım:\n"
                "`/addcard <isim> | <açıklama> | <fiyat> | <kategori> | <kod> | [resim_url]`",
                parse_mode='Markdown'
            )
            return
        
        name = parts[0]
        description = parts[1]
        price = float(parts[2])
        category = parts[3]
        code = parts[4]
        image_url = parts[5] if len(parts) > 5 else None
        
        card_id = db.add_gift_card(name, description, price, category, code, image_url)
        
        await update.message.reply_text(
            f"✅ Gift card başarıyla eklendi!\n\n"
            f"🎁 {name}\n"
            f"💰 {price}{config.CURRENCY}\n"
            f"ID: {card_id}"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Hata: {str(e)}")

async def admin_list_cards(query, context):
    """Admin için tüm kartları listele"""
    user = query.from_user
    
    if not is_admin(user.id):
        await query.answer("⛔ Bu özelliğe erişim yetkiniz yok!", show_alert=True)
        return
    
    cards = db.get_all_cards()
    
    if not cards:
        await query.edit_message_text(
            "📋 Henüz kart eklenmemiş.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_panel')
            ]])
        )
        return
    
    text = "📋 *Tüm Gift Card'lar:*\n\n"
    keyboard = []
    
    for card in cards:
        status_emoji = "✅" if card['status'] == 'available' else "❌"
        text += f"{status_emoji} ID:{card['id']} - {card['name']} - {card['price']}{config.CURRENCY} - {card['status']}\n"
        
        if card['status'] == 'available':
            keyboard.append([
                InlineKeyboardButton(
                    f"🗑️ Sil: {card['name']}",
                    callback_data=f"delete_{card['id']}"
                )
            ])
    
    keyboard.append([InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_panel')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def delete_card(query, context, card_id):
    """Kartı sil"""
    user = query.from_user
    
    if not is_admin(user.id):
        await query.answer("⛔ Bu özelliğe erişim yetkiniz yok!", show_alert=True)
        return
    
    if db.delete_card(card_id):
        await query.answer("✅ Kart silindi!")
        await admin_list_cards(query, context)
    else:
        await query.answer("❌ Kart bulunamadı!", show_alert=True)

async def show_stats(query, context):
    """İstatistikleri göster"""
    user = query.from_user
    
    if not is_admin(user.id):
        await query.answer("⛔ Bu özelliğe erişim yetkiniz yok!", show_alert=True)
        return
    
    stats = db.get_stats()
    
    text = "📊 *İstatistikler*\n\n"
    text += f"📦 Toplam Kart: {stats['total_cards']}\n"
    text += f"✅ Mevcut Kartlar: {stats['available_cards']}\n"
    text += f"💰 Satılan Kartlar: {stats['sold_cards']}\n"
    text += f"💵 Toplam Gelir: {stats['total_revenue']}{config.CURRENCY}\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_panel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def back_to_main(query, context):
    """Ana menüye dön"""
    user = query.from_user
    
    keyboard = [
        [InlineKeyboardButton("🎁 Gift Card'ları Görüntüle", callback_data='view_cards')],
        [InlineKeyboardButton("📂 Kategoriler", callback_data='categories')],
    ]
    
    if is_admin(user.id):
        keyboard.append([InlineKeyboardButton("⚙️ Admin Panel", callback_data='admin_panel')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
🎉 Hoş geldiniz {user.first_name}!

Bu bot üzerinden gift card satın alabilirsiniz.

🎁 Gift Card'ları görüntülemek için aşağıdaki butonları kullanın.
📦 Kategorilere göre arama yapabilirsiniz.
💳 Satın almak istediğiniz kartı seçin ve işlemi tamamlayın.
"""
    
    await query.edit_message_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yardım komutu"""
    help_text = """
📚 *Yardım*

*Kullanıcı Komutları:*
/start - Botu başlat
/help - Yardım mesajını göster

*Admin Komutları:*
/addcard - Yeni gift card ekle

*Kullanım:*
1️⃣ Kategorileri görüntüleyin
2️⃣ İstediğiniz gift card'ı seçin
3️⃣ Detayları inceleyin
4️⃣ Satın alın
5️⃣ Kodunuzu alın!

Herhangi bir sorun için lütfen admin ile iletişime geçin.
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Ana fonksiyon"""
    # Application oluştur
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Handler'ları ekle
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addcard", add_card_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Botu başlat
    logger.info("Bot başlatılıyor...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
