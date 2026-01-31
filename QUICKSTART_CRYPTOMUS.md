# Cryptomus Integration - Quick Start Guide

## TL;DR - What Changed?

✅ **Added:** Cryptomus cryptocurrency payment gateway (Bitcoin, Ethereum, USDT)  
❌ **Removed:** PayPal integration  
🔄 **Changed:** Payment flow now fully automated via webhooks  

## Getting Started (5 Minutes)

### 1. Sign Up for Cryptomus

1. Visit: https://cryptomus.com
2. Create merchant account
3. Complete KYB verification
4. Get API credentials from dashboard

### 2. Set Up MySQL

```bash
# Install MySQL
sudo apt-get install mysql-server  # Ubuntu/Debian
brew install mysql                  # macOS

# Create database
mysql -u root -p
CREATE DATABASE telegram_sales_bot;
EXIT;

# Initialize tables
python mysql_payment_db.py
```

### 3. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env file
nano .env
```

**Required Settings:**
```bash
# Get from Cryptomus dashboard
CRYPTOMUS_MERCHANT_ID=your_uuid_here
CRYPTOMUS_PAYMENT_API_KEY=your_key_here

# Your webhook URL (see step 4)
WEBHOOK_URL=https://your-domain.com/webhook/cryptomus

# MySQL settings
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=telegram_sales_bot
```

### 4. Set Up Webhook (Choose One)

**Option A: Development (ngrok)**
```bash
# Install ngrok
brew install ngrok  # or download from ngrok.com

# Start tunnel
ngrok http 5000

# Copy HTTPS URL to .env
WEBHOOK_URL=https://abc123.ngrok.io/webhook/cryptomus
```

**Option B: Production**
```bash
# Use your domain
WEBHOOK_URL=https://yourdomain.com/webhook/cryptomus

# Configure nginx reverse proxy (see docs)
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Start Services

**Terminal 1 - Webhook:**
```bash
python webhook_handler.py
```

**Terminal 2 - Bot:**
```bash
python telegram_bot.py
```

## How to Use

### For Users

1. Open bot: `/start`
2. Click: **💰 Create Payment**
3. Select: BTC, ETH, or USDT
4. Enter: Amount ($20 - $10,000)
5. Click: Payment link
6. Pay: Using your crypto wallet
7. Done: Automatic notification when confirmed!

### For Admins

```bash
/admin_payments        # View all payments
/admin_payments 2      # View page 2
/payment_stats         # View statistics
```

## Common Issues

### "Payment creation failed"
- Check Cryptomus API credentials in .env
- Verify account is KYB verified
- Check internet connection

### "Webhook not working"
- Verify WEBHOOK_URL is publicly accessible
- Test: `curl https://your-url/webhook/cryptomus`
- Check Flask server is running
- Review webhook_handler.py logs

### "Database connection error"
- Verify MySQL is running: `sudo systemctl status mysql`
- Check credentials in .env
- Ensure database exists
- Check firewall settings

## File Structure

```
Key Files:
├── webhook_handler.py       ← Start this first!
├── telegram_bot.py          ← Start this second!
├── .env                     ← Configure your secrets here
├── cryptomus_payment.py     ← API client (no changes needed)
├── mysql_payment_db.py      ← Database (auto-creates tables)
└── CRYPTOMUS_INTEGRATION.md ← Full documentation

Configuration:
├── .env                     ← Your secrets (never commit!)
├── .env.example             ← Template

Documentation:
├── README.md                         ← Overview
├── CRYPTOMUS_INTEGRATION.md          ← Complete guide
└── IMPLEMENTATION_SUMMARY_CRYPTOMUS.md ← Technical details
```

## Testing

### Test Payment Creation

```bash
python cryptomus_service.py
```

Expected output:
```
✅ Payment created successfully!
   Order ID: ORDER_123456789_1234567890
   Payment URL: https://pay.cryptomus.com/...
```

### Test Database

```bash
python mysql_payment_db.py
```

Expected output:
```
✅ Connection pool created
✅ Database tables created
```

### Test Webhook

```bash
# While webhook_handler.py is running
curl http://localhost:5000/health
```

Expected output:
```json
{
  "status": "ok",
  "service": "cryptomus-webhook",
  "timestamp": "..."
}
```

## Important Notes

⚠️ **Security:**
- Never commit `.env` file to Git
- Use strong MySQL passwords
- Only run webhook on HTTPS in production
- Keep API keys secret

💡 **Tips:**
- Use ngrok for development testing
- Check logs if something fails
- Payment timeout is 60 minutes
- Minimum payment is $20

📝 **For Production:**
- Set up systemd services
- Configure nginx reverse proxy
- Enable SSL/TLS certificate
- Set up database backups
- Monitor logs regularly

## Support

- **Full Documentation:** See `CRYPTOMUS_INTEGRATION.md`
- **Troubleshooting:** Check logs in webhook_handler.py and telegram_bot.py
- **Cryptomus Support:** https://cryptomus.com/support
- **GitHub Issues:** Open an issue with your question

## Quick Commands Reference

```bash
# Start webhook server
python webhook_handler.py

# Start Telegram bot
python telegram_bot.py

# Test payment service
python cryptomus_service.py

# Initialize database
python mysql_payment_db.py

# View bot logs
tail -f telegram_bot.log

# View webhook logs
tail -f webhook_handler.log

# Check MySQL status
sudo systemctl status mysql

# Restart services (production)
sudo systemctl restart cryptomus-webhook
sudo systemctl restart telegram-bot
```

## Success Checklist

- [ ] Cryptomus account created and verified
- [ ] MySQL installed and database created
- [ ] `.env` file configured with all credentials
- [ ] Webhook URL publicly accessible
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database tables created (`python mysql_payment_db.py`)
- [ ] Webhook handler running
- [ ] Telegram bot running
- [ ] Test payment successful

## Next Steps

1. ✅ Complete setup checklist above
2. 📱 Test with small payment ($20)
3. 🎉 Start accepting crypto payments!
4. 📊 Monitor payments via admin panel
5. 💰 Watch your balance grow!

---

**Need Help?** Read the full guide: `CRYPTOMUS_INTEGRATION.md`

**Ready to Deploy?** Follow production deployment section in docs.

**Everything Working?** You're all set! 🚀
