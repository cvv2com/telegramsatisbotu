#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cryptomus Payment Integration Module
Handles payment creation, webhook validation, and status updates
"""

import hashlib
import hmac
import json
import logging
import requests
from typing import Dict, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class CryptomusPayment:
    """Cryptomus Payment Gateway Integration"""
    
    BASE_URL = "https://api.cryptomus.com/v1"
    
    def __init__(self, merchant_id: str, payment_api_key: str):
        """Initialize Cryptomus payment client
        
        Args:
            merchant_id: Cryptomus merchant UUID
            payment_api_key: Payment API key from Cryptomus
        """
        self.merchant_id = merchant_id
        self.payment_api_key = payment_api_key
        
        if not merchant_id or not payment_api_key:
            logger.warning("Cryptomus credentials not configured")
    
    def _generate_signature(self, data: dict) -> str:
        """Generate signature for API request
        
        Args:
            data: Request payload dictionary
            
        Returns:
            HMAC-SHA256 signature
        """
        # Convert data to JSON string and encode
        json_string = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        message = json_string.encode('utf-8')
        
        # Create HMAC signature
        signature = hmac.new(
            self.payment_api_key.encode('utf-8'),
            message,
            hashlib.md5
        ).hexdigest()
        
        return signature
    
    def _make_request(self, endpoint: str, data: dict) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Make authenticated request to Cryptomus API
        
        Args:
            endpoint: API endpoint path
            data: Request payload
            
        Returns:
            (success, response_data, error_message)
        """
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            
            # Generate signature
            signature = self._generate_signature(data)
            
            # Set headers
            headers = {
                "merchant": self.merchant_id,
                "sign": signature,
                "Content-Type": "application/json"
            }
            
            # Make request
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                if result.get('state') == 0:  # Success state
                    return True, result.get('result'), None
                else:
                    error_msg = result.get('message', 'Unknown error')
                    logger.error(f"Cryptomus API error: {error_msg}")
                    return False, None, error_msg
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"Cryptomus API request failed: {error_msg}")
                return False, None, error_msg
                
        except requests.exceptions.Timeout:
            error_msg = "Request timeout"
            logger.error(f"Cryptomus API timeout: {error_msg}")
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(f"Cryptomus API exception: {error_msg}")
            return False, None, error_msg
    
    def create_payment(self, amount: str, currency: str, order_id: str,
                      url_callback: str, url_return: Optional[str] = None,
                      network: Optional[str] = None, lifetime: int = 3600) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Create a new payment invoice
        
        Args:
            amount: Amount in USD
            currency: Target cryptocurrency (BTC, ETH, USDT, etc.)
            order_id: Unique order identifier
            url_callback: Webhook URL for payment notifications
            url_return: Optional return URL after payment
            network: Blockchain network (e.g., 'TRON' for USDT TRC-20)
            lifetime: Payment lifetime in seconds (default: 3600 = 1 hour)
            
        Returns:
            (success, payment_data, error_message)
            payment_data contains: uuid, order_id, amount, url (payment page), etc.
        """
        data = {
            "amount": str(amount),
            "currency": currency.upper(),
            "order_id": str(order_id),
            "url_callback": url_callback,
            "lifetime": str(lifetime),
        }
        
        # Add optional parameters
        if url_return:
            data["url_return"] = url_return
        
        if network:
            data["network"] = network.upper()
        
        # Create payment
        success, result, error = self._make_request("payment", data)
        
        if success and result:
            logger.info(f"Payment created: order_id={order_id}, uuid={result.get('uuid')}")
            return True, result, None
        else:
            logger.error(f"Failed to create payment: {error}")
            return False, None, error
    
    def get_payment_info(self, uuid: str = None, order_id: str = None) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Get payment information
        
        Args:
            uuid: Payment UUID (provide either uuid or order_id)
            order_id: Order ID (provide either uuid or order_id)
            
        Returns:
            (success, payment_info, error_message)
        """
        if not uuid and not order_id:
            return False, None, "Either uuid or order_id must be provided"
        
        data = {}
        if uuid:
            data["uuid"] = uuid
        if order_id:
            data["order_id"] = str(order_id)
        
        success, result, error = self._make_request("payment/info", data)
        
        if success and result:
            return True, result, None
        else:
            return False, None, error
    
    def verify_webhook_signature(self, request_data: bytes, signature: str) -> bool:
        """Verify webhook signature from Cryptomus
        
        Args:
            request_data: Raw request body (bytes)
            signature: Signature from 'sign' header
            
        Returns:
            True if signature is valid
        """
        try:
            # Calculate expected signature
            expected_signature = hmac.new(
                self.payment_api_key.encode('utf-8'),
                request_data,
                hashlib.md5
            ).hexdigest()
            
            # Compare signatures securely
            return hmac.compare_digest(expected_signature, signature)
            
        except Exception as e:
            logger.error(f"Webhook signature verification failed: {e}")
            return False
    
    def parse_webhook_data(self, data: dict) -> Dict:
        """Parse webhook data from Cryptomus
        
        Args:
            data: Webhook payload dictionary
            
        Returns:
            Parsed payment information
        """
        return {
            "uuid": data.get("uuid"),
            "order_id": data.get("order_id"),
            "amount": data.get("amount"),
            "payment_amount": data.get("payment_amount"),
            "payer_amount": data.get("payer_amount"),
            "currency": data.get("currency"),
            "payer_currency": data.get("payer_currency"),
            "network": data.get("network"),
            "address": data.get("address"),
            "from_address": data.get("from"),
            "txid": data.get("txid"),
            "payment_status": data.get("payment_status"),
            "url": data.get("url"),
            "expired_at": data.get("expired_at"),
            "status": data.get("status"),
            "is_final": data.get("is_final"),
            "additional_data": data.get("additional_data"),
        }
    
    @staticmethod
    def get_payment_status_text(status: str) -> str:
        """Get human-readable payment status
        
        Args:
            status: Cryptomus payment status
            
        Returns:
            Human-readable status text
        """
        status_map = {
            "check": "Checking payment",
            "paid": "Paid successfully",
            "paid_over": "Overpaid",
            "fail": "Payment failed",
            "wrong_amount": "Wrong amount received",
            "cancel": "Payment cancelled",
            "system_fail": "System failure",
            "refund_process": "Refund in process",
            "refund_fail": "Refund failed",
            "refund_paid": "Refunded",
            "locked": "Payment locked",
        }
        return status_map.get(status, f"Unknown status: {status}")
    
    @staticmethod
    def is_payment_successful(status: str) -> bool:
        """Check if payment status indicates success
        
        Args:
            status: Cryptomus payment status
            
        Returns:
            True if payment is successful
        """
        return status in ["paid", "paid_over"]
    
    @staticmethod
    def is_payment_final(status: str) -> bool:
        """Check if payment status is final (no more updates expected)
        
        Args:
            status: Cryptomus payment status
            
        Returns:
            True if payment status is final
        """
        return status in ["paid", "paid_over", "fail", "cancel", "refund_paid", "wrong_amount"]


def test_cryptomus_integration():
    """Test Cryptomus integration with sample data"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    merchant_id = os.getenv("CRYPTOMUS_MERCHANT_ID")
    api_key = os.getenv("CRYPTOMUS_PAYMENT_API_KEY")
    
    if not merchant_id or not api_key:
        print("❌ Cryptomus credentials not configured")
        return
    
    client = CryptomusPayment(merchant_id, api_key)
    
    # Test payment creation
    print("Testing payment creation...")
    success, result, error = client.create_payment(
        amount="10.00",
        currency="USDT",
        order_id=f"TEST_{int(datetime.now().timestamp())}",
        url_callback="https://example.com/webhook",
        network="TRON",
        lifetime=3600
    )
    
    if success:
        print("✅ Payment created successfully!")
        print(f"   UUID: {result.get('uuid')}")
        print(f"   Amount: {result.get('amount')}")
        print(f"   Payment URL: {result.get('url')}")
    else:
        print(f"❌ Payment creation failed: {error}")


if __name__ == "__main__":
    test_cryptomus_integration()
