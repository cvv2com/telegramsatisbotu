# Telegram Gift Card Sales Bot

An automated Telegram bot for selling gift cards with cryptocurrency payments.

[Türkçe Dokümantasyon için README_TR.md dosyasına bakın](README_TR.md)

**🐧 Ubuntu/cPanel-WHM Users:** See [UBUNTU_CPANEL_INSTALL.md](UBUNTU_CPANEL_INSTALL.md) for Ubuntu and cPanel/WHM specific installation instructions (Turkish).

**🪟 Windows Users:** See [WINDOWS.md](WINDOWS.md) for Windows-specific setup instructions.

## Features

### User Features
- 🎉 `/start` command with welcome message and main menu
- 💰 Balance checking (new users start with $0 balance)
- 💎 Cryptocurrency payment support (BTC, ETH, USDT, LTC)
- 🎁 Gift card purchases (Mastercard, Visa, Amazon, Steam, Google Play)
- 🎟️ Coupon code support for discounts
- 📊 Transaction history tracking
- 🔒 Secure data storage with SQLite database
- 🤖 Automatic gift card image delivery

### Admin Features
- 📤 **Bulk Product Import** - Import hundreds of products at once via CSV or JSON files
- 🎟️ **Coupon Management** - Create discount coupons with `/addcoupon` command
- 👥 User management (via admin.py)
- 💰 Manual balance loading
- 📈 Sales statistics

### Platform Support
- 🪟 Windows support with batch files
- 🐧 Ubuntu/cPanel-WHM support
- 🐧 Generic Linux/Mac support

## Quick Start

### Platform Selection

Choose the appropriate installation guide for your operating system:

- **🐧 Ubuntu + cPanel/WHM Server**: [UBUNTU_CPANEL_INSTALL.md](UBUNTU_CPANEL_INSTALL.md) - Detailed Ubuntu and cPanel/WHM setup guide (Turkish)
- **🪟 Windows**: [WINDOWS.md](WINDOWS.md) - Windows-specific installation guide
- **🐧 Generic Linux/Mac**: Follow the general instructions below
- **🚀 Advanced Setup**: [DEPLOYMENT.md](DEPLOYMENT.md) - Docker, systemd, and other options

### 1. Requirements

- Python 3.8 or higher
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))

### 2. Installation

**For Windows Users:**
```cmd
# Run the setup script
setup.bat
```
Then edit `config.py` with your bot token and run `start.bat`. See [WINDOWS.md](WINDOWS.md) for details.

**For Linux/Mac Users:**
```bash
# Clone the repository
git clone https://github.com/cvv2com/telegramsatisbotu.git
cd telegramsatisbotu

# Run setup script
chmod +x setup.sh
./setup.sh

# Or manually:
pip install -r requirements.txt
cp config.example.py config.py
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

#### Setting Up Admin Access

Add admin user IDs in `config.py`:

```python
# Admin User IDs (Telegram user IDs)
# Get your ID by messaging @userinfobot on Telegram
ADMIN_IDS = [123456789, 987654321]
```

#### Bulk Product Import

Import hundreds of products at once using CSV or JSON files.

**1. Start with `/import` command:**
```
/import
```

**2. Send a CSV or JSON file:**

**CSV Format:**
```csv
name,description,price,category,code,stock
Netflix 10$,1 Month,10,Entertainment,NF-123,5
Steam 20$,Steam Wallet,20,Gaming,ST-456,10
Amazon 50$,Gift Card,50,Shopping,AMZ-789,3
```

**JSON Format:**
```json
[
  {
    "name": "Netflix 10$",
    "description": "1 Month",
    "price": 10,
    "category": "Entertainment",
    "code": "NF-123",
    "stock": 5
  },
  {
    "name": "Steam 20$",
    "description": "Steam Wallet",
    "price": 20,
    "category": "Gaming",
    "code": "ST-456",
    "stock": 10
  }
]
```

#### Creating Coupons

Use `/addcoupon` command to create discount coupons.

**Command Format:**
```
/addcoupon <code> <type> <value> [min_purchase] [max_uses] [expiry_days]
```

**Parameters:**
- `code`: Coupon code (e.g., SUMMER2024)
- `type`: Discount type (`percent` or `fixed`)
- `value`: Discount value (percentage or fixed amount)
- `min_purchase`: Minimum purchase amount (optional, default: 0)
- `max_uses`: Maximum number of uses (optional, default: unlimited)
- `expiry_days`: Validity period in days (optional, default: 30)

**Examples:**

```bash
# 20% discount, min $10, max 100 uses, valid for 30 days
/addcoupon WELCOME20 percent 20 10 100 30

# $10 fixed discount, min $50, unlimited uses, valid for 60 days
/addcoupon SAVE10 fixed 10 50 -1 60

# 15% discount, no minimum, 50 uses available
/addcoupon SPECIAL15 percent 15 0 50
```

#### Manual Balance Management

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
