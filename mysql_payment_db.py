#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL Database Handler for Payment Transactions
Manages payment data in MySQL database
"""

import logging
import mysql.connector
from mysql.connector import Error, pooling
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class MySQLPaymentDB:
    """MySQL Database Handler for Payment Transactions"""
    
    def __init__(self, config: Dict):
        """Initialize MySQL connection pool
        
        Args:
            config: MySQL configuration dictionary with host, user, password, database
        """
        self.config = config
        self.pool = None
        
        try:
            # Create connection pool
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="payment_pool",
                pool_size=5,
                pool_reset_session=True,
                host=config.get('host', 'localhost'),
                port=config.get('port', 3306),
                database=config.get('database'),
                user=config.get('user'),
                password=config.get('password'),
                autocommit=False
            )
            logger.info("MySQL connection pool created successfully")
        except Error as e:
            logger.error(f"Error creating MySQL connection pool: {e}")
            self.pool = None
    
    @contextmanager
    def get_connection(self):
        """Get database connection from pool (context manager)
        
        Yields:
            MySQL connection object
        """
        conn = None
        try:
            if self.pool:
                conn = self.pool.get_connection()
                yield conn
            else:
                # Fallback: create direct connection if pool not available
                conn = mysql.connector.connect(**self.config)
                yield conn
        except Error as e:
            logger.error(f"Database connection error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn and conn.is_connected():
                conn.close()
    
    def initialize_database(self) -> bool:
        """Create database tables if they don't exist
        
        Returns:
            True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create cryptomus_payments table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cryptomus_payments (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        order_id VARCHAR(255) NOT NULL UNIQUE,
                        payment_uuid VARCHAR(255) UNIQUE,
                        amount DECIMAL(20, 8) NOT NULL,
                        currency VARCHAR(10) NOT NULL,
                        network VARCHAR(50),
                        payment_amount DECIMAL(20, 8),
                        payer_amount DECIMAL(20, 8),
                        payer_currency VARCHAR(10),
                        address VARCHAR(255),
                        from_address VARCHAR(255),
                        txid VARCHAR(255),
                        status VARCHAR(50) NOT NULL DEFAULT 'pending',
                        payment_status VARCHAR(50),
                        is_final BOOLEAN DEFAULT FALSE,
                        payment_url TEXT,
                        expired_at DATETIME,
                        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        confirmed_at DATETIME,
                        additional_data TEXT,
                        INDEX idx_user_id (user_id),
                        INDEX idx_order_id (order_id),
                        INDEX idx_payment_uuid (payment_uuid),
                        INDEX idx_status (status),
                        INDEX idx_created_at (created_at)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                
                # Create payment_notifications table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS payment_notifications (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        payment_id INT NOT NULL,
                        user_id BIGINT NOT NULL,
                        notification_type VARCHAR(50) NOT NULL,
                        message TEXT NOT NULL,
                        sent_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        telegram_message_id BIGINT,
                        status VARCHAR(20) NOT NULL DEFAULT 'sent',
                        INDEX idx_payment_id (payment_id),
                        INDEX idx_user_id (user_id),
                        INDEX idx_sent_at (sent_at),
                        FOREIGN KEY (payment_id) REFERENCES cryptomus_payments(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                
                # Create user_balances table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_balances (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id BIGINT NOT NULL UNIQUE,
                        balance DECIMAL(20, 2) NOT NULL DEFAULT 0.00,
                        total_deposited DECIMAL(20, 2) NOT NULL DEFAULT 0.00,
                        total_spent DECIMAL(20, 2) NOT NULL DEFAULT 0.00,
                        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_user_id (user_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                
                conn.commit()
                logger.info("Database tables created successfully")
                return True
                
        except Error as e:
            logger.error(f"Error initializing database: {e}")
            return False
    
    def create_payment(self, user_id: int, order_id: str, amount: float,
                      currency: str, network: str = None) -> Tuple[bool, Optional[int], Optional[str]]:
        """Create a new payment record
        
        Args:
            user_id: Telegram user ID
            order_id: Unique order identifier
            amount: Payment amount in USD
            currency: Cryptocurrency (BTC, ETH, USDT)
            network: Blockchain network (optional)
            
        Returns:
            (success, payment_id, error_message)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    INSERT INTO cryptomus_payments 
                    (user_id, order_id, amount, currency, network, status)
                    VALUES (%s, %s, %s, %s, %s, 'pending')
                """
                
                cursor.execute(query, (user_id, order_id, amount, currency, network))
                payment_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Payment created: id={payment_id}, order_id={order_id}")
                return True, payment_id, None
                
        except Error as e:
            logger.error(f"Error creating payment: {e}")
            return False, None, str(e)
    
    def update_payment_from_cryptomus(self, order_id: str, payment_data: Dict) -> Tuple[bool, Optional[str]]:
        """Update payment with data from Cryptomus webhook
        
        Args:
            order_id: Order ID
            payment_data: Payment data from Cryptomus webhook
            
        Returns:
            (success, error_message)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Prepare update data
                status = payment_data.get('status', 'pending')
                is_final = payment_data.get('is_final', False)
                
                query = """
                    UPDATE cryptomus_payments SET
                        payment_uuid = %s,
                        payment_amount = %s,
                        payer_amount = %s,
                        payer_currency = %s,
                        address = %s,
                        from_address = %s,
                        txid = %s,
                        status = %s,
                        payment_status = %s,
                        is_final = %s,
                        payment_url = %s,
                        expired_at = %s,
                        updated_at = NOW()
                    WHERE order_id = %s
                """
                
                values = (
                    payment_data.get('uuid'),
                    payment_data.get('payment_amount'),
                    payment_data.get('payer_amount'),
                    payment_data.get('payer_currency'),
                    payment_data.get('address'),
                    payment_data.get('from_address'),
                    payment_data.get('txid'),
                    status,
                    payment_data.get('payment_status'),
                    is_final,
                    payment_data.get('url'),
                    payment_data.get('expired_at'),
                    order_id
                )
                
                cursor.execute(query, values)
                
                # If payment is successful, update confirmed_at
                if status in ['paid', 'paid_over']:
                    cursor.execute(
                        "UPDATE cryptomus_payments SET confirmed_at = NOW() WHERE order_id = %s AND confirmed_at IS NULL",
                        (order_id,)
                    )
                
                conn.commit()
                
                logger.info(f"Payment updated: order_id={order_id}, status={status}")
                return True, None
                
        except Error as e:
            logger.error(f"Error updating payment: {e}")
            return False, str(e)
    
    def get_payment_by_order_id(self, order_id: str) -> Optional[Dict]:
        """Get payment by order ID
        
        Args:
            order_id: Order ID
            
        Returns:
            Payment dictionary or None
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                query = "SELECT * FROM cryptomus_payments WHERE order_id = %s"
                cursor.execute(query, (order_id,))
                
                result = cursor.fetchone()
                return result
                
        except Error as e:
            logger.error(f"Error getting payment: {e}")
            return None
    
    def get_user_payments(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's payment history
        
        Args:
            user_id: Telegram user ID
            limit: Maximum number of records to return
            
        Returns:
            List of payment dictionaries
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                query = """
                    SELECT * FROM cryptomus_payments 
                    WHERE user_id = %s 
                    ORDER BY created_at DESC 
                    LIMIT %s
                """
                cursor.execute(query, (user_id, limit))
                
                results = cursor.fetchall()
                return results
                
        except Error as e:
            logger.error(f"Error getting user payments: {e}")
            return []
    
    def get_all_payments(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get all payments (for admin panel)
        
        Args:
            limit: Maximum number of records
            offset: Offset for pagination
            
        Returns:
            List of payment dictionaries
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                query = """
                    SELECT * FROM cryptomus_payments 
                    ORDER BY created_at DESC 
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (limit, offset))
                
                results = cursor.fetchall()
                return results
                
        except Error as e:
            logger.error(f"Error getting all payments: {e}")
            return []
    
    def add_notification(self, payment_id: int, user_id: int, notification_type: str,
                        message: str, telegram_message_id: int = None) -> bool:
        """Add payment notification record
        
        Args:
            payment_id: Payment ID
            user_id: Telegram user ID
            notification_type: Type of notification
            message: Notification message
            telegram_message_id: Telegram message ID (optional)
            
        Returns:
            True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    INSERT INTO payment_notifications 
                    (payment_id, user_id, notification_type, message, telegram_message_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
                
                cursor.execute(query, (payment_id, user_id, notification_type, message, telegram_message_id))
                conn.commit()
                
                return True
                
        except Error as e:
            logger.error(f"Error adding notification: {e}")
            return False
    
    def ensure_user_balance(self, user_id: int) -> bool:
        """Ensure user balance record exists
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if record exists or was created
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if user balance exists
                query = "SELECT balance FROM user_balances WHERE user_id = %s"
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                
                if not result:
                    # Create new balance record
                    cursor.execute(
                        "INSERT INTO user_balances (user_id, balance) VALUES (%s, 0.00)",
                        (user_id,)
                    )
                    conn.commit()
                
                return True
                
        except Error as e:
            logger.error(f"Error ensuring user balance: {e}")
            return False
    
    def get_user_balance(self, user_id: int) -> float:
        """Get user's current balance
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Balance amount
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT balance FROM user_balances WHERE user_id = %s"
                cursor.execute(query, (user_id,))
                
                result = cursor.fetchone()
                if result:
                    return float(result[0])
                else:
                    # Create new balance record if it doesn't exist
                    self.ensure_user_balance(user_id)
                    return 0.0
                
        except Error as e:
            logger.error(f"Error getting user balance: {e}")
            return 0.0
    
    def update_user_balance(self, user_id: int, amount: float, operation: str = 'add') -> bool:
        """Update user's balance
        
        Args:
            user_id: Telegram user ID
            amount: Amount to add or subtract
            operation: 'add' or 'subtract'
            
        Returns:
            True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Ensure user balance record exists
                self.ensure_user_balance(user_id)
                
                if operation == 'add':
                    query = """
                        UPDATE user_balances 
                        SET balance = balance + %s, 
                            total_deposited = total_deposited + %s,
                            updated_at = NOW()
                        WHERE user_id = %s
                    """
                    cursor.execute(query, (amount, amount, user_id))
                else:  # subtract
                    query = """
                        UPDATE user_balances 
                        SET balance = balance - %s,
                            total_spent = total_spent + %s,
                            updated_at = NOW()
                        WHERE user_id = %s AND balance >= %s
                    """
                    cursor.execute(query, (amount, amount, user_id, amount))
                    
                    if cursor.rowcount == 0:
                        logger.warning(f"Insufficient balance for user {user_id}")
                        return False
                
                conn.commit()
                return True
                
        except Error as e:
            logger.error(f"Error updating user balance: {e}")
            return False


if __name__ == "__main__":
    # Test database initialization
    import os
    from dotenv import load_dotenv
    from config import MYSQL_CONFIG
    
    load_dotenv()
    
    print("Testing MySQL database initialization...")
    db = MySQLPaymentDB(MYSQL_CONFIG)
    
    if db.pool:
        print("✅ Connection pool created")
        
        if db.initialize_database():
            print("✅ Database tables created")
        else:
            print("❌ Failed to create tables")
    else:
        print("❌ Failed to create connection pool")
        print("Make sure MySQL is running and credentials are correct")
