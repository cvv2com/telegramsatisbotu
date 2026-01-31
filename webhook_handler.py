#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cryptomus Webhook Handler
Flask server to handle Cryptomus payment webhooks
"""

import logging
import json
import asyncio
from flask import Flask, request, jsonify
from telegram import Bot
from cryptomus_payment import CryptomusPayment
from mysql_payment_db import MySQLPaymentDB
from config import CRYPTOMUS_CONFIG, MYSQL_CONFIG, BOT_TOKEN
from datetime import datetime

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize Cryptomus client
cryptomus = CryptomusPayment(
    merchant_id=CRYPTOMUS_CONFIG['merchant_id'],
    payment_api_key=CRYPTOMUS_CONFIG['payment_api_key']
)

# Initialize MySQL database
mysql_db = MySQLPaymentDB(MYSQL_CONFIG)

# Initialize Telegram bot
telegram_bot = None
try:
    telegram_bot = Bot(token=BOT_TOKEN)
except Exception as e:
    logger.error(f"Failed to initialize Telegram bot: {e}")


async def send_telegram_notification(user_id: int, message: str) -> bool:
    """Send Telegram notification to user
    
    Args:
        user_id: Telegram user ID
        message: Message to send
        
    Returns:
        True if successful
    """
    try:
        if telegram_bot:
            await telegram_bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}")
        return False


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "cryptomus-webhook",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/webhook/cryptomus', methods=['POST'])
def cryptomus_webhook():
    """Handle Cryptomus payment webhooks
    
    Webhook is called when payment status changes
    """
    try:
        # Get signature from header
        signature = request.headers.get('sign')
        if not signature:
            logger.warning("Missing signature in webhook request")
            return jsonify({"error": "Missing signature"}), 401
        
        # Get raw request data
        request_data = request.get_data()
        
        # Verify signature
        if not cryptomus.verify_webhook_signature(request_data, signature):
            logger.warning("Invalid webhook signature")
            return jsonify({"error": "Invalid signature"}), 401
        
        # Parse webhook data
        webhook_data = request.json
        logger.info(f"Received webhook: {json.dumps(webhook_data, indent=2)}")
        
        # Parse payment data
        payment_data = cryptomus.parse_webhook_data(webhook_data)
        order_id = payment_data.get('order_id')
        status = payment_data.get('status')
        
        if not order_id:
            logger.error("Missing order_id in webhook data")
            return jsonify({"error": "Missing order_id"}), 400
        
        # Get payment from database
        payment = mysql_db.get_payment_by_order_id(order_id)
        if not payment:
            logger.error(f"Payment not found: order_id={order_id}")
            return jsonify({"error": "Payment not found"}), 404
        
        # Update payment in database
        success, error = mysql_db.update_payment_from_cryptomus(order_id, payment_data)
        if not success:
            logger.error(f"Failed to update payment: {error}")
            return jsonify({"error": "Database update failed"}), 500
        
        # Handle successful payment
        if cryptomus.is_payment_successful(status):
            logger.info(f"Payment successful: order_id={order_id}, status={status}")
            
            # Update user balance
            user_id = payment['user_id']
            amount = float(payment['amount'])
            
            if mysql_db.update_user_balance(user_id, amount, 'add'):
                logger.info(f"Balance updated: user_id={user_id}, amount={amount}")
                
                # Send Telegram notification
                notification_message = (
                    f"✅ *Ödeme Onaylandı!*\n\n"
                    f"💰 Miktar: ${amount:.2f}\n"
                    f"💳 Para Birimi: {payment_data.get('payer_currency', 'N/A')}\n"
                    f"🔗 İşlem ID: `{payment_data.get('txid', 'N/A')[:16]}...`\n"
                    f"📝 Sipariş No: `{order_id}`\n\n"
                    f"Bakiyeniz güncellendi. Alışverişe devam edebilirsiniz!"
                )
                
                # Send notification asynchronously
                try:
                    asyncio.run(send_telegram_notification(user_id, notification_message))
                    
                    # Log notification
                    mysql_db.add_notification(
                        payment_id=payment['id'],
                        user_id=user_id,
                        notification_type='payment_success',
                        message=notification_message
                    )
                except Exception as e:
                    logger.error(f"Failed to send notification: {e}")
            else:
                logger.error(f"Failed to update balance for user {user_id}")
        
        # Handle failed payment
        elif status in ['fail', 'cancel', 'wrong_amount']:
            logger.info(f"Payment failed/cancelled: order_id={order_id}, status={status}")
            
            # Send notification to user
            user_id = payment['user_id']
            status_text = cryptomus.get_payment_status_text(status)
            
            notification_message = (
                f"❌ *Ödeme Başarısız*\n\n"
                f"📝 Sipariş No: `{order_id}`\n"
                f"ℹ️ Durum: {status_text}\n\n"
                f"Lütfen tekrar deneyin veya destek ekibiyle iletişime geçin."
            )
            
            # Send notification asynchronously
            try:
                asyncio.run(send_telegram_notification(user_id, notification_message))
                
                # Log notification
                mysql_db.add_notification(
                    payment_id=payment['id'],
                    user_id=user_id,
                    notification_type='payment_failed',
                    message=notification_message
                )
            except Exception as e:
                logger.error(f"Failed to send notification: {e}")
        
        # Return success response
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        logger.error(f"Webhook processing error: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/payment/info/<order_id>', methods=['GET'])
def get_payment_info(order_id: str):
    """Get payment information by order ID (for testing/debugging)
    
    Args:
        order_id: Order ID
    """
    try:
        payment = mysql_db.get_payment_by_order_id(order_id)
        
        if not payment:
            return jsonify({"error": "Payment not found"}), 404
        
        # Convert datetime objects to strings
        result = dict(payment)
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting payment info: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Initialize database tables
    logger.info("Initializing database...")
    if mysql_db.initialize_database():
        logger.info("Database initialized successfully")
    else:
        logger.error("Failed to initialize database")
    
    # Start Flask server
    logger.info("Starting webhook server...")
    app.run(host='0.0.0.0', port=5000, debug=False)
