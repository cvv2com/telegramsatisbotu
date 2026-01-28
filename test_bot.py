#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script to verify bot functionality
"""

import sys
import sqlite3
import os

def test_database():
    """Test database initialization"""
    print("Testing database initialization...")
    
    # Import database functions
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from bot import init_db, create_or_get_user, get_user_balance, update_balance
    
    # Remove existing test database
    if os.path.exists('test_bot.db'):
        os.remove('test_bot.db')
    
    # Override database name for testing
    import bot
    original_connect = sqlite3.connect
    
    def test_connect(db_name):
        return original_connect('test_bot.db')
    
    sqlite3.connect = test_connect
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    # Test user creation
    test_user_id = 123456789
    create_or_get_user(test_user_id, "test_user")
    print("✅ User created")
    
    # Test balance check
    balance = get_user_balance(test_user_id)
    assert balance == 0.0, "New user should have 0 balance"
    print(f"✅ Balance check: ${balance:.2f}")
    
    # Test balance update
    update_balance(test_user_id, 100.0, 'deposit', 'Test deposit')
    new_balance = get_user_balance(test_user_id)
    assert new_balance == 100.0, "Balance should be 100.0 after deposit"
    print(f"✅ Balance update: ${new_balance:.2f}")
    
    # Test purchase
    update_balance(test_user_id, 50.0, 'purchase', 'Test purchase')
    final_balance = get_user_balance(test_user_id)
    assert final_balance == 50.0, "Balance should be 50.0 after purchase"
    print(f"✅ Purchase test: ${final_balance:.2f}")
    
    # Cleanup
    os.remove('test_bot.db')
    sqlite3.connect = original_connect
    
    print("\n✅ All database tests passed!")

def test_config():
    """Test configuration file"""
    print("\nTesting configuration...")
    
    try:
        from config import BOT_TOKEN, CRYPTO_WALLETS, GIFT_CARDS
        
        print(f"✅ Config loaded")
        print(f"   - Bot token: {'SET' if BOT_TOKEN and BOT_TOKEN != 'YOUR_BOT_TOKEN_HERE' else 'NOT SET'}")
        print(f"   - Crypto wallets: {len(CRYPTO_WALLETS)} configured")
        print(f"   - Gift cards: {len(GIFT_CARDS)} configured")
        
        if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            print("\n⚠️  Warning: Please set your bot token in config.py")
        
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    return True

def main():
    print("="*50)
    print("Telegram Gift Card Bot - Test Suite")
    print("="*50)
    print()
    
    try:
        # Test config
        if not test_config():
            return
        
        # Test database
        test_database()
        
        print("\n" + "="*50)
        print("✅ All tests passed!")
        print("="*50)
        print("\nYou can now run the bot with: python3 bot.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
