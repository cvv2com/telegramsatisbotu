#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for gift card enhancements
Tests the new numeric details and front/back image support
"""

import sys
import os

def test_config_structure():
    """Test that config example has the new structure"""
    print("Testing config.example.py structure...")
    
    # Import config example
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Read config.example.py
    with open('config.example.py', 'r') as f:
        config_content = f.read()
    
    # Check for new fields
    checks = [
        ('card_number', 'Card number field'),
        ('exp_date', 'Expiration date field'),
        ('pin', 'PIN field'),
        ('image_front', 'Front image field'),
        ('image_back', 'Back image field'),
        ('5543554475829811', 'Example 16-digit card number'),
        ('02/27', 'Example expiration date'),
        ('097', 'Example PIN'),
    ]
    
    results = []
    for check_str, desc in checks:
        if check_str in config_content:
            print(f"  ✅ {desc} found")
            results.append(True)
        else:
            print(f"  ❌ {desc} missing")
            results.append(False)
    
    return all(results)

def test_database_structure():
    """Test that bot.py has the new database table"""
    print("\nTesting database structure in bot.py...")
    
    with open('bot.py', 'r') as f:
        bot_content = f.read()
    
    # Check for gift card purchases table
    checks = [
        ('gift_card_purchases', 'Gift card purchases table'),
        ('card_number TEXT', 'Card number column'),
        ('exp_date TEXT', 'Expiration date column'),
        ('pin TEXT', 'PIN column'),
    ]
    
    results = []
    for check_str, desc in checks:
        if check_str in bot_content:
            print(f"  ✅ {desc} found")
            results.append(True)
        else:
            print(f"  ❌ {desc} missing")
            results.append(False)
    
    return all(results)

def test_purchase_function():
    """Test that purchase function handles new fields"""
    print("\nTesting purchase function updates...")
    
    with open('bot.py', 'r') as f:
        bot_content = f.read()
    
    # Check for new functionality
    checks = [
        ("card_info.get('card_number')", 'Card number handling'),
        ("card_info.get('exp_date')", 'Expiration date handling'),
        ("card_info.get('pin')", 'PIN handling'),
        ("card_info.get('image_front')", 'Front image handling'),
        ("card_info.get('image_back')", 'Back image handling'),
        ('💳 Kart Numarası', 'Card number display'),
        ('📅 Son Kullanma Tarihi', 'Expiry date display'),
        ('🔐 PIN', 'PIN display'),
        ('🔙 Gift Card Arka Yüz', 'Back image caption'),
    ]
    
    results = []
    for check_str, desc in checks:
        if check_str in bot_content:
            print(f"  ✅ {desc} found")
            results.append(True)
        else:
            print(f"  ❌ {desc} missing")
            results.append(False)
    
    return all(results)

def test_backward_compatibility():
    """Test backward compatibility with old format"""
    print("\nTesting backward compatibility...")
    
    with open('config.example.py', 'r') as f:
        config_content = f.read()
    
    with open('bot.py', 'r') as f:
        bot_content = f.read()
    
    # Check that old format is still supported
    checks = [
        ('image_path', 'Old image_path field in config'),
        ("card_info.get('image_front') or card_info.get('image_path')", 'Fallback to image_path in bot'),
    ]
    
    results = []
    for check_str, desc in checks:
        if check_str in config_content or check_str in bot_content:
            print(f"  ✅ {desc} supported")
            results.append(True)
        else:
            print(f"  ❌ {desc} missing")
            results.append(False)
    
    return all(results)

def test_documentation():
    """Test that documentation is updated"""
    print("\nTesting documentation updates...")
    
    with open('gift_cards/README.md', 'r') as f:
        readme_content = f.read()
    
    checks = [
        ('card_number', 'Card number documented'),
        ('exp_date', 'Expiration date documented'),
        ('pin', 'PIN documented'),
        ('image_front', 'Front image documented'),
        ('image_back', 'Back image documented'),
        ('16 haneli', 'Turkish description'),
        ('Geriye Dönük Uyumluluk', 'Backward compatibility section'),
    ]
    
    results = []
    for check_str, desc in checks:
        if check_str in readme_content:
            print(f"  ✅ {desc} found")
            results.append(True)
        else:
            print(f"  ❌ {desc} missing")
            results.append(False)
    
    return all(results)

def main():
    print("="*60)
    print("Gift Card Enhancement Test Suite")
    print("="*60)
    print()
    
    tests = [
        ("Config Structure", test_config_structure),
        ("Database Structure", test_database_structure),
        ("Purchase Function", test_purchase_function),
        ("Backward Compatibility", test_backward_compatibility),
        ("Documentation", test_documentation),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        try:
            result = test_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"  ❌ Test failed with error: {e}")
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ All tests passed!")
        print("\nNew features:")
        print("  • 16-digit card numbers")
        print("  • Expiration dates (MM/YY)")
        print("  • PIN codes")
        print("  • Front and back images")
        print("  • Database tracking")
        print("  • Backward compatible with old format")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
