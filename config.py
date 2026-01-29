"""
Configuration file
"""
import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE').strip()

# Admin user IDs
try:
    admin_ids_str = os.environ.get('ADMIN_IDS', '')
    ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(',') if x.strip()]

    if not ADMIN_IDS:
        print("Warning: No ADMIN_IDS found! (Check your .env file)")
        
except ValueError as e:
    print(f"Error: Invalid ADMIN_IDS format.")
    sys.exit(1)

# Database file
DATABASE_FILE = 'gift_cards.json'

# Currency Symbol
CURRENCY = '$'  # Changed to Dollar
