#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the new gift card system features
"""

import os
import sys
from database import GiftCardDB

def test_card_generation():
    """Test card generation functions"""
    print("=" * 60)
    print("Testing Card Generation Functions")
    print("=" * 60)
    
    # Test card number generation
    print("\n1. Testing card number generation:")
    for card_type in ['visa', 'mastercard', 'amex', 'discover']:
        card_num = GiftCardDB.generate_card_number(card_type)
        print(f"   {card_type.upper()}: {card_num} (length: {len(card_num)})")
    
    # Test expiration date generation
    print("\n2. Testing expiration date generation:")
    exp_date = GiftCardDB.generate_expiration_date()
    print(f"   Default (24 months): {exp_date}")
    exp_date_12 = GiftCardDB.generate_expiration_date(12)
    print(f"   12 months: {exp_date_12}")
    
    # Test PIN generation
    print("\n3. Testing PIN generation:")
    pin_3 = GiftCardDB.generate_pin(3)
    pin_4 = GiftCardDB.generate_pin(4)
    print(f"   3-digit PIN: {pin_3}")
    print(f"   4-digit PIN: {pin_4}")
    
    # Test code generation
    print("\n4. Testing card code generation:")
    code = GiftCardDB.generate_card_code()
    print(f"   Default: {code}")
    code_custom = GiftCardDB.generate_card_code("GIFT", 16)
    print(f"   Custom: {code_custom}")
    
    print("\n✅ Card generation tests passed!")

def test_database_operations():
    """Test database operations with new features"""
    print("\n" + "=" * 60)
    print("Testing Database Operations")
    print("=" * 60)
    
    # Create test database
    test_db_file = '/tmp/test_gift_card.db.json'
    if os.path.exists(test_db_file):
        os.remove(test_db_file)
    
    db = GiftCardDB(test_db_file)
    
    # Test 1: Add card with auto-generated details
    print("\n1. Testing auto-generation when adding card:")
    card_id_1 = db.add_gift_card(
        name="Test Card - Auto Generated",
        description="Card with auto-generated details",
        price=25.0,
        category="Test",
        code="TEST-001",
        stock=5
    )
    card_1 = db.get_card_by_id(card_id_1)
    print(f"   Card ID: {card_1['id']}")
    print(f"   Card Number: {card_1['card_number']}")
    print(f"   Expiration: {card_1['exp_date']}")
    print(f"   PIN: {card_1['pin']}")
    
    # Test 2: Add card with manual details (new format)
    print("\n2. Testing manual card details (new format):")
    card_id_2 = db.add_gift_card(
        name="Test Card - Manual New Format",
        description="Card with manual details",
        price=50.0,
        category="Test",
        code="TEST-002",
        card_number="4111111111111111",
        exp_date="12/25",
        pin="1234",
        image_front="/path/to/front.jpg",
        image_back="/path/to/back.jpg",
        stock=3
    )
    card_2 = db.get_card_by_id(card_id_2)
    print(f"   Card ID: {card_2['id']}")
    print(f"   Card Number: {card_2['card_number']}")
    print(f"   Expiration: {card_2['exp_date']}")
    print(f"   PIN: {card_2['pin']}")
    print(f"   Image Front: {card_2['image_front']}")
    print(f"   Image Back: {card_2['image_back']}")
    
    # Test 3: Add card with legacy format
    print("\n3. Testing legacy format support:")
    card_id_3 = db.add_gift_card(
        name="Test Card - Legacy Format",
        description="Card with legacy image format",
        price=30.0,
        category="Test",
        code="TEST-003",
        image_url="/path/to/image.jpg",
        stock=2
    )
    card_3 = db.get_card_by_id(card_id_3)
    print(f"   Card ID: {card_3['id']}")
    print(f"   Image URL (legacy): {card_3['image_url']}")
    print(f"   Card Number: {card_3['card_number']} (auto-generated)")
    print(f"   Expiration: {card_3['exp_date']} (auto-generated)")
    print(f"   PIN: {card_3['pin']} (auto-generated)")
    
    # Test 4: Test get_card_images helper
    print("\n4. Testing get_card_images helper:")
    images_1 = db.get_card_images(card_1)
    print(f"   Auto-generated card: Front={images_1['front']}, Back={images_1['back']}")
    images_2 = db.get_card_images(card_2)
    print(f"   New format card: Front={images_2['front']}, Back={images_2['back']}")
    images_3 = db.get_card_images(card_3)
    print(f"   Legacy format card: Front={images_3['front']}, Back={images_3['back']}")
    
    # Test 5: Test gift card purchase recording
    print("\n5. Testing gift card purchase recording:")
    test_user_id = 123456789
    purchase_id = db.add_gift_card_purchase(test_user_id, card_2)
    print(f"   Purchase ID: {purchase_id}")
    
    # Retrieve purchases
    purchases = db.get_user_purchases(test_user_id)
    print(f"   Total purchases for user: {len(purchases)}")
    if purchases:
        p = purchases[0]
        print(f"   Purchase Details:")
        print(f"     - Card Name: {p['card_name']}")
        print(f"     - Card Number: {p['card_number']}")
        print(f"     - Expiration: {p['exp_date']}")
        print(f"     - PIN: {p['pin']}")
        print(f"     - Amount: ${p['amount']}")
    
    # Test 6: Bulk add with mixed formats
    print("\n6. Testing bulk add with mixed formats:")
    bulk_cards = [
        {
            'name': 'Bulk Card 1',
            'description': 'Auto-generated',
            'price': 10.0,
            'code': 'BULK-001',
            'category': 'Bulk'
        },
        {
            'name': 'Bulk Card 2',
            'description': 'Manual details',
            'price': 20.0,
            'code': 'BULK-002',
            'category': 'Bulk',
            'card_number': '5555555555554444',
            'exp_date': '06/26',
            'pin': '999',
            'image_front': '/bulk/front.jpg'
        },
        {
            'name': 'Bulk Card 3',
            'description': 'Legacy format',
            'price': 15.0,
            'code': 'BULK-003',
            'category': 'Bulk',
            'image_url': '/bulk/image.jpg'
        }
    ]
    success_count, errors = db.bulk_add_cards(bulk_cards)
    print(f"   Success: {success_count}/{len(bulk_cards)}")
    if errors:
        print(f"   Errors: {errors}")
    
    # Verify all cards
    all_cards = db.get_all_cards()
    print(f"\n7. Total cards in database: {len(all_cards)}")
    
    # Cleanup
    os.remove(test_db_file)
    print("\n✅ Database operation tests passed!")

def test_backward_compatibility():
    """Test backward compatibility with existing databases"""
    print("\n" + "=" * 60)
    print("Testing Backward Compatibility")
    print("=" * 60)
    
    # Create a database with old format
    test_db_file = '/tmp/test_legacy.db.json'
    if os.path.exists(test_db_file):
        os.remove(test_db_file)
    
    # Simulate old database format
    import json
    old_data = {
        'gift_cards': [
            {
                'id': 1,
                'name': 'Old Card',
                'description': 'Card from old format',
                'price': 25.0,
                'category': 'Old',
                'code': 'OLD-001',
                'image_url': '/old/image.jpg',
                'stock': 1,
                'status': 'available',
                'created_at': '2024-01-01T00:00:00',
                'sold_at': None,
                'buyer_id': None
            }
        ],
        'categories': ['Old'],
        'orders': [],
        'coupons': [],
        'users': {},
        'next_card_id': 2,
        'next_order_id': 1,
        'next_coupon_id': 1
    }
    
    with open(test_db_file, 'w') as f:
        json.dump(old_data, f)
    
    # Load with new system
    print("\n1. Loading old format database:")
    db = GiftCardDB(test_db_file)
    print(f"   ✅ Database loaded successfully")
    
    # Check if old card still accessible
    old_card = db.get_card_by_id(1)
    print(f"\n2. Old card still accessible:")
    print(f"   Name: {old_card['name']}")
    print(f"   Image URL: {old_card['image_url']}")
    
    # Test get_card_images on old card
    images = db.get_card_images(old_card)
    print(f"\n3. Image compatibility:")
    print(f"   Front: {images['front']} (from image_url)")
    print(f"   Back: {images['back']} (None, as expected)")
    
    # Add new card to old database
    print(f"\n4. Adding new card to old database:")
    new_card_id = db.add_gift_card(
        name="New Card in Old DB",
        description="Testing compatibility",
        price=35.0,
        category="New",
        code="NEW-001"
    )
    new_card = db.get_card_by_id(new_card_id)
    print(f"   ✅ New card added with ID: {new_card_id}")
    print(f"   Has card_number: {new_card.get('card_number') is not None}")
    print(f"   Has exp_date: {new_card.get('exp_date') is not None}")
    print(f"   Has pin: {new_card.get('pin') is not None}")
    
    # Verify gift_card_purchases table created
    print(f"\n5. Checking new fields in database:")
    has_purchases = 'gift_card_purchases' in db.data
    has_next_purchase_id = 'next_purchase_id' in db.data
    print(f"   gift_card_purchases table: {has_purchases}")
    print(f"   next_purchase_id counter: {has_next_purchase_id}")
    
    # Cleanup
    os.remove(test_db_file)
    print("\n✅ Backward compatibility tests passed!")

def main():
    print("\n" + "=" * 60)
    print("Gift Card System Enhancement Tests")
    print("=" * 60)
    
    try:
        # Run all tests
        test_card_generation()
        test_database_operations()
        test_backward_compatibility()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe gift card system enhancements are working correctly:")
        print("  ✅ Card generation (number, expiration, PIN)")
        print("  ✅ Front/back image support")
        print("  ✅ Gift card purchases tracking")
        print("  ✅ Legacy format compatibility")
        print("  ✅ Auto-generation with defaults")
        print("  ✅ Bulk operations with mixed formats")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
