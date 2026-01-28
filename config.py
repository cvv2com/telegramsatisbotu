"""
Yapılandırma dosyası - Configuration file
"""
import os

# Telegram Bot Token - Bot Father'dan alınacak
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Admin kullanıcı ID'leri - Admin user IDs
ADMIN_IDS = [int(x) for x in os.environ.get('ADMIN_IDS', '').split(',') if x]

# Veritabanı dosyası - Database file
DATABASE_FILE = 'gift_cards.json'

# Para birimi - Currency
CURRENCY = '₺'  # TL simgesi / TL symbol
