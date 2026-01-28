#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Gift Card Sales Bot
Otomatik gift card satış botu
"""

import logging
import sys
import os
import csv
import json
import io
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import sqlite3

# Try to import config, provide helpful error if missing
try:
    from config import BOT_TOKEN, CRYPTO_WALLETS, GIFT_CARDS
    # Try to import ADMIN_IDS, default to empty list if not found
    try:
        from config import ADMIN_IDS
    except ImportError:
        ADMIN_IDS = []
        logger.warning("ADMIN_IDS not found in config.py. Admin features will be disabled.")
except ImportError as e:
    print("\n" + "="*60)
    print("ERROR: config.py file not found!")
    print("="*60)
    print("\nThe bot requires a config.py file with your bot token and settings.")
    print("\nTo fix this:")
    if os.name == 'nt':  # Windows
        print("  1. Run: copy config.example.py config.py")
    else:  # Unix/Linux/Mac
        print("  1. Run: cp config.example.py config.py")
    print("  2. Edit config.py and add your bot token from @BotFather")
    print("  3. Add your cryptocurrency wallet addresses")
    print("\nFor more help, see README.md or QUICKSTART.md")
    print("="*60 + "\n")
    sys.exit(1)
except Exception as e:
    print("\n" + "="*60)
    print("ERROR loading config.py!")
    print("="*60)
    print(f"\nError details: {e}")
    print("\nPlease check your config.py file for syntax errors.")
    print("You can use config.example.py as a reference.")
    print("="*60 + "\n")
    sys.exit(1)

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
    
    # Gift card satın alımları tablosu
    cursor.execute('''
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
        )
    ''')
    
    # Products tablosu (bulk import için)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            code TEXT UNIQUE,
            stock INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Coupons tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            discount_type TEXT NOT NULL,
            discount_value REAL NOT NULL,
            min_purchase REAL DEFAULT 0.0,
            max_uses INTEGER DEFAULT -1,
            used_count INTEGER DEFAULT 0,
            expiry_date TIMESTAMP,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Coupon usage tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coupon_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coupon_id INTEGER,
            user_id INTEGER,
            discount_amount REAL,
            used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (coupon_id) REFERENCES coupons (id),
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
    
    # Gift card bilgilerini veritabanına kaydet
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO gift_card_purchases 
        (user_id, card_id, card_name, card_number, exp_date, pin, amount)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        card_id,
        card_info['name'],
        card_info.get('card_number', 'N/A'),
        card_info.get('exp_date', 'N/A'),
        card_info.get('pin', 'N/A'),
        card_info['amount']
    ))
    conn.commit()
    conn.close()
    
    # Gift card bilgilerini hazırla
    keyboard = [[InlineKeyboardButton("🏠 Ana Menü", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Caption mesajı oluştur
    caption = (
        f"✅ Satın Alma Başarılı!\n\n"
        f"🎁 {card_info['name']}\n"
        f"💰 Tutar: ${card_info['amount']:.2f}\n"
    )
    
    # Kart bilgilerini ekle (varsa)
    if card_info.get('card_number'):
        caption += f"\n💳 Kart Numarası: `{card_info['card_number']}`\n"
    if card_info.get('exp_date'):
        caption += f"📅 Son Kullanma Tarihi: {card_info['exp_date']}\n"
    if card_info.get('pin'):
        caption += f"🔐 PIN: `{card_info['pin']}`\n"
    
    caption += f"\n📊 Kalan Bakiye: ${get_user_balance(user_id):.2f}\n"
    caption += f"\nİyi alışverişler!"
    
    # Önce front image'i gönder
    has_images = False
    
    try:
        # Ön yüz görseli (image_front veya image_path)
        front_path = card_info.get('image_front') or card_info.get('image_path')
        
        if front_path:
            try:
                with open(front_path, 'rb') as photo_file:
                    await query.message.reply_photo(
                        photo=photo_file,
                        caption=caption,
                        parse_mode='Markdown',
                        reply_markup=reply_markup
                    )
                has_images = True
            except FileNotFoundError:
                logger.warning(f"Front image not found: {front_path}")
        
        # Arka yüz görseli (varsa)
        back_path = card_info.get('image_back')
        if back_path:
            try:
                with open(back_path, 'rb') as photo_file:
                    await query.message.reply_photo(
                        photo=photo_file,
                        caption="🔙 Gift Card Arka Yüz",
                        reply_markup=reply_markup
                    )
            except FileNotFoundError:
                logger.warning(f"Back image not found: {back_path}")
        
        await query.delete_message()
        
    except Exception as e:
        logger.error(f"Error sending gift card images: {e}")
        has_images = False
    
    # Eğer hiç görsel gönderilemedi ise sadece metin gönder
    if not has_images:
        await query.edit_message_text(
            caption + f"\n\n⚠️ Gift card görselleri bulunamadı.\n"
            f"Lütfen destek ekibiyle iletişime geçin.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
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

# ============ Admin Functions ============

def is_admin(user_id: int) -> bool:
    """Check if user is an admin"""
    return user_id in ADMIN_IDS

async def import_products_csv(file_content: str) -> tuple:
    """Import products from CSV content"""
    try:
        reader = csv.DictReader(io.StringIO(file_content))
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        
        imported = 0
        errors = []
        
        for row in reader:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO products (name, description, price, category, code, stock)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('name', ''),
                    row.get('description', ''),
                    float(row.get('price', 0)),
                    row.get('category', ''),
                    row.get('code', ''),
                    int(row.get('stock', 0))
                ))
                imported += 1
            except Exception as e:
                errors.append(f"Row error: {str(e)}")
        
        conn.commit()
        conn.close()
        return (imported, errors)
    except Exception as e:
        return (0, [f"CSV parsing error: {str(e)}"])

async def import_products_json(file_content: str) -> tuple:
    """Import products from JSON content"""
    try:
        products = json.loads(file_content)
        if not isinstance(products, list):
            return (0, ["JSON must be an array of products"])
        
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        
        imported = 0
        errors = []
        
        for product in products:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO products (name, description, price, category, code, stock)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    product.get('name', ''),
                    product.get('description', ''),
                    float(product.get('price', 0)),
                    product.get('category', ''),
                    product.get('code', ''),
                    int(product.get('stock', 0))
                ))
                imported += 1
            except Exception as e:
                errors.append(f"Product error: {str(e)}")
        
        conn.commit()
        conn.close()
        return (imported, errors)
    except json.JSONDecodeError as e:
        return (0, [f"JSON parsing error: {str(e)}"])
    except Exception as e:
        return (0, [f"Import error: {str(e)}"])

async def import_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /import command - wait for file upload"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Bu komutu kullanma yetkiniz yok!")
        return
    
    message = (
        "📤 **Toplu Ürün İçe Aktarma**\n\n"
        "CSV veya JSON dosyası gönderin:\n\n"
        "**CSV Format:**\n"
        "```\n"
        "name,description,price,category,code,stock\n"
        "Netflix 10$,1 Month,10,Entertainment,NF-123,5\n"
        "Steam 20$,Steam Wallet,20,Gaming,ST-456,10\n"
        "```\n\n"
        "**JSON Format:**\n"
        "```json\n"
        "[\n"
        "  {\n"
        '    "name": "Netflix 10$",\n'
        '    "description": "1 Month",\n'
        '    "price": 10,\n'
        '    "category": "Entertainment",\n'
        '    "code": "NF-123",\n'
        '    "stock": 5\n'
        "  }\n"
        "]\n"
        "```"
    )
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file uploads for product import"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        return
    
    document = update.message.document
    
    if not document:
        return
    
    # Check file type
    file_name = document.file_name.lower()
    
    if not (file_name.endswith('.csv') or file_name.endswith('.json')):
        await update.message.reply_text("❌ Sadece CSV veya JSON dosyaları desteklenir!")
        return
    
    # Download file
    file = await context.bot.get_file(document.file_id)
    file_content = await file.download_as_bytearray()
    file_text = file_content.decode('utf-8')
    
    # Import based on file type
    if file_name.endswith('.csv'):
        imported, errors = await import_products_csv(file_text)
    else:
        imported, errors = await import_products_json(file_text)
    
    # Send result
    if imported > 0:
        message = f"✅ **İçe Aktarma Başarılı!**\n\n"
        message += f"📦 {imported} ürün içe aktarıldı.\n"
        if errors:
            message += f"\n⚠️ {len(errors)} hata:\n"
            message += "\n".join(errors[:5])  # Show first 5 errors
    else:
        message = f"❌ **İçe Aktarma Başarısız!**\n\n"
        if errors:
            message += "Hatalar:\n"
            message += "\n".join(errors[:10])
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def addcoupon_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /addcoupon command"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Bu komutu kullanma yetkiniz yok!")
        return
    
    # Parse arguments: /addcoupon CODE TYPE VALUE [MIN_PURCHASE] [MAX_USES] [EXPIRY_DAYS]
    if len(context.args) < 3:
        message = (
            "📋 **Kupon Oluşturma**\n\n"
            "**Komut formatı:**\n"
            "`/addcoupon <code> <type> <value> [min_purchase] [max_uses] [expiry_days]`\n\n"
            "**Parametreler:**\n"
            "• `code`: Kupon kodu (örn: SUMMER2024)\n"
            "• `type`: İndirim tipi (percent veya fixed)\n"
            "• `value`: İndirim değeri (örn: 20 veya 10.50)\n"
            "• `min_purchase`: Minimum alış tutarı (opsiyonel, varsayılan: 0)\n"
            "• `max_uses`: Maksimum kullanım sayısı (opsiyonel, varsayılan: sınırsız)\n"
            "• `expiry_days`: Geçerlilik süresi (gün) (opsiyonel, varsayılan: 30)\n\n"
            "**Örnekler:**\n"
            "`/addcoupon WELCOME20 percent 20 10 100 30`\n"
            "→ %20 indirim, min 10$, max 100 kullanım, 30 gün\n\n"
            "`/addcoupon SAVE10 fixed 10 50 -1 60`\n"
            "→ 10$ indirim, min 50$, sınırsız kullanım, 60 gün"
        )
        await update.message.reply_text(message, parse_mode='Markdown')
        return
    
    try:
        code = context.args[0].upper()
        discount_type = context.args[1].lower()
        discount_value = float(context.args[2])
        min_purchase = float(context.args[3]) if len(context.args) > 3 else 0.0
        max_uses = int(context.args[4]) if len(context.args) > 4 else -1
        expiry_days = int(context.args[5]) if len(context.args) > 5 else 30
        
        if discount_type not in ['percent', 'fixed']:
            await update.message.reply_text("❌ İndirim tipi 'percent' veya 'fixed' olmalıdır!")
            return
        
        if discount_value <= 0:
            await update.message.reply_text("❌ İndirim değeri 0'dan büyük olmalıdır!")
            return
        
        if discount_type == 'percent' and discount_value > 100:
            await update.message.reply_text("❌ Yüzde indirimi 100'den büyük olamaz!")
            return
        
        expiry_date = datetime.now() + timedelta(days=expiry_days)
        
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO coupons (code, discount_type, discount_value, min_purchase, max_uses, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (code, discount_type, discount_value, min_purchase, max_uses, expiry_date))
        
        conn.commit()
        conn.close()
        
        message = (
            "✅ **Kupon Oluşturuldu!**\n\n"
            f"🎟️ **Kod:** `{code}`\n"
            f"💰 **İndirim:** {discount_value}{'%' if discount_type == 'percent' else '$'}\n"
            f"🛒 **Min. Alış:** ${min_purchase:.2f}\n"
            f"🔢 **Max. Kullanım:** {'Sınırsız' if max_uses == -1 else max_uses}\n"
            f"📅 **Son Kullanma:** {expiry_date.strftime('%Y-%m-%d')}\n"
        )
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    except ValueError:
        await update.message.reply_text("❌ Geçersiz değerler! Lütfen doğru format kullanın.")
    except sqlite3.IntegrityError:
        await update.message.reply_text(f"❌ '{code}' kodu zaten mevcut!")
    except Exception as e:
        await update.message.reply_text(f"❌ Hata: {str(e)}")

def main():
    """Bot'u başlat"""
    # Veritabanını başlat
    init_db()
    
    # Bot uygulamasını oluştur
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handler'ları ekle
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("import", import_command))
    application.add_handler(CommandHandler("addcoupon", addcoupon_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    # Bot'u başlat
    logger.info("Bot başlatılıyor...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
