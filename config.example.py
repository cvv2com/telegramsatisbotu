# Example Configuration File
# Copy this to config.py and fill in your actual values

# Telegram Bot Token
# Get this from @BotFather on Telegram
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Admin User IDs (List of Telegram user IDs who can use admin commands)
# Get your user ID by messaging @userinfobot on Telegram
ADMIN_IDS = [123456789]  # Replace with your actual admin user IDs

# Cryptocurrency Wallet Addresses
# Replace with your actual wallet addresses
CRYPTO_WALLETS = {
    "btc": "YOUR_BTC_ADDRESS",
    "eth": "YOUR_ETH_ADDRESS",
    "usdt": "YOUR_USDT_ADDRESS",
    "ltc": "YOUR_LTC_ADDRESS",
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
