# Example Environment File
# Copy this to config.py and fill in your actual values

# Telegram Bot Token
# Get this from @BotFather on Telegram
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual bot token

# Admin User IDs (List of Telegram user IDs who can use admin commands)
# Get your user ID by messaging @userinfobot on Telegram
ADMIN_IDS = [123456789, 987654321]  # Replace with your actual admin user IDs

# Cryptocurrency Wallet Addresses
# Replace with your actual wallet addresses
CRYPTO_WALLETS = {
    "btc": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "eth": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "usdt": "TXj9KpLuTdU8kqvU9ZnQxQHDJVPH2NFq8K",
    "ltc": "LUWPbpM43E2p7ZSh8cyTBEkvpHmr3cB8Ez",
}

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
}

