#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Payment Handler Module
Ödeme lojik ve validasyon
"""

from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from crypto_utils import (
    validate_wallet_address,
    validate_tx_hash,
    format_crypto_amount,
    parse_crypto_amount,
    calculate_crypto_amount,
    calculate_usd_amount,
    get_currency_symbol,
    get_network_info,
    get_explorer_url
)


class PaymentHandler:
    """Handle payment operations and validations"""
    
    def __init__(self, db, config):
        """Initialize payment handler
        
        Args:
            db: Database instance
            config: Configuration dictionary
        """
        self.db = db
        self.config = config
        self.crypto_wallets = config.get('CRYPTO_WALLETS', {})
    
    def create_payment(self, user_id: int, usd_amount: float, currency: str,
                      exchange_rate: float) -> Tuple[bool, str, Optional[int]]:
        """Create a new payment transaction
        
        Args:
            user_id: User's Telegram ID
            usd_amount: Amount in USD
            currency: Cryptocurrency type
            exchange_rate: Current exchange rate
            
        Returns:
            (success, message, transaction_id)
        """
        # Validate currency
        currency = currency.upper()
        if currency.lower() not in self.crypto_wallets:
            return False, f"Unsupported currency: {currency}", None
        
        # Get wallet address
        wallet_address = self.crypto_wallets.get(currency.lower())
        if not wallet_address:
            return False, f"Wallet address not configured for {currency}", None
        
        # Validate wallet address
        if not validate_wallet_address(wallet_address, currency):
            return False, f"Invalid wallet address for {currency}", None
        
        # Calculate crypto amount
        try:
            crypto_amount = calculate_crypto_amount(usd_amount, exchange_rate)
        except ValueError as e:
            return False, str(e), None
        
        # Get network info
        network_info = get_network_info(currency)
        required_confirmations = network_info.get('confirmations_required', 3)
        
        # Create transaction
        try:
            transaction_id = self.db.create_payment_transaction(
                user_id=user_id,
                amount=crypto_amount,
                currency=currency,
                wallet_address=wallet_address,
                exchange_rate=exchange_rate,
                usd_equivalent=usd_amount,
                timeout_minutes=30,
                required_confirmations=required_confirmations,
                notes=f"Payment for ${usd_amount:.2f}"
            )
            
            return True, "Payment created successfully", transaction_id
        except Exception as e:
            return False, f"Error creating payment: {str(e)}", None
    
    def validate_payment(self, tx_hash: str, currency: str) -> Tuple[bool, str]:
        """Validate a payment transaction hash
        
        Args:
            tx_hash: Transaction hash
            currency: Cryptocurrency type
            
        Returns:
            (is_valid, message)
        """
        currency = currency.upper()
        
        # Validate format
        if not validate_tx_hash(tx_hash, currency):
            return False, f"Invalid transaction hash format for {currency}"
        
        # Check if hash already exists
        existing_tx = self.db.get_transaction_by_hash(tx_hash)
        if existing_tx:
            return False, f"Transaction hash already used (ID: {existing_tx['id']})"
        
        return True, "Transaction hash is valid"
    
    def confirm_payment(self, transaction_id: int, tx_hash: str,
                       confirmations: int = None) -> Tuple[bool, str]:
        """Confirm a payment transaction
        
        Args:
            transaction_id: Transaction ID
            tx_hash: Transaction hash
            confirmations: Number of confirmations
            
        Returns:
            (success, message)
        """
        # Get transaction
        tx = self.db.get_transaction_by_id(transaction_id)
        if not tx:
            return False, "Transaction not found"
        
        # Check status
        if tx['status'] != 'pending':
            return False, f"Transaction already {tx['status']}"
        
        # Validate transaction hash (skip if it's already set for this transaction)
        if tx.get('tx_hash') != tx_hash:
            is_valid, message = self.validate_payment(tx_hash, tx['currency'])
            if not is_valid:
                return False, message
        
        # Confirm transaction
        success = self.db.confirm_transaction(
            transaction_id=transaction_id,
            tx_hash=tx_hash,
            confirmations=confirmations,
            credit_balance=True
        )
        
        if success:
            return True, f"Payment confirmed! ${tx['usd_equivalent']:.2f} credited to balance"
        else:
            return False, "Error confirming payment"
    
    def get_payment_instructions(self, transaction_id: int, language: str = 'tr') -> Optional[Dict]:
        """Get payment instructions for a transaction
        
        Args:
            transaction_id: Transaction ID
            language: Language code
            
        Returns:
            Dictionary with payment instructions or None
        """
        # Get transaction
        tx = self.db.get_transaction_by_id(transaction_id)
        if not tx:
            return None
        
        # Get network info
        network_info = get_network_info(tx['currency'])
        
        # Calculate estimated confirmation time
        avg_time = network_info.get('avg_confirmation_time_minutes', 10)
        required_confirmations = tx.get('required_confirmations', 3)
        estimated_time = avg_time * required_confirmations
        
        # Get timeout info
        timeout_at = datetime.fromisoformat(tx['timeout_at'])
        time_remaining = timeout_at - datetime.now()
        minutes_remaining = int(time_remaining.total_seconds() / 60)
        
        # Format crypto amount
        crypto_amount_str = format_crypto_amount(tx['amount'], tx['currency'])
        
        # Get currency symbol
        symbol = get_currency_symbol(tx['currency'])
        
        instructions = {
            'transaction_id': transaction_id,
            'currency': tx['currency'],
            'currency_symbol': symbol,
            'network_name': network_info.get('name', tx['currency']),
            'crypto_amount': tx['amount'],
            'crypto_amount_formatted': f"{crypto_amount_str} {tx['currency']}",
            'usd_amount': tx['usd_equivalent'],
            'wallet_address': tx['wallet_address'],
            'exchange_rate': tx['exchange_rate'],
            'required_confirmations': required_confirmations,
            'estimated_time_minutes': estimated_time,
            'timeout_minutes': minutes_remaining,
            'status': tx['status'],
            'created_at': tx['created_at'],
            'timeout_at': tx['timeout_at']
        }
        
        return instructions
    
    def check_timeouts(self) -> list:
        """Check for timed out transactions
        
        Returns:
            List of timed out transaction IDs
        """
        pending_transactions = self.db.get_pending_transactions()
        timed_out = []
        
        for tx in pending_transactions:
            if self.db.check_transaction_timeout(tx['id']):
                # Mark as timeout
                self.db.update_transaction_status(tx['id'], 'timeout', notes='Payment timed out')
                timed_out.append(tx['id'])
        
        return timed_out
    
    def cancel_payment(self, transaction_id: int, reason: str = "Cancelled") -> Tuple[bool, str]:
        """Cancel a payment transaction
        
        Args:
            transaction_id: Transaction ID
            reason: Cancellation reason
            
        Returns:
            (success, message)
        """
        # Get transaction
        tx = self.db.get_transaction_by_id(transaction_id)
        if not tx:
            return False, "Transaction not found"
        
        # Check status
        if tx['status'] != 'pending':
            return False, f"Cannot cancel {tx['status']} transaction"
        
        # Cancel transaction
        success = self.db.cancel_payment(transaction_id, reason)
        
        if success:
            return True, f"Transaction #{transaction_id} cancelled"
        else:
            return False, "Error cancelling transaction"
    
    def get_transaction_status(self, transaction_id: int) -> Optional[Dict]:
        """Get transaction status information
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            Dictionary with status information or None
        """
        tx = self.db.get_transaction_by_id(transaction_id)
        if not tx:
            return None
        
        # Get network info
        network_info = get_network_info(tx['currency'])
        
        # Get explorer URL if tx_hash exists
        explorer_url = ""
        if tx.get('tx_hash'):
            explorer_url = get_explorer_url(tx['tx_hash'], tx['currency'])
        
        status_info = {
            'transaction_id': tx['id'],
            'status': tx['status'],
            'currency': tx['currency'],
            'amount': tx['amount'],
            'usd_equivalent': tx['usd_equivalent'],
            'wallet_address': tx['wallet_address'],
            'tx_hash': tx.get('tx_hash'),
            'explorer_url': explorer_url,
            'confirmations': tx.get('confirmations', 0),
            'required_confirmations': tx.get('required_confirmations', 3),
            'created_at': tx['created_at'],
            'confirmed_at': tx.get('confirmed_at'),
            'timeout_at': tx['timeout_at'],
            'notes': tx.get('notes', ''),
            'network_name': network_info.get('name', tx['currency'])
        }
        
        return status_info
    
    def format_transaction_message(self, transaction_id: int, language: str = 'tr') -> Optional[str]:
        """Format transaction information as a message
        
        Args:
            transaction_id: Transaction ID
            language: Language code
            
        Returns:
            Formatted message or None
        """
        status_info = self.get_transaction_status(transaction_id)
        if not status_info:
            return None
        
        # Status emoji
        status_emoji = {
            'pending': '⏳',
            'confirmed': '✅',
            'failed': '❌',
            'timeout': '⏰'
        }
        
        emoji = status_emoji.get(status_info['status'], '❓')
        
        # Format amount
        crypto_amount_str = format_crypto_amount(
            status_info['amount'],
            status_info['currency']
        )
        
        # Build message
        lines = [
            f"{emoji} **Transaction #{status_info['transaction_id']}**",
            f"",
            f"💰 Amount: {crypto_amount_str} {status_info['currency']}",
            f"💵 USD Equivalent: ${status_info['usd_equivalent']:.2f}",
            f"📊 Status: {status_info['status'].upper()}",
            f"🌐 Network: {status_info['network_name']}",
        ]
        
        # Add TX hash if available
        if status_info['tx_hash']:
            lines.append(f"🔗 TX Hash: `{status_info['tx_hash'][:16]}...`")
            if status_info['explorer_url']:
                lines.append(f"🔍 Explorer: {status_info['explorer_url']}")
        
        # Add confirmations
        if status_info['status'] == 'pending':
            lines.append(f"✓ Confirmations: {status_info['confirmations']}/{status_info['required_confirmations']}")
        
        # Add timestamps
        lines.append(f"📅 Created: {status_info['created_at'][:19]}")
        
        if status_info['confirmed_at']:
            lines.append(f"✅ Confirmed: {status_info['confirmed_at'][:19]}")
        
        # Add notes if available
        if status_info['notes']:
            lines.append(f"📝 Notes: {status_info['notes']}")
        
        return "\n".join(lines)
