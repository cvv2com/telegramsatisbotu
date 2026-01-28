# Example Environment File
# Copy this to config.py and fill in your actual values

# Telegram Bot Token
# Get this from @BotFather on Telegram
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"

# Cryptocurrency Wallet Addresses
# Replace with your actual wallet addresses
CRYPTO_WALLETS = {
    "btc": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "eth": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "usdt": "TXj9KpLuTdU8kqvU9ZnQxQHDJVPH2NFq8K",
    "ltc": "LUWPbpM43E2p7ZSh8cyTBEkvpHmr3cB8Ez",
}

# Gift Card Configuration
# Add or remove gift cards as needed
# Each gift card can have:
#   - name: Display name
#   - amount: Price in USD
#   - card_number: 16-digit card number (optional)
#   - exp_date: Expiration date MM/YY format (optional)
#   - pin: PIN code (optional)
#   - image_front: Path to front image (optional, falls back to image_path)
#   - image_back: Path to back image (optional)
#   - image_path: Single image path (for backward compatibility)
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
    # Example with single image (backward compatible)
    "amazon_25": {
        "name": "Amazon Gift Card $25",
        "amount": 25.0,
        "card_number": "AMZN-1234-5678-9012",
        "pin": "XYZABC",
        "image_path": "gift_cards/amazon_25.jpg",
        "description": "Amazon $25 Gift Card"
    },
    # Add more gift cards here
}
