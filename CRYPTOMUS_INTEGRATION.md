# Cryptomus Crypto Payment Integration Guide

## Overview

This project now integrates with **Cryptomus** payment gateway to accept cryptocurrency payments (Bitcoin, Ethereum, USDT TRC-20) instead of PayPal. The integration provides:

- ✅ Automated payment processing
- ✅ Real-time payment status updates via webhooks
- ✅ Automatic balance updates upon successful payment
- ✅ Telegram notifications for payment confirmations
- ✅ Admin panel for payment history and management
- ✅ MySQL database for persistent payment records

## Supported Cryptocurrencies

- **Bitcoin (BTC)** - Bitcoin network
- **Ethereum (ETH)** - Ethereum network
- **USDT** - Tether on Tron (TRC-20) network

## Architecture

### Components

1. **cryptomus_payment.py** - Low-level Cryptomus API client
2. **mysql_payment_db.py** - MySQL database handler for payments
3. **cryptomus_service.py** - High-level payment service integrating API + DB
4. **webhook_handler.py** - Flask server for handling Cryptomus webhooks
5. **telegram_bot.py** - Updated with Cryptomus payment flow

### Payment Flow

```
User Request Payment
       ↓
Bot Creates Payment (cryptomus_service)
       ↓
Cryptomus API Creates Invoice
       ↓
User Receives Payment URL
       ↓
User Makes Payment
       ↓
Cryptomus Webhook Notification
       ↓
Balance Updated + Telegram Notification
```

## Setup Instructions

### 1. Sign Up for Cryptomus

