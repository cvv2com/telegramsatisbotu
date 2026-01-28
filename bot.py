#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Gift Card Sales Bot
Otomatik gift card satış botu
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import sqlite3
from datetime import datetime
from config import BOT_TOKEN, CRYPTO_WALLETS, GIFT_CARDS

# Constants
MAX_TRANSACTION_HISTORY = 10  # Maximum number of transactions to show in history

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database başlatma
def init_db():
    """Veritabanını başlat"""
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    # Kullanıcılar tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # İşlemler tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            transaction_type TEXT,
            amount REAL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user_balance(user_id: int) -> float:
    """Kullanıcının bakiyesini getir"""
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result[0]
    return 0.0

def create_or_get_user(user_id: int, username: str = None):
    """Kullanıcı oluştur veya mevcut kullanıcıyı getir"""
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    if not cursor.fetchone():
        cursor.execute(
            'INSERT INTO users (user_id, username, balance) VALUES (?, ?, 0.0)',
            (user_id, username)
        )
        conn.commit()
    
    conn.close()

def update_balance(user_id: int, amount: float, transaction_type: str, description: str):
    """Kullanıcı bakiyesini güncelle ve işlem kaydı oluştur"""
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    if transaction_type == 'purchase':
        # Check balance before deduction to prevent negative balance
        cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        if result and result[0] >= amount:
            cursor.execute(
                'UPDATE users SET balance = balance - ? WHERE user_id = ?',
                (amount, user_id)
            )
        else:
            conn.close()
            raise ValueError("Insufficient balance for purchase")
    else:  # deposit
        cursor.execute(
            'UPDATE users SET balance = balance + ? WHERE user_id = ?',
            (amount, user_id)
        )
    
    cursor.execute(
        'INSERT INTO transactions (user_id, transaction_type, amount, description) VALUES (?, ?, ?, ?)',
        (user_id, transaction_type, amount, description)
    )
    
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start komutu - Ana menü"""
    user = update.effective_user
    create_or_get_user(user.id, user.username)
    
    keyboard = [
        [
            InlineKeyboardButton("💰 Balance", callback_data='balance'),
            InlineKeyboardButton("🛒 Buy Gift Card", callback_data='buy')
        ],
        [
            InlineKeyboardButton("❓ How to Buy", callback_data='how'),
            InlineKeyboardButton("📊 Transaction History", callback_data='history')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        f"🎉 Hoş geldiniz {user.first_name}!\n\n"
        f"Gift Card satış botuna hoş geldiniz. "
        f"Kripto para ile güvenli bir şekilde gift card satın alabilirsiniz.\n\n"
        f"Lütfen aşağıdaki menüden bir seçenek seçin:"
    )
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buton tıklamalarını işle"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == 'balance':
        await show_balance(query, user_id)
    elif query.data == 'buy':
        await show_gift_cards(query, user_id)
    elif query.data == 'how':
        await show_how_to_buy(query)
    elif query.data == 'history':
        await show_transaction_history(query, user_id)
    elif query.data == 'main_menu':
        await show_main_menu(query)
    elif query.data.startswith('crypto_'):
        await show_crypto_wallet(query, query.data.split('_')[1])
    elif query.data.startswith('buy_'):
        await process_gift_card_purchase(query, user_id, query.data.split('_', 1)[1])

async def show_balance(query, user_id: int):
    """Bakiye göster"""
    balance = get_user_balance(user_id)
    
    keyboard = [
        [InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"💰 Mevcut Bakiyeniz\n\n"
        f"Bakiye: ${balance:.2f}\n\n"
    )
    
    if balance == 0:
        message += (
            "⚠️ Bakiyeniz bulunmamaktadır.\n"
            "Bakiye yüklemek için 'How to Buy' bölümünü ziyaret edin."
        )
    
    await query.edit_message_text(message, reply_markup=reply_markup)

async def show_gift_cards(query, user_id: int):
    """Satın alınabilir gift card'ları göster"""
    balance = get_user_balance(user_id)
    
    keyboard = []
    for card_id, card_info in GIFT_CARDS.items():
        button_text = f"{card_info['name']} ${card_info['amount']}"
        if balance >= card_info['amount']:
            button_text += " ✅"
        else:
            button_text += " ❌"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f'buy_{card_id}')])
    
    keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"🎁 Gift Card Seçenekleri\n\n"
        f"Mevcut bakiyeniz: ${balance:.2f}\n\n"
        f"Satın almak istediğiniz gift card'ı seçin:\n"
        f"(✅ Yeterli bakiye | ❌ Yetersiz bakiye)"
    )
    
    await query.edit_message_text(message, reply_markup=reply_markup)

