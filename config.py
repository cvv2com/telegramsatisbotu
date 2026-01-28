# -*- coding: utf-8 -*-
"""
Bot Konfigürasyon Dosyası
Telegram bot token ve kripto cüzdan adreslerini buradan ayarlayın
"""

# Telegram Bot Token
# @BotFather'dan alınan token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Kripto Para Cüzdan Adresleri
# Ödeme alınacak cüzdan adreslerini buraya ekleyin
CRYPTO_WALLETS = {
    "btc": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # Örnek BTC adresi
    "eth": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",  # Örnek ETH adresi
    "usdt": "TXj9KpLuTdU8kqvU9ZnQxQHDJVPH2NFq8K",  # Örnek USDT (TRC20) adresi
    "ltc": "LUWPbpM43E2p7ZSh8cyTBEkvpHmr3cB8Ez",  # Örnek LTC adresi
}

# Gift Card Seçenekleri
# Satılacak gift card'ları ve fiyatlarını tanımlayın
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
    "mc_100": {
        "name": "Mastercard Gift Card $100",
        "amount": 100.0,
        "image_path": "gift_cards/mastercard_100.jpg",
        "description": "Mastercard $100 Gift Card"
    },
    "visa_50": {
        "name": "Visa Gift Card $50",
        "amount": 50.0,
        "image_path": "gift_cards/visa_50.jpg",
        "description": "Visa $50 Gift Card"
    },
    "amazon_25": {
        "name": "Amazon Gift Card $25",
        "amount": 25.0,
        "image_path": "gift_cards/amazon_25.jpg",
        "description": "Amazon $25 Gift Card"
    },
    "amazon_50": {
        "name": "Amazon Gift Card $50",
        "amount": 50.0,
        "image_path": "gift_cards/amazon_50.jpg",
        "description": "Amazon $50 Gift Card"
    },
    "steam_20": {
        "name": "Steam Gift Card $20",
        "amount": 20.0,
        "image_path": "gift_cards/steam_20.jpg",
        "description": "Steam $20 Gift Card"
    },
    "google_play_25": {
        "name": "Google Play Gift Card $25",
        "amount": 25.0,
        "image_path": "gift_cards/google_play_25.jpg",
        "description": "Google Play $25 Gift Card"
    },
}