1. Visit [https://cryptomus.com](https://cryptomus.com)
2. Create a merchant account
3. Complete KYB verification (business verification)
4. Verify your domain

### 2. Get API Credentials

1. Go to your Cryptomus dashboard
2. Navigate to **API Settings**
3. Copy the following:
   - Merchant ID (UUID)
   - Payment API Key
   - Payout API Key (optional)

### 3. Configure Environment Variables

Edit your `.env` file and add:

```bash
# Cryptomus Configuration
CRYPTOMUS_MERCHANT_ID=your_merchant_uuid_here
CRYPTOMUS_PAYMENT_API_KEY=your_payment_api_key_here
CRYPTOMUS_PAYOUT_API_KEY=your_payout_api_key_here
CRYPTOMUS_WEBHOOK_SECRET=your_webhook_secret_here

# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=telegram_sales_bot
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password_here
```

### 4. Set Up MySQL Database

Install MySQL if not already installed:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install mysql-server

# macOS
brew install mysql

# Windows
# Download from https://dev.mysql.com/downloads/mysql/
```

Create the database:

```bash
mysql -u root -p
```

```sql
CREATE DATABASE telegram_sales_bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'botuser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON telegram_sales_bot.* TO 'botuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Update `.env` with your MySQL credentials.

### 5. Initialize Database Tables

Run the MySQL payment database script to create tables:

```bash
python mysql_payment_db.py
```

This will create the following tables:
- `cryptomus_payments` - Payment transactions
- `payment_notifications` - Notification logs
- `user_balances` - User balance records

### 6. Install Dependencies

```bash
pip install -r requirements.txt
```

### 7. Configure Webhook URL

The webhook handler needs to be accessible from the internet. Options:

**Option A: Use ngrok (for development/testing)**

```bash
# Install ngrok
# Download from https://ngrok.com/download

# Start ngrok tunnel
ngrok http 5000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

**Option B: Deploy to production server**

Deploy `webhook_handler.py` to your production server with a public IP/domain.

**Update webhook URL in telegram_bot.py:**

```python
# In payment_amount_entered function
webhook_url = "https://your-actual-domain.com/webhook/cryptomus"
```

### 8. Start the Services

**Terminal 1: Start Webhook Handler**

```bash
python webhook_handler.py
```

This starts Flask server on port 5000.

**Terminal 2: Start Telegram Bot**

```bash
python telegram_bot.py
```

## Usage

### For Users

1. Start the bot: `/start`
2. Create payment: Select "💰 Create Payment"
3. Choose cryptocurrency: BTC, ETH, or USDT
4. Enter amount: Minimum $20
5. Click payment link
6. Complete payment on Cryptomus page
7. Receive automatic confirmation via Telegram

### For Admins

**View Payment History**

```bash
/admin_payments
/admin_payments 2  # Page 2
```

**View Payment Statistics**

```bash
/payment_stats
```

**User Commands**

```bash
/payment_history  # View your payment history
```

## API Reference

### CryptomusPayment Class

```python
from cryptomus_payment import CryptomusPayment

client = CryptomusPayment(merchant_id, payment_api_key)

# Create payment
success, result, error = client.create_payment(
    amount="10.00",
    currency="USDT",
    order_id="ORDER_123",
    url_callback="https://yoursite.com/webhook",
    network="TRON"
)

# Get payment info
success, info, error = client.get_payment_info(uuid="payment_uuid")

# Verify webhook signature
is_valid = client.verify_webhook_signature(request_data, signature)
```

### MySQLPaymentDB Class

```python
from mysql_payment_db import MySQLPaymentDB

db = MySQLPaymentDB(MYSQL_CONFIG)

# Create payment record
success, payment_id, error = db.create_payment(
    user_id=123456789,
    order_id="ORDER_123",
    amount=10.00,
    currency="USDT"
)

# Get user payments
payments = db.get_user_payments(user_id=123456789, limit=10)

# Update balance
db.update_user_balance(user_id=123456789, amount=10.00, operation='add')
```

### CryptomusPaymentService Class

```python
from cryptomus_service import get_payment_service

service = get_payment_service()

# Create payment
success, payment_info, error = service.create_payment(
    user_id=123456789,
    amount=10.00,
    currency="USDT",
    webhook_url="https://yoursite.com/webhook"
)

# Get payment status
success, payment_data, error = service.get_payment_status(order_id)

# Get user balance
balance = service.get_user_balance(user_id)
```

## Webhook Endpoints

### POST /webhook/cryptomus

Receives payment status updates from Cryptomus.

**Request Headers:**
- `sign`: HMAC-MD5 signature

**Request Body:**
```json
{
  "uuid": "payment_uuid",
  "order_id": "ORDER_123",
  "amount": "10.00",
  "currency": "USD",
  "payer_currency": "USDT",
  "status": "paid",
  "txid": "transaction_hash",
  ...
}
```

**Response:**
```json
{
  "status": "ok"
}
```

### GET /payment/info/:order_id

Get payment information (for debugging).

**Response:**
```json
{
  "id": 1,
  "user_id": 123456789,
  "order_id": "ORDER_123",
  "amount": 10.00,
  "currency": "USDT",
  "status": "paid",
  ...
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "cryptomus-webhook",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Payment Status Flow

```
pending → paid → Balance Updated + Notification Sent
pending → fail → Failure Notification Sent
pending → cancel → Cancellation Notification Sent
pending → wrong_amount → Error Notification Sent
```

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Webhook Signature**: Always verify webhook signatures
3. **HTTPS**: Use HTTPS for webhook endpoints
4. **Database**: Use strong passwords for MySQL
5. **Environment Variables**: Store all secrets in `.env` file
6. **IP Whitelist**: Consider whitelisting Cryptomus IPs

## Troubleshooting

### Payment Not Created

**Issue**: Payment creation fails

**Solutions**:
- Check API credentials in `.env`
- Verify Cryptomus account is verified
- Check network connectivity
- Review logs: `tail -f webhook_handler.log`

### Webhook Not Received

**Issue**: No notification after payment

**Solutions**:
- Verify webhook URL is publicly accessible
- Test webhook endpoint: `curl https://your-domain.com/webhook/cryptomus`
- Check Flask server logs
- Verify Cryptomus webhook configuration

### Database Connection Error

**Issue**: Cannot connect to MySQL

**Solutions**:
- Verify MySQL is running: `sudo systemctl status mysql`
- Check credentials in `.env`
- Ensure database exists: `SHOW DATABASES;`
- Check firewall settings

### Balance Not Updated

**Issue**: Payment confirmed but balance not updated

**Solutions**:
- Check webhook logs for errors
- Verify payment status in database: `SELECT * FROM cryptomus_payments WHERE order_id='ORDER_123';`
- Check user_balances table
- Review webhook_handler.py logs

## Production Deployment

### Using Systemd (Linux)

**Create webhook service:**

```bash
sudo nano /etc/systemd/system/cryptomus-webhook.service
```

```ini
[Unit]
Description=Cryptomus Webhook Handler
After=network.target mysql.service

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/telegramsatisbotu
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python webhook_handler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Create bot service:**

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

```ini
[Unit]
Description=Telegram Sales Bot
After=network.target mysql.service

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/telegramsatisbotu
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start services:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable cryptomus-webhook
sudo systemctl enable telegram-bot
sudo systemctl start cryptomus-webhook
sudo systemctl start telegram-bot
```

### Using Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /webhook/cryptomus {
        proxy_pass http://localhost:5000/webhook/cryptomus;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Testing

### Test Payment Creation

```bash
python cryptomus_service.py
```

### Test Database

```bash
python mysql_payment_db.py
```

### Test Webhook

```bash
# Start webhook server
python webhook_handler.py

# In another terminal, send test webhook
curl -X POST http://localhost:5000/webhook/cryptomus \
  -H "Content-Type: application/json" \
  -H "sign: test_signature" \
  -d '{"order_id":"TEST_123","status":"paid"}'
```

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in webhook_handler.py and telegram_bot.py
3. Open an issue on GitHub
4. Contact Cryptomus support: https://cryptomus.com/support

## License

MIT License - see LICENSE file for details
