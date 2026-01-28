# Deployment Guide - Telegram Gift Card Sales Bot

This guide will help you deploy and run the Telegram gift card sales bot.

## Pre-requisites

- Python 3.8 or higher
- A Telegram account
- Cryptocurrency wallets (BTC, ETH, USDT, LTC)
- Gift card images

## Step-by-Step Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/cvv2com/telegramsatisbotu.git
cd telegramsatisbotu
```

### 2. Create Your Bot on Telegram

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Save the bot token (it looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Configure the Bot

Create your configuration file:

```bash
cp config.example.py config.py
nano config.py  # or use your preferred editor
```

Update the following values:

```python
# Add your bot token
BOT_TOKEN = "YOUR_BOT_TOKEN_FROM_BOTFATHER"

# Add your cryptocurrency wallet addresses
CRYPTO_WALLETS = {
    "btc": "your_actual_btc_address",
    "eth": "your_actual_eth_address",
    "usdt": "your_actual_usdt_trc20_address",
    "ltc": "your_actual_ltc_address",
}
```

**Important:** Keep `config.py` secure and never commit it to git!

### 4. Add Gift Card Images

Place your gift card images in the `gift_cards/` directory:

```bash
# Example structure:
gift_cards/
├── mastercard_50.jpg
├── mastercard_100.jpg
├── visa_30.jpg
├── visa_50.jpg
├── amazon_25.jpg
├── amazon_50.jpg
├── steam_20.jpg
└── google_play_25.jpg
```

**Image Requirements:**
- Format: JPG or PNG
- Recommended size: 800x500 pixels
- Maximum size: 5MB
- Make sure filenames match those in `config.py`

### 5. Install Dependencies

Run the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

Or manually install:

```bash
pip3 install -r requirements.txt
```

### 6. Verify Configuration

Before starting the bot, verify your configuration:

```bash
python3 verify.py
```

This will check:
- ✅ Configuration file exists
- ✅ Bot token is set
- ✅ Cryptocurrency wallets are configured
- ✅ Gift cards are configured
- ✅ Gift card images exist

### 7. Start the Bot

```bash
python3 bot.py
```

You should see:
```
Bot başlatılıyor...
```

### 8. Test the Bot

1. Open Telegram
2. Search for your bot by username
3. Send `/start` command
4. You should see the welcome message with menu buttons

## Running the Bot in Production

### Option 1: Screen (Simple)

```bash
# Start a new screen session
screen -S telegram-bot

# Run the bot
python3 bot.py

# Detach from screen: Press Ctrl+A then D
# To reattach: screen -r telegram-bot
```

### Option 2: Systemd Service (Recommended)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/telegram-gift-bot.service
```

Add the following content:

```ini
[Unit]
Description=Telegram Gift Card Sales Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/telegramsatisbotu
ExecStart=/usr/bin/python3 /path/to/telegramsatisbotu/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-gift-bot
sudo systemctl start telegram-gift-bot
sudo systemctl status telegram-gift-bot
```

View logs:
```bash
sudo journalctl -u telegram-gift-bot -f
```

### Option 3: Docker (Advanced)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]
```

Build and run:

```bash
docker build -t telegram-gift-bot .
docker run -d --name gift-bot --restart unless-stopped telegram-gift-bot
```

## Admin Operations

### View All Users

```bash
python3 admin.py users
```

### View User Details

```bash
python3 admin.py user 123456789
```

### Add Balance to User

When a user sends cryptocurrency payment:

1. Verify the payment on blockchain
2. Add balance to the user:

```bash
python3 admin.py add 123456789 50.00
```

This will:
- Add $50 to user's balance
- Create a transaction record
- User can now purchase gift cards

### View System Statistics

```bash
python3 admin.py stats
```

Shows:
- Total users
- Total balance in system
- Total transactions
- Total sales
- Net income

## Database Backup

Regular backups are essential:

```bash
# Backup database
cp bot_database.db backups/bot_database_$(date +%Y%m%d).db

# Automated daily backup (add to crontab)
0 0 * * * cp /path/to/bot_database.db /path/to/backups/bot_database_$(date +\%Y\%m\%d).db
```

## Security Best Practices

1. **Never commit sensitive data:**
   - `config.py` is in `.gitignore`
   - Never share bot token publicly
   
2. **Verify payments manually:**
   - Always check blockchain before adding balance
   - Use a transaction tracking spreadsheet
   
3. **Regular backups:**
   - Backup database daily
   - Store backups securely
   
4. **Monitor the bot:**
   - Check logs regularly
   - Monitor for unusual activity
   
5. **Secure the server:**
   - Use firewall (UFW)
   - Keep system updated
   - Use SSH keys instead of passwords

## Troubleshooting

### Bot doesn't start

**Error: ModuleNotFoundError: No module named 'telegram'**
```bash
pip3 install python-telegram-bot==21.9
```

**Error: telegram.error.InvalidToken**
- Check your bot token in `config.py`
- Make sure there are no extra spaces

### Bot starts but doesn't respond

1. Check if bot is running: `ps aux | grep bot.py`
2. Check logs for errors
3. Verify bot token with @BotFather
4. Make sure your server has internet access

### Gift card images not sending

1. Check file permissions: `chmod 644 gift_cards/*.jpg`
2. Verify filenames match `config.py`
3. Check image file size (< 5MB)

### Database errors

```bash
# Check database integrity
sqlite3 bot_database.db "PRAGMA integrity_check;"

# If corrupted, restore from backup
cp backups/bot_database_YYYYMMDD.db bot_database.db
```

## Monitoring

### Check if bot is running

```bash
ps aux | grep bot.py
# or with systemd
sudo systemctl status telegram-gift-bot
```

### View recent logs

```bash
# If running in screen
screen -r telegram-bot

# If using systemd
sudo journalctl -u telegram-gift-bot -n 100
```

### Monitor database size

```bash
du -h bot_database.db
```

## Scaling

For high volume:

1. **Use PostgreSQL instead of SQLite**
2. **Implement payment verification service**
3. **Add rate limiting**
4. **Use Redis for caching**
5. **Deploy multiple instances with load balancer**

## Support

For issues or questions:
- Check the README files
- Review this deployment guide
- Open an issue on GitHub
- Check bot logs for errors

## Maintenance Tasks

### Daily
- [ ] Check bot is running
- [ ] Review new user signups
- [ ] Process pending payments

### Weekly
- [ ] Backup database
- [ ] Review transaction logs
- [ ] Check system resources

### Monthly
- [ ] Update dependencies: `pip install -U -r requirements.txt`
- [ ] Review and archive old backups
- [ ] Check for bot updates

## Legal Considerations

⚠️ **Important:** Ensure compliance with:
- Local cryptocurrency regulations
- Gift card resale laws
- Tax reporting requirements
- Data privacy regulations (GDPR, etc.)

Consult with legal counsel before operating in production.
