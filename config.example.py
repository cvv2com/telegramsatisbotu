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
GIFT_CARDS = {
    "mc_50": {
        "name": "Mastercard Gift Card $50",
        "amount": 50.0,
        "image_path": "gift_cards/mastercard_50.jpg",
        "description": "Mastercard $50 Gift Card"
    },
    "visa_30": {
        "name": "Visa Gift Card $30",
        "amount": 30.0,
        "image_path": "gift_cards/visa_30.jpg",
        "description": "Visa $30 Gift Card"
    },
    # Add more gift cards here
}
