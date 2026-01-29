#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Timeout Handler Module
Zaman aşımı yönetimi
"""

import asyncio
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TimeoutHandler:
    """Handle payment timeouts and notifications"""
    
    def __init__(self, db, bot_application=None, check_interval_minutes: int = 5):
        """Initialize timeout handler
        
        Args:
            db: Database instance
            bot_application: Telegram bot application (for notifications)
            check_interval_minutes: Interval between timeout checks (default: 5 minutes)
        """
        self.db = db
        self.bot_application = bot_application
        self.check_interval_minutes = check_interval_minutes
        self.is_running = False
        self._task = None
    
    async def check_payment_timeouts(self):
        """Check for timed out payments and notify users"""
        try:
            pending_transactions = self.db.get_pending_transactions()
            
            for tx in pending_transactions:
                try:
                    # Check if transaction has timed out
                    if self.db.check_transaction_timeout(tx['id']):
                        logger.info(f"Transaction #{tx['id']} has timed out")
                        
                        # Mark as timeout
                        self.db.update_transaction_status(
                            tx['id'],
                            'timeout',
                            notes='Payment timed out - no transaction received'
                        )
                        
                        # Notify user if bot is available
                        if self.bot_application:
                            await self.notify_user_timeout(tx['user_id'], tx)
                        
                except Exception as e:
                    logger.error(f"Error processing timeout for transaction #{tx['id']}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error checking payment timeouts: {e}")
    
    async def notify_user_timeout(self, user_id: int, transaction: dict):
        """Notify user about transaction timeout
        
        Args:
            user_id: User's Telegram ID
            transaction: Transaction dictionary
        """
        if not self.bot_application:
            return
        
        try:
            message = (
                f"⏰ **Payment Timeout**\n\n"
                f"Your payment transaction #{transaction['id']} has timed out.\n\n"
                f"💰 Amount: {transaction['amount']:.8f} {transaction['currency']}\n"
                f"💵 USD: ${transaction.get('usd_equivalent', 0):.2f}\n\n"
                f"The transaction was not completed within the timeout period. "
                f"If you have sent the payment, please contact support with your transaction hash.\n\n"
                f"You can create a new payment request at any time."
            )
            
            await self.bot_application.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Timeout notification sent to user {user_id} for transaction #{transaction['id']}")
            
        except Exception as e:
            logger.error(f"Error sending timeout notification to user {user_id}: {e}")
    
    async def notify_user_confirmed(self, user_id: int, transaction: dict):
        """Notify user about transaction confirmation
        
        Args:
            user_id: User's Telegram ID
            transaction: Transaction dictionary
        """
        if not self.bot_application:
            return
        
        try:
            message = (
                f"✅ **Payment Confirmed!**\n\n"
                f"Your payment has been confirmed!\n\n"
                f"💰 Amount: {transaction['amount']:.8f} {transaction['currency']}\n"
                f"💵 USD: ${transaction.get('usd_equivalent', 0):.2f}\n"
                f"🔗 TX: `{transaction.get('tx_hash', 'N/A')[:16]}...`\n\n"
                f"Your balance has been credited. You can now use it to purchase gift cards!\n\n"
                f"Thank you for your payment! 🎉"
            )
            
            await self.bot_application.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Confirmation notification sent to user {user_id} for transaction #{transaction['id']}")
            
        except Exception as e:
            logger.error(f"Error sending confirmation notification to user {user_id}: {e}")
    
    async def _timeout_check_loop(self):
        """Main loop for checking timeouts"""
        logger.info(f"Timeout handler started (check interval: {self.check_interval_minutes} minutes)")
        
        while self.is_running:
            try:
                await self.check_payment_timeouts()
                
                # Wait for next check
                await asyncio.sleep(self.check_interval_minutes * 60)
                
            except asyncio.CancelledError:
                logger.info("Timeout handler cancelled")
                break
            except Exception as e:
                logger.error(f"Error in timeout check loop: {e}")
                # Wait a bit before retrying
                await asyncio.sleep(60)
    
    async def start(self):
        """Start the timeout handler"""
        if self.is_running:
            logger.warning("Timeout handler is already running")
            return
        
        self.is_running = True
        self._task = asyncio.create_task(self._timeout_check_loop())
        logger.info("Timeout handler started")
    
    async def stop(self):
        """Stop the timeout handler"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        logger.info("Timeout handler stopped")
    
    def get_timeout_info(self, transaction_id: int) -> Optional[dict]:
        """Get timeout information for a transaction
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            Dictionary with timeout info or None
        """
        tx = self.db.get_transaction_by_id(transaction_id)
        if not tx:
            return None
        
        timeout_at = datetime.fromisoformat(tx['timeout_at'])
        now = datetime.now()
        
        time_remaining = timeout_at - now
        minutes_remaining = int(time_remaining.total_seconds() / 60)
        is_timed_out = minutes_remaining <= 0 and tx['status'] == 'pending'
        
        return {
            'transaction_id': transaction_id,
            'timeout_at': tx['timeout_at'],
            'minutes_remaining': max(0, minutes_remaining),
            'is_timed_out': is_timed_out,
            'status': tx['status']
        }


async def notify_admin_pending_payment(bot_application, admin_ids: list, transaction: dict):
    """Notify admins about a new pending payment
    
    Args:
        bot_application: Telegram bot application
        admin_ids: List of admin user IDs
        transaction: Transaction dictionary
    """
    if not bot_application or not admin_ids:
        return
    
    message = (
        f"🔔 **New Payment Transaction**\n\n"
        f"Transaction ID: #{transaction['id']}\n"
        f"User ID: {transaction['user_id']}\n"
        f"💰 Amount: {transaction['amount']:.8f} {transaction['currency']}\n"
        f"💵 USD: ${transaction.get('usd_equivalent', 0):.2f}\n"
        f"📅 Created: {transaction['created_at'][:19]}\n"
        f"⏰ Timeout: {transaction['timeout_at'][:19]}\n\n"
        f"Waiting for user to send payment..."
    )
    
    for admin_id in admin_ids:
        try:
            await bot_application.bot.send_message(
                chat_id=admin_id,
                text=message,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error notifying admin {admin_id}: {e}")
