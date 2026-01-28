"""
Yapılandırma dosyası - Configuration file
"""
import os
import sys

# Telegram Bot Token - Bot Father'dan alınacak
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Admin kullanıcı ID'leri - Admin user IDs
try:
    ADMIN_IDS = [int(x) for x in os.environ.get('ADMIN_IDS', '').split(',') if x.strip()]
except ValueError as e:
    print(f"Error: Invalid ADMIN_IDS format. Please provide comma-separated numeric IDs.")
    print(f"Example: ADMIN_IDS=123456789,987654321")
    sys.exit(1)

# Veritabanı dosyası - Database file
DATABASE_FILE = 'gift_cards.json'

# Para birimi - Currency
CURRENCY = '₺'  # TL simgesi / TL symbol
