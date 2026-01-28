# Telegram Gift Card Sales Bot

An automated Telegram bot for selling gift cards with cryptocurrency payments.

[Türkçe Dokümantasyon için README_TR.md dosyasına bakın](README_TR.md)

## Features

- 🎉 `/start` command with welcome message and main menu
- 💰 Balance checking (new users start with $0 balance)
- 💎 Cryptocurrency payment support (BTC, ETH, USDT, LTC)
- 🎁 Gift card purchases (Mastercard, Visa, Amazon, Steam, Google Play)
- 📊 Transaction history tracking
- 🔒 Secure data storage with SQLite database
- 🤖 Automatic gift card image delivery

## Quick Start

### 1. Requirements

- Python 3.8 or higher
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/cvv2com/telegramsatisbotu.git
cd telegramsatisbotu

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Edit `config.py`:

```python
# Add your bot token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Add your cryptocurrency wallet addresses
CRYPTO_WALLETS = {
    "btc": "your_btc_wallet_address",
    "eth": "your_eth_wallet_address",
    "usdt": "your_usdt_wallet_address",
    "ltc": "your_ltc_wallet_address",
}
```

### 4. Add Gift Card Images

Create gift card images in the `gift_cards` folder:
- `gift_cards/mastercard_50.jpg`
- `gift_cards/visa_30.jpg`
- etc.

### 5. Run the Bot

```bash
python bot.py
```

## Usage

### User Flow

1. **Start**: Send `/start` command to the bot
2. **Check Balance**: Click "Balance" button to view your balance
3. **Load Balance**:
   - Click "How to Buy"
   - Select a cryptocurrency (BTC, ETH, USDT, LTC)
   - Send payment to the displayed wallet address
   - Balance is automatically loaded after confirmation
4. **Purchase Gift Card**:
   - Click "Buy Gift Card"
   - Select desired gift card
   - Payment is automatically deducted from balance
   - Gift card image is sent to you

### Admin Operations

Use the admin utility script for manual operations:

```bash
# List all users
python admin.py users

# View user information
python admin.py user 123456789

# Add balance to user
python admin.py add 123456789 100.00

# View system statistics
python admin.py stats
```

## Project Structure

```
telegramsatisbotu/
├── bot.py              # Main bot application
├── config.py           # Configuration file
├── admin.py            # Admin utility script
├── requirements.txt    # Python dependencies
├── README.md           # English documentation
├── README_TR.md        # Turkish documentation
├── .gitignore         # Git ignore file
└── gift_cards/        # Gift card images directory
    └── README.md
```

## Database Schema

### Users Table
- `user_id`: Telegram user ID (PRIMARY KEY)
- `username`: Username
- `balance`: Current balance (USD)
- `created_at`: Registration date

### Transactions Table
- `id`: Transaction ID (AUTO INCREMENT)
- `user_id`: User ID
- `transaction_type`: Type (deposit/purchase)
- `amount`: Transaction amount
- `description`: Transaction description
- `created_at`: Transaction date

## Security Notes

⚠️ Important security considerations:
- Never commit `config.py` with real tokens/addresses to GitHub
- Keep your bot token private
- Regularly verify cryptocurrency payments manually
- Take regular database backups
- Consider implementing payment verification system

## Customization

### Adding New Gift Cards

Add to `GIFT_CARDS` in `config.py`:

```python
"new_card": {
    "name": "New Gift Card $75",
    "amount": 75.0,
    "image_path": "gift_cards/new_card_75.jpg",
    "description": "New $75 Gift Card"
}
```

### Adding New Cryptocurrencies

Add to `CRYPTO_WALLETS` in `config.py`:

```python
"doge": "your_dogecoin_wallet_address"
```

## Troubleshooting

**Bot not starting?**
- Check your bot token is correct
- Verify internet connection
- Check Python version (3.8+)

**Gift card images not sending?**
- Ensure `gift_cards` folder exists
- Check file names match `config.py`
- Verify file permissions

## License

Open source - free to use

## Support

For questions, please open an issue on GitHub.
