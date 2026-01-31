#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrated Payment Service for Cryptomus
Combines Cryptomus API with database and Telegram bot
"""

import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
from cryptomus_payment import CryptomusPayment
from mysql_payment_db import MySQLPaymentDB
from config import CRYPTOMUS_CONFIG, MYSQL_CONFIG

logger = logging.getLogger(__name__)


class CryptomusPaymentService:
    """Integrated payment service for Cryptomus"""
    
    def __init__(self):
        """Initialize payment service"""
        # Initialize Cryptomus client
        self.cryptomus = CryptomusPayment(
            merchant_id=CRYPTOMUS_CONFIG['merchant_id'],
            payment_api_key=CRYPTOMUS_CONFIG['payment_api_key']
        )
        
        # Initialize MySQL database
        self.mysql_db = MySQLPaymentDB(MYSQL_CONFIG)
        
        # Supported currencies
        self.supported_currencies = CRYPTOMUS_CONFIG['supported_currencies']
        self.currency_networks = CRYPTOMUS_CONFIG['currency_networks']
    
    def create_payment(self, user_id: int, amount: float, currency: str,
                      webhook_url: str, return_url: Optional[str] = None) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Create a new payment
        
        Args:
            user_id: Telegram user ID
            amount: Amount in USD
            currency: Cryptocurrency (BTC, ETH, USDT)
            webhook_url: Webhook URL for payment notifications
            return_url: Optional return URL after payment
            
        Returns:
            (success, payment_info, error_message)
            payment_info contains: order_id, payment_url, amount, currency, etc.
        """
        try:
            # Validate currency
            currency = currency.upper()
            if currency not in self.supported_currencies:
                return False, None, f"Unsupported currency: {currency}. Supported: {', '.join(self.supported_currencies)}"
            
            # Generate unique order ID
            order_id = f"ORDER_{user_id}_{int(datetime.now().timestamp())}"
            
            # Get network for currency
            network = self.currency_networks.get(currency)
            
            # Create payment in database first
            success, payment_id, error = self.mysql_db.create_payment(
                user_id=user_id,
                order_id=order_id,
                amount=amount,
                currency=currency,
                network=network
            )
            
            if not success:
                logger.error(f"Failed to create payment in database: {error}")
                return False, None, f"Database error: {error}"
            
            # Create payment with Cryptomus
            success, cryptomus_result, error = self.cryptomus.create_payment(
                amount=str(amount),
                currency=currency,
                order_id=order_id,
                url_callback=webhook_url,
                url_return=return_url,
                network=network,
                lifetime=3600  # 1 hour
            )
            
            if not success:
                logger.error(f"Failed to create payment with Cryptomus: {error}")
                return False, None, f"Payment gateway error: {error}"
            
            # Update payment with Cryptomus data
            update_success, update_error = self.mysql_db.update_payment_from_cryptomus(
                order_id=order_id,
                payment_data=cryptomus_result
            )
            
            if not update_success:
                logger.warning(f"Failed to update payment with Cryptomus data: {update_error}")
            
            # Return payment information
            payment_info = {
                "payment_id": payment_id,
                "order_id": order_id,
                "payment_uuid": cryptomus_result.get('uuid'),
                "payment_url": cryptomus_result.get('url'),
                "amount": amount,
                "currency": currency,
                "network": network,
                "address": cryptomus_result.get('address'),
                "expired_at": cryptomus_result.get('expired_at'),
            }
            
            logger.info(f"Payment created successfully: order_id={order_id}, payment_url={payment_info['payment_url']}")
            return True, payment_info, None
            
        except Exception as e:
            logger.error(f"Error creating payment: {e}", exc_info=True)
            return False, None, str(e)
    
    def get_payment_status(self, order_id: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Get payment status
        
        Args:
            order_id: Order ID
            
        Returns:
            (success, payment_data, error_message)
        """
        try:
            # Get payment from database
            payment = self.mysql_db.get_payment_by_order_id(order_id)
            
            if not payment:
                return False, None, "Payment not found"
            
            # Convert to dict with proper types
            payment_data = dict(payment)
            for key, value in payment_data.items():
                if isinstance(value, datetime):
                    payment_data[key] = value.isoformat()
            
            return True, payment_data, None
            
        except Exception as e:
            logger.error(f"Error getting payment status: {e}")
            return False, None, str(e)
    
    def get_user_payments(self, user_id: int, limit: int = 10) -> list:
        """Get user's payment history
        
        Args:
            user_id: Telegram user ID
            limit: Maximum number of records
            
        Returns:
            List of payment dictionaries
        """
        try:
            payments = self.mysql_db.get_user_payments(user_id, limit)
            
            # Convert datetime objects to strings
            result = []
            for payment in payments:
                payment_dict = dict(payment)
                for key, value in payment_dict.items():
                    if isinstance(value, datetime):
                        payment_dict[key] = value.isoformat()
                result.append(payment_dict)
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting user payments: {e}")
            return []
    
    def get_user_balance(self, user_id: int) -> float:
        """Get user's current balance
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Balance amount
        """
        return self.mysql_db.get_user_balance(user_id)
    
    def format_payment_message(self, payment_data: Dict, language: str = 'tr') -> str:
        """Format payment information as a message
        
        Args:
            payment_data: Payment data dictionary
            language: Language code (tr/en)
            
        Returns:
            Formatted message
        """
        if language == 'tr':
            status_map = {
                'pending': '⏳ Beklemede',
                'paid': '✅ Ödendi',
                'paid_over': '✅ Ödendi (Fazla)',
                'fail': '❌ Başarısız',
                'cancel': '❌ İptal',
                'wrong_amount': '⚠️ Yanlış Miktar',
            }
            
            message = f"**Ödeme Bilgileri**\n\n"
            message += f"📝 Sipariş No: `{payment_data['order_id']}`\n"
            message += f"💰 Miktar: ${payment_data['amount']:.2f}\n"
            message += f"💳 Para Birimi: {payment_data['currency']}\n"
            message += f"🌐 Network: {payment_data.get('network', 'N/A')}\n"
            message += f"📊 Durum: {status_map.get(payment_data['status'], payment_data['status'])}\n"
            
            if payment_data.get('txid'):
                message += f"🔗 İşlem ID: `{payment_data['txid'][:16]}...`\n"
            
            if payment_data.get('payment_url'):
                message += f"\n[Ödeme Yap]({payment_data['payment_url']})"
        else:
            status_map = {
                'pending': '⏳ Pending',
                'paid': '✅ Paid',
                'paid_over': '✅ Paid (Overpaid)',
                'fail': '❌ Failed',
                'cancel': '❌ Cancelled',
                'wrong_amount': '⚠️ Wrong Amount',
            }
            
            message = f"**Payment Information**\n\n"
            message += f"📝 Order ID: `{payment_data['order_id']}`\n"
            message += f"💰 Amount: ${payment_data['amount']:.2f}\n"
            message += f"💳 Currency: {payment_data['currency']}\n"
            message += f"🌐 Network: {payment_data.get('network', 'N/A')}\n"
            message += f"📊 Status: {status_map.get(payment_data['status'], payment_data['status'])}\n"
            
            if payment_data.get('txid'):
                message += f"🔗 Transaction ID: `{payment_data['txid'][:16]}...`\n"
            
            if payment_data.get('payment_url'):
                message += f"\n[Make Payment]({payment_data['payment_url']})"
        
        return message


# Global instance
payment_service = None


def get_payment_service() -> CryptomusPaymentService:
    """Get global payment service instance
    
    Returns:
        CryptomusPaymentService instance
    """
    global payment_service
    if payment_service is None:
        payment_service = CryptomusPaymentService()
    return payment_service


if __name__ == "__main__":
    # Test payment service
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("Testing payment service...")
    
    service = get_payment_service()
    
    # Test payment creation
    print("\nCreating test payment...")
    success, payment_info, error = service.create_payment(
        user_id=123456789,
        amount=10.00,
        currency="USDT",
        webhook_url="https://example.com/webhook",
        return_url="https://example.com/return"
    )
    
    if success:
        print("✅ Payment created successfully!")
        print(f"   Order ID: {payment_info['order_id']}")
        print(f"   Payment URL: {payment_info['payment_url']}")
        
        # Test getting payment status
        print("\nGetting payment status...")
        success, payment_data, error = service.get_payment_status(payment_info['order_id'])
        if success:
            print("✅ Payment status retrieved")
            print(f"   Status: {payment_data['status']}")
        else:
            print(f"❌ Failed to get payment status: {error}")
    else:
        print(f"❌ Failed to create payment: {error}")