async def show_how_to_buy(query):
    """Nasıl satın alınır - Kripto cüzdan adreslerini göster"""
    keyboard = []
    for crypto_name in CRYPTO_WALLETS.keys():
        keyboard.append([InlineKeyboardButton(
            f"💎 {crypto_name.upper()} Wallet",
            callback_data=f'crypto_{crypto_name}'
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        "❓ Nasıl Satın Alınır?\n\n"
        "1️⃣ Aşağıdaki kripto para seçeneklerinden birini seçin\n"
        "2️⃣ Gösterilen cüzdan adresine ödeme yapın\n"
        "3️⃣ Ödeme yaptıktan sonra admin onayını bekleyin\n"
        "4️⃣ Admin onayından sonra bakiyeniz yüklenecektir\n"
        "5️⃣ Bakiyeniz ile gift card satın alabilirsiniz\n\n"
        "⚠️ Önemli: Ödemeler manuel olarak kontrol edilir ve onaylanır.\n"
        "Admin onayı genellikle 1-24 saat içinde yapılır.\n\n"
        "Ödeme yapmak için bir kripto para seçin:"
    )
    
    await query.edit_message_text(message, reply_markup=reply_markup)

async def show_crypto_wallet(query, crypto: str):
    """Seçilen kripto para için cüzdan adresini göster"""
    if crypto not in CRYPTO_WALLETS:
        await query.edit_message_text("❌ Geçersiz kripto para!")
        return
    
    wallet_address = CRYPTO_WALLETS[crypto]
    
    keyboard = [
        [InlineKeyboardButton("🔙 Geri", callback_data='how')],
        [InlineKeyboardButton("🏠 Ana Menü", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"💎 {crypto.upper()} Wallet Address\n\n"
        f"Cüzdan Adresi:\n"
        f"`{wallet_address}`\n\n"
        f"⚠️ Önemli:\n"
        f"• Sadece {crypto.upper()} gönderin!\n"
        f"• Minimum miktar: $10\n"
        f"• Ödemeniz manuel olarak kontrol edilir\n"
        f"• Bakiye yüklemesi admin onayı ile yapılır\n"
        f"• Onay süresi: 1-24 saat\n\n"
        f"Yukarıdaki adrese {crypto.upper()} gönderin. "
        f"Ödemeniz admin tarafından onaylandığında bakiyeniz güncellenecektir."
    )
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_transaction_history(query, user_id: int):
    """İşlem geçmişini göster"""
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT transaction_type, amount, description, created_at FROM transactions WHERE user_id = ? ORDER BY created_at DESC LIMIT ?',
        (user_id, MAX_TRANSACTION_HISTORY)
    )
    transactions = cursor.fetchall()
    conn.close()
    
    keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if not transactions:
        message = "📊 İşlem Geçmişi\n\nHenüz işlem bulunmamaktadır."
    else:
        message = f"📊 İşlem Geçmişi (Son {MAX_TRANSACTION_HISTORY})\n\n"
        for trans in transactions:
            trans_type, amount, desc, created = trans
            emoji = "➕" if trans_type == "deposit" else "➖"
            message += f"{emoji} ${amount:.2f} - {desc}\n"
            message += f"   {created}\n\n"
    
    await query.edit_message_text(message, reply_markup=reply_markup)

async def process_gift_card_purchase(query, user_id: int, card_id: str):
    """Gift card satın alma işlemini gerçekleştir"""
    if card_id not in GIFT_CARDS:
        await query.edit_message_text("❌ Geçersiz gift card!")
        return
    
    card_info = GIFT_CARDS[card_id]
    balance = get_user_balance(user_id)
    
    if balance < card_info['amount']:
        keyboard = [
            [InlineKeyboardButton("💰 Bakiye Yükle", callback_data='how')],
            [InlineKeyboardButton("🔙 Geri", callback_data='buy')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"❌ Yetersiz Bakiye!\n\n"
            f"Gerekli: ${card_info['amount']:.2f}\n"
            f"Mevcut: ${balance:.2f}\n"
            f"Eksik: ${card_info['amount'] - balance:.2f}\n\n"
            f"Lütfen bakiye yükleyin.",
            reply_markup=reply_markup
        )
        return
    
    # Bakiyeden düş
    update_balance(
        user_id,
        card_info['amount'],
        'purchase',
        f"{card_info['name']} satın alındı"
    )
    
    # Gift card görselini gönder
    keyboard = [[InlineKeyboardButton("🏠 Ana Menü", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        # Gift card görseli gönder (use context manager for proper file handling)
        with open(card_info['image_path'], 'rb') as photo_file:
            await query.message.reply_photo(
                photo=photo_file,
                caption=(
                    f"✅ Satın Alma Başarılı!\n\n"
                    f"🎁 {card_info['name']}\n"
                    f"💰 Tutar: ${card_info['amount']:.2f}\n"
                    f"📊 Kalan Bakiye: ${get_user_balance(user_id):.2f}\n\n"
                    f"Gift card bilgileriniz yukarıdadır.\n"
                    f"İyi alışverişler!"
                ),
                reply_markup=reply_markup
            )
        await query.delete_message()
    except FileNotFoundError:
        # Eğer görsel yoksa sadece metin gönder
        await query.edit_message_text(
            f"✅ Satın Alma Başarılı!\n\n"
            f"🎁 {card_info['name']}\n"
            f"💰 Tutar: ${card_info['amount']:.2f}\n"
            f"📊 Kalan Bakiye: ${get_user_balance(user_id):.2f}\n\n"
            f"⚠️ Gift card görseli bulunamadı.\n"
            f"Lütfen destek ekibiyle iletişime geçin.\n\n"
            f"Kod: GIFTCARD-{card_id.upper()}",
            reply_markup=reply_markup
        )

async def show_main_menu(query):
    """Ana menüyü göster"""
    keyboard = [
        [
            InlineKeyboardButton("💰 Balance", callback_data='balance'),
            InlineKeyboardButton("🛒 Buy Gift Card", callback_data='buy')
        ],
        [
            InlineKeyboardButton("❓ How to Buy", callback_data='how'),
            InlineKeyboardButton("📊 Transaction History", callback_data='history')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        "🏠 Ana Menü\n\n"
        "Lütfen aşağıdaki seçeneklerden birini seçin:"
    )
    
    await query.edit_message_text(message, reply_markup=reply_markup)

def main():
    """Bot'u başlat"""
    # Veritabanını başlat
    init_db()
    
    # Bot uygulamasını oluştur
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handler'ları ekle
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Bot'u başlat
    logger.info("Bot başlatılıyor...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
