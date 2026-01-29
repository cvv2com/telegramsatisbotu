# Example Environment File
# Copy this to config.py and fill in your actual values

# Telegram Bot Token
# Get this from @BotFather on Telegram
BOT_TOKEN = "8547124011:AAHZrClnI4yUM4epIBZi61MRTrrj5_LlyRA"

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

# Gift Card Generation Configuration
GIFT_CARD_CONFIG = {
    "auto_generate": True,  # Auto-generate card numbers, expiration dates, and PINs
    "default_card_type": "visa",  # Default card type: visa, mastercard, amex, discover
    "default_validity_months": 24,  # Default validity period in months
    "default_pin_length": 4,  # Default PIN length (3-4 digits recommended)
    "code_prefix": "GC",  # Prefix for auto-generated codes
}

# Gift Card Configuration
# Add or remove gift cards as needed
# Each gift card should have:
#   - name: Display name
#   - amount: Price in USD
#   - card_number: 16-digit card number (auto-generated if omitted)
#   - exp_date: Expiration date MM/YY format (auto-generated if omitted)
#   - pin: PIN code (auto-generated if omitted)
#   - image_front: Path to front image
#   - image_back: Path to back image (optional)
#   - description: Brief description
#
# Legacy format (still supported):
#   - image_path: Single image path (will be used as front image)
GIFT_CARDS = {
    "mc_50": {
        "name": "Mastercard Gift Card $50",
        "amount": 50.0,
        "card_number": "5543554475829811",
        "exp_date": "02/27",
        "pin": "097",
        "image_front": "gift_cards/mastercard_50_front.jpg",
        "image_back": "gift_cards/mastercard_50_back.jpg",
        "description": "Mastercard $50 Gift Card"
    },
    "visa_30": {
        "name": "Visa Gift Card $30",
        "amount": 30.0,
        "card_number": "4532123456789012",
        "exp_date": "12/28",
        "pin": "234",
        "image_front": "gift_cards/visa_30_front.jpg",
        "image_back": "gift_cards/visa_30_back.jpg",
        "description": "Visa $30 Gift Card"
    },
    # Add more gift cards here
}
