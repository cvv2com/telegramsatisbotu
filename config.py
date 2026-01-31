import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token
# Get this from @BotFather on Telegram
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Admin User IDs (List of Telegram user IDs who can use admin commands)
# Get your user ID by messaging @userinfobot on Telegram
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "123456789,987654321")
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(',') if id.strip()]

# Cryptomus Payment Gateway Configuration
CRYPTOMUS_CONFIG = {
    "merchant_id": os.getenv("CRYPTOMUS_MERCHANT_ID", ""),
    "payment_api_key": os.getenv("CRYPTOMUS_PAYMENT_API_KEY", ""),
    "payout_api_key": os.getenv("CRYPTOMUS_PAYOUT_API_KEY", ""),
    "webhook_secret": os.getenv("CRYPTOMUS_WEBHOOK_SECRET", ""),
    "supported_currencies": ["BTC", "ETH", "USDT"],  # Bitcoin, Ethereum, USDT (TRC-20)
    "currency_networks": {
        "BTC": "BTC",
        "ETH": "ETH",
        "USDT": "TRON",  # TRC-20
    }
}

# MySQL Database Configuration
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "database": os.getenv("MYSQL_DATABASE", "telegram_sales_bot"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
}

# Stock Management
LOW_STOCK_THRESHOLD = int(os.getenv("LOW_STOCK_THRESHOLD", "5"))


# MC/Visa Gift Card System Configuration (Version 3.0)
GIFT_CARD_CONFIG = {
    "auto_generate": True,  # Auto-generate card numbers, expiration dates, and PINs
    "default_validity_months": 24,  # Default validity period in months
    "pin_length": 3,  # PIN length for MC/Visa cards (3 digits)
    
    # Minimum balance requirement
    "minimum_balance": 20.0,  # Minimum balance required to make purchases ($20)
    
    # Card pricing
    "numeric_card_price": 20.0,  # Price per numeric gift card ($20)
    "picture_card_price": 50.0,  # Price per picture gift card ($50)
    
    # Card types available
    "card_types": {
        "mc_numeric": {
            "name": "MC Gift Card (Numeric)",
            "description": "Mastercard numeric gift card with card number, expiration date, and PIN",
            "price": 20.0,
            "category": "MC Numeric"
        },
        "visa_numeric": {
            "name": "Visa Gift Card (Numeric)",
            "description": "Visa numeric gift card with card number, expiration date, and PIN",
            "price": 20.0,
            "category": "Visa Numeric"
        },
        "mc_picture": {
            "name": "MC Gift Card (Picture)",
            "description": "Mastercard picture gift card with front and back images",
            "price": 50.0,
            "category": "MC Picture"
        },
        "visa_picture": {
            "name": "Visa Gift Card (Picture)",
            "description": "Visa picture gift card with front and back images",
            "price": 50.0,
            "category": "Visa Picture"
        }
    }
}

# Gift Card Image Paths
# Images should be placed in the /giftcards/ directory
# Format: /giftcards/mc{ID}front.jpg, /giftcards/mc{ID}back.jpg
# Format: /giftcards/visa{ID}front.jpg, /giftcards/visa{ID}back.jpg
GIFTCARD_IMAGE_PATH = "/giftcards/"

# Payment System Configuration
PAYMENT_CONFIG = {
    "timeout_minutes": 30,  # Payment timeout in minutes
    "required_confirmations": {
        "btc": 3,
        "eth": 12,
        "usdt": 19,
        "ltc": 6
    },
    "check_interval_minutes": 5,  # Interval for checking timeouts
    "minimum_payment_usd": 20.0,  # Minimum payment amount in USD
    "maximum_payment_usd": 10000.0,  # Maximum payment amount in USD
    # Exchange rates (demo values - replace with real-time API in production)
    "exchange_rates": {
        "btc": 42500.0,
        "eth": 2200.0,
        "usdt": 1.0,
        "ltc": 65.0
    }
}

