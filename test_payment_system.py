#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the crypto payment system
"""

import os
import sys
import tempfile
from datetime import datetime, timedelta
from database import GiftCardDB
from crypto_utils import (
    validate_btc_address,
    validate_eth_address,
    validate_usdt_address,
    validate_ltc_address,
    validate_tx_hash,
    format_crypto_amount,
    parse_crypto_amount,
    calculate_crypto_amount,
    calculate_usd_amount
)
from payment_handler import PaymentHandler

def test_crypto_utils():
    """Test crypto utility functions"""
    print("=" * 70)
    print("Testing Crypto Utility Functions")
    print("=" * 70)
    
    # Test BTC address validation
    print("\n1. Testing BTC address validation:")
    valid_btc = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    invalid_btc = "invalid_address"
    print(f"   Valid BTC: {valid_btc} -> {validate_btc_address(valid_btc)}")
    print(f"   Invalid BTC: {invalid_btc} -> {validate_btc_address(invalid_btc)}")
    assert validate_btc_address(valid_btc) == True
    assert validate_btc_address(invalid_btc) == False
    
    # Test ETH address validation
    print("\n2. Testing ETH address validation:")
    valid_eth = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
    invalid_eth = "0xinvalid"
    print(f"   Valid ETH: {valid_eth} -> {validate_eth_address(valid_eth)}")
    print(f"   Invalid ETH: {invalid_eth} -> {validate_eth_address(invalid_eth)}")
    assert validate_eth_address(valid_eth) == True
    assert validate_eth_address(invalid_eth) == False
    
    # Test USDT address validation
    print("\n3. Testing USDT address validation:")
    valid_usdt = "TXj9KpLuTdU8kqvU9ZnQxQHDJVPH2NFq8K"
    invalid_usdt = "invalid_usdt"
    print(f"   Valid USDT (TRC20): {valid_usdt} -> {validate_usdt_address(valid_usdt)}")
    print(f"   Invalid USDT: {invalid_usdt} -> {validate_usdt_address(invalid_usdt)}")
    assert validate_usdt_address(valid_usdt) == True
    assert validate_usdt_address(invalid_usdt) == False
    
    # Test LTC address validation
    print("\n4. Testing LTC address validation:")
    valid_ltc = "LUWPbpM43E2p7ZSh8cyTBEkvpHmr3cB8Ez"
    invalid_ltc = "invalid_ltc"
    print(f"   Valid LTC: {valid_ltc} -> {validate_ltc_address(valid_ltc)}")
    print(f"   Invalid LTC: {invalid_ltc} -> {validate_ltc_address(invalid_ltc)}")
    assert validate_ltc_address(valid_ltc) == True
    assert validate_ltc_address(invalid_ltc) == False
    
    # Test TX hash validation
    print("\n5. Testing TX hash validation:")
    valid_btc_tx = "a" * 64
    invalid_btc_tx = "invalid"
    print(f"   Valid BTC TX: {valid_btc_tx[:16]}... -> {validate_tx_hash(valid_btc_tx, 'BTC')}")
    print(f"   Invalid BTC TX: {invalid_btc_tx} -> {validate_tx_hash(invalid_btc_tx, 'BTC')}")
    assert validate_tx_hash(valid_btc_tx, 'BTC') == True
    assert validate_tx_hash(invalid_btc_tx, 'BTC') == False
    
    # Test amount formatting
    print("\n6. Testing amount formatting:")
    btc_amount = 0.00123456
    formatted_btc = format_crypto_amount(btc_amount, 'BTC')
    print(f"   BTC: {btc_amount} -> {formatted_btc}")
    assert formatted_btc == "0.00123456"
    
    # Test amount parsing
    print("\n7. Testing amount parsing:")
    amount_str = "0.00123456"
    parsed = parse_crypto_amount(amount_str)
    print(f"   Parse: '{amount_str}' -> {parsed}")
    assert parsed == 0.00123456
    
    # Test crypto calculations
    print("\n8. Testing crypto calculations:")
    usd_amount = 100.0
    exchange_rate = 42500.0  # 1 BTC = $42,500
    crypto_amount = calculate_crypto_amount(usd_amount, exchange_rate)
    print(f"   ${usd_amount} at rate ${exchange_rate} = {crypto_amount:.8f} BTC")
    assert abs(crypto_amount - 0.00235294) < 0.00000001
    
    usd_back = calculate_usd_amount(crypto_amount, exchange_rate)
    print(f"   {crypto_amount:.8f} BTC at rate ${exchange_rate} = ${usd_back:.2f}")
    assert abs(usd_back - usd_amount) < 0.01
    
    print("\n✅ Crypto utility tests passed!")

def test_database_payment_functions():
    """Test database payment functions"""
    print("\n" + "=" * 70)
    print("Testing Database Payment Functions")
    print("=" * 70)
    
    # Create test database
    test_db_file = tempfile.mktemp(suffix='.json')
    db = GiftCardDB(test_db_file)
    
    try:
        # Test 1: Create payment transaction
        print("\n1. Testing create_payment_transaction:")
        tx_id = db.create_payment_transaction(
            user_id=123456789,
            amount=0.00235294,
            currency='BTC',
            wallet_address='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            user_wallet='3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy',
            exchange_rate=42500.0,
            usd_equivalent=100.0,
            timeout_minutes=30,
            required_confirmations=3
        )
        print(f"   Created transaction ID: {tx_id}")
        assert tx_id == 1
        
        # Test 2: Get transaction by ID
        print("\n2. Testing get_transaction_by_id:")
        tx = db.get_transaction_by_id(tx_id)
        assert tx is not None
        assert tx['id'] == tx_id
        assert tx['user_id'] == 123456789
        assert tx['currency'] == 'BTC'
        assert tx['status'] == 'pending'
        print(f"   Found transaction: ID={tx['id']}, Status={tx['status']}, Amount={tx['amount']}")
        
        # Test 3: Update transaction status
        print("\n3. Testing update_transaction_status:")
        tx_hash = "a" * 64
        success = db.update_transaction_status(tx_id, 'pending', tx_hash=tx_hash, confirmations=1)
        assert success == True
        tx = db.get_transaction_by_id(tx_id)
        assert tx['tx_hash'] == tx_hash
        assert tx['confirmations'] == 1
        print(f"   Updated: TX Hash={tx['tx_hash'][:16]}..., Confirmations={tx['confirmations']}")
        
        # Test 4: Get pending transactions
        print("\n4. Testing get_pending_transactions:")
        pending = db.get_pending_transactions()
        assert len(pending) == 1
        assert pending[0]['id'] == tx_id
        print(f"   Found {len(pending)} pending transaction(s)")
        
        # Test 5: Confirm transaction
        print("\n5. Testing confirm_transaction:")
        success = db.confirm_transaction(tx_id, tx_hash, confirmations=3, credit_balance=True)
        assert success == True
        tx = db.get_transaction_by_id(tx_id)
        assert tx['status'] == 'confirmed'
        assert tx['confirmed_at'] is not None
        print(f"   Confirmed: Status={tx['status']}, Confirmed at={tx['confirmed_at'][:19]}")
        
        # Test 6: Check balance was credited
        print("\n6. Testing balance credit:")
        balance = db.get_user_balance(123456789)
        assert balance == 100.0
        print(f"   User balance after credit: ${balance:.2f}")
        
        # Test 7: Get user transactions
        print("\n7. Testing get_user_transactions:")
        user_txs = db.get_user_transactions(123456789)
        assert len(user_txs) == 1
        assert user_txs[0]['id'] == tx_id
        print(f"   Found {len(user_txs)} transaction(s) for user")
        
        # Test 8: Get transaction by hash
        print("\n8. Testing get_transaction_by_hash:")
        tx_by_hash = db.get_transaction_by_hash(tx_hash)
        assert tx_by_hash is not None
        assert tx_by_hash['id'] == tx_id
        print(f"   Found transaction by hash: ID={tx_by_hash['id']}")
        
        # Test 9: Create another transaction and test timeout
        print("\n9. Testing transaction timeout:")
        tx_id_2 = db.create_payment_transaction(
            user_id=987654321,
            amount=0.001,
            currency='BTC',
            wallet_address='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            exchange_rate=42500.0,
            usd_equivalent=42.5,
            timeout_minutes=0  # Immediate timeout
        )
        is_timeout = db.check_transaction_timeout(tx_id_2)
        assert is_timeout == True
        print(f"   Transaction #{tx_id_2} timeout check: {is_timeout}")
        
        # Test 10: Cancel payment
        print("\n10. Testing cancel_payment:")
        success = db.cancel_payment(tx_id_2, "Test cancellation")
        assert success == True
        tx_cancelled = db.get_transaction_by_id(tx_id_2)
        assert tx_cancelled['status'] == 'failed'
        print(f"   Cancelled transaction #{tx_id_2}: Status={tx_cancelled['status']}")
        
        # Test 11: Get payment stats
        print("\n11. Testing get_payment_stats:")
        stats = db.get_payment_stats()
        assert stats['total'] == 2
        assert stats['confirmed'] == 1
        assert stats['failed'] == 1
        assert stats['total_volume_usd'] == 100.0
        print(f"   Stats: Total={stats['total']}, Confirmed={stats['confirmed']}, "
              f"Failed={stats['failed']}, Volume=${stats['total_volume_usd']:.2f}")
        
        print("\n✅ Database payment function tests passed!")
        
    finally:
        # Cleanup
        if os.path.exists(test_db_file):
            os.remove(test_db_file)

def test_payment_handler():
    """Test payment handler"""
    print("\n" + "=" * 70)
    print("Testing Payment Handler")
    print("=" * 70)
    
    # Create test database
    test_db_file = tempfile.mktemp(suffix='.json')
    db = GiftCardDB(test_db_file)
    
    # Mock config
    config = {
        'CRYPTO_WALLETS': {
            'btc': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            'eth': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0'
        }
    }
    
    handler = PaymentHandler(db, config)
    
    try:
        # Test 1: Create payment
        print("\n1. Testing create_payment:")
        success, message, tx_id = handler.create_payment(
            user_id=123456789,
            usd_amount=100.0,
            currency='BTC',
            exchange_rate=42500.0
        )
        assert success == True
        assert tx_id is not None
        print(f"   Created payment: Success={success}, Message={message}, TX ID={tx_id}")
        
        # Test 2: Get payment instructions
        print("\n2. Testing get_payment_instructions:")
        instructions = handler.get_payment_instructions(tx_id)
        assert instructions is not None
        assert instructions['currency'] == 'BTC'
        assert instructions['usd_amount'] == 100.0
        print(f"   Instructions: Currency={instructions['currency']}, "
              f"Amount={instructions['crypto_amount_formatted']}, "
              f"Wallet={instructions['wallet_address'][:16]}...")
        
        # Test 3: Validate payment
        print("\n3. Testing validate_payment:")
        valid_hash = "a" * 64
        is_valid, msg = handler.validate_payment(valid_hash, 'BTC')
        assert is_valid == True
        print(f"   Validation: Valid={is_valid}, Message={msg}")
        
        # Test 4: Confirm payment
        print("\n4. Testing confirm_payment:")
        success, message = handler.confirm_payment(tx_id, valid_hash, confirmations=3)
        assert success == True
        print(f"   Confirmation: Success={success}, Message={message}")
        
        # Test 5: Get transaction status
        print("\n5. Testing get_transaction_status:")
        status = handler.get_transaction_status(tx_id)
        assert status is not None
        assert status['status'] == 'confirmed'
        print(f"   Status: {status['status']}, Amount={status['amount']:.8f} {status['currency']}")
        
        # Test 6: Format transaction message
        print("\n6. Testing format_transaction_message:")
        message = handler.format_transaction_message(tx_id)
        assert message is not None
        assert '✅' in message  # Confirmed emoji
        print(f"   Message length: {len(message)} characters")
        print(f"   First line: {message.split(chr(10))[0]}")
        
        # Test 7: Cancel payment
        print("\n7. Testing cancel_payment:")
        # Create another payment to cancel
        success, msg, tx_id_2 = handler.create_payment(
            user_id=123456789,
            usd_amount=50.0,
            currency='BTC',
            exchange_rate=42500.0
        )
        assert success == True
        
        success, msg = handler.cancel_payment(tx_id_2, "Test cancellation")
        assert success == True
        print(f"   Cancellation: Success={success}, Message={msg}")
        
        print("\n✅ Payment handler tests passed!")
        
    finally:
        # Cleanup
        if os.path.exists(test_db_file):
            os.remove(test_db_file)

def main():
    print("\n" + "=" * 70)
    print("Crypto Payment System Tests")
    print("=" * 70)
    
    try:
        # Run all tests
        test_crypto_utils()
        test_database_payment_functions()
        test_payment_handler()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\nThe crypto payment system is working correctly:")
        print("  ✅ Crypto utility functions (address/hash validation)")
        print("  ✅ Database payment transaction management")
        print("  ✅ Payment handler (creation, validation, confirmation)")
        print("  ✅ Transaction status tracking")
        print("  ✅ Balance crediting")
        print("  ✅ Timeout handling")
        print("  ✅ Payment cancellation")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: Assertion error")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
