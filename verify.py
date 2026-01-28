#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration verification script
"""

import os
import sys

def verify_config():
    """Verify configuration file"""
    print("="*60)
    print("Telegram Gift Card Bot - Configuration Verification")
    print("="*60)
    print()
    
    # Check if config.py exists
    if not os.path.exists('config.py'):
        print("❌ config.py not found!")
        print("\nPlease create config.py from config.example.py:")
        print("   cp config.example.py config.py")
        print("   nano config.py  # Edit and add your bot token")
        return False
    
    print("✅ config.py found")
    
    # Load config
    try:
        from config import BOT_TOKEN, CRYPTO_WALLETS, GIFT_CARDS
        print("✅ Configuration loaded successfully")
    except ImportError as e:
        print(f"❌ Error importing configuration: {e}")
        return False
    except FileNotFoundError as e:
        print(f"❌ Configuration file not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False
    
    # Verify bot token
    print("\n" + "-"*60)
    print("Bot Token Check")
    print("-"*60)
    if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("⚠️  Bot token is not set!")
        print("   Please get a token from @BotFather on Telegram")
        print("   and update BOT_TOKEN in config.py")
    else:
        print(f"✅ Bot token is set (length: {len(BOT_TOKEN)})")
    
    # Verify crypto wallets
    print("\n" + "-"*60)
    print("Cryptocurrency Wallets")
    print("-"*60)
    for crypto, address in CRYPTO_WALLETS.items():
        status = "✅" if address else "❌"
        print(f"{status} {crypto.upper()}: {address}")
    
    # Verify gift cards
    print("\n" + "-"*60)
    print("Gift Cards Configuration")
    print("-"*60)
    print(f"Total gift cards: {len(GIFT_CARDS)}")
    for card_id, card_info in GIFT_CARDS.items():
        print(f"\n  {card_info['name']}")
        print(f"    Amount: ${card_info['amount']:.2f}")
        print(f"    Image: {card_info['image_path']}")
        
        # Check if image exists
        if os.path.exists(card_info['image_path']):
            print(f"    Status: ✅ Image found")
        else:
            print(f"    Status: ⚠️  Image not found")
    
    # Check gift_cards directory
    print("\n" + "-"*60)
    print("Gift Cards Directory")
    print("-"*60)
    if os.path.exists('gift_cards'):
        print("✅ gift_cards directory exists")
        images = [f for f in os.listdir('gift_cards') if f.endswith(('.jpg', '.jpeg', '.png'))]
        print(f"   Found {len(images)} image(s): {', '.join(images) if images else 'none'}")
    else:
        print("⚠️  gift_cards directory not found")
        print("   Creating it now...")
        os.makedirs('gift_cards', exist_ok=True)
        print("✅ gift_cards directory created")
    
    # Summary
    print("\n" + "="*60)
    print("Setup Status Summary")
    print("="*60)
    
    checks = []
    checks.append(("Configuration file", True))
    checks.append(("Bot token", BOT_TOKEN and BOT_TOKEN != 'YOUR_BOT_TOKEN_HERE'))
    checks.append(("Crypto wallets", len(CRYPTO_WALLETS) > 0))
    checks.append(("Gift cards", len(GIFT_CARDS) > 0))
    checks.append(("Gift cards directory", os.path.exists('gift_cards')))
    
    for check_name, status in checks:
        icon = "✅" if status else "⚠️ "
        print(f"{icon} {check_name}")
    
    # Next steps
    print("\n" + "="*60)
    print("Next Steps")
    print("="*60)
    
    steps = []
    if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        steps.append("Get a bot token from @BotFather on Telegram")
        steps.append("Update BOT_TOKEN in config.py")
    
    steps.append("Add your cryptocurrency wallet addresses to config.py")
    steps.append("Add gift card images to gift_cards/ directory")
    steps.append("Install dependencies: pip install -r requirements.txt")
    steps.append("Run the bot: python3 bot.py")
    
    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")
    
    print("\nFor help: python3 admin.py help")
    print()
    
    return True

if __name__ == '__main__':
    try:
        verify_config()
    except KeyboardInterrupt:
        print("\n\nAborted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
