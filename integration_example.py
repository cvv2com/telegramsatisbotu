#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Example for Gift Card System Enhancements

This file demonstrates how to integrate the new gift card features
into a Telegram bot or other application.
"""

from database import GiftCardDB
from typing import Optional

class GiftCardBot:
    """Example integration of gift card system with enhanced features"""
    
    def __init__(self, db_file: str = 'gift_cards.db.json'):
        self.db = GiftCardDB(db_file)
    
    def add_card_with_auto_generation(self, name: str, description: str, 
                                     price: float, category: str, stock: int = 1) -> dict:
        """
        Add a gift card with auto-generated details
        
        Example usage:
            bot.add_card_with_auto_generation(
                name="Steam $50",
                description="Gaming gift card",
                price=50.0,
                category="Gaming",
                stock=10
            )
        """
        # Auto-generate a unique code
        code = self.db.generate_card_code(prefix="STEAM", length=15)
        
        # Add card (card_number, exp_date, pin auto-generated)
        card_id = self.db.add_gift_card(
            name=name,
            description=description,
            price=price,
            category=category,
            code=code,
            stock=stock
        )
        
        return self.db.get_card_by_id(card_id)
    
    def add_card_with_manual_details(self, name: str, description: str,
                                    price: float, category: str,
                                    card_number: str, exp_date: str, pin: str,
                                    image_front: Optional[str] = None,
                                    image_back: Optional[str] = None,
                                    stock: int = 1) -> dict:
        """
        Add a gift card with manually specified details
        
        Example usage:
            bot.add_card_with_manual_details(
                name="Amazon $100",
                description="Shopping card",
                price=100.0,
                category="Shopping",
                card_number="4111111111111111",
                exp_date="12/25",
                pin="1234",
                image_front="images/amazon_front.jpg",
                image_back="images/amazon_back.jpg",
                stock=5
            )
        """
        code = self.db.generate_card_code(prefix="AMZ", length=12)
        
        card_id = self.db.add_gift_card(
            name=name,
            description=description,
            price=price,
            category=category,
            code=code,
            card_number=card_number,
            exp_date=exp_date,
            pin=pin,
            image_front=image_front,
            image_back=image_back,
            stock=stock
        )
        
        return self.db.get_card_by_id(card_id)
    
    def display_card_to_user(self, card: dict) -> str:
        """
        Format card information for display to user
        Handles both legacy and new image formats
        """
        # Get images (supports both formats)
        images = self.db.get_card_images(card)
        
        message = f"🎁 **{card['name']}**\n\n"
        message += f"📝 {card['description']}\n"
        message += f"💰 Price: ${card['price']:.2f}\n"
        message += f"📦 Stock: {card['stock']}\n\n"
        
        # Only show card details to buyer after purchase
        # These should be hidden/spoilered in Telegram
        if card.get('card_number'):
            message += f"💳 Card Number: ||{card['card_number']}||\n"
        if card.get('exp_date'):
            message += f"📅 Expires: ||{card['exp_date']}||\n"
        if card.get('pin'):
            message += f"🔢 PIN: ||{card['pin']}||\n"
        
        # Note which images are available
        if images['front']:
            message += f"\n🖼️ Front image available"
        if images['back']:
            message += f"\n🖼️ Back image available"
        
        return message
    
    def process_purchase(self, user_id: int, card_id: int) -> tuple[bool, str, Optional[dict]]:
        """
        Process a gift card purchase
        
        Returns: (success, message, purchase_record)
        """
        # Get card
        card = self.db.get_card_by_id(card_id)
        if not card:
            return False, "Card not found", None
        
        # Check availability
        if card['status'] != 'available':
            return False, "Card is not available", None
        
        if card['stock'] <= 0:
            return False, "Out of stock", None
        
        # Mark as sold
        success = self.db.mark_as_sold(card_id, user_id)
        if not success:
            return False, "Failed to process purchase", None
        
        # Record the purchase with full details
        purchase_id = self.db.add_gift_card_purchase(user_id, card)
        
        # Create order record
        self.db.add_order(user_id, card_id, card['price'])
        
        # Update stock
        self.db.update_stock(card_id, -1)
        
        # Get purchase record
        purchases = self.db.get_user_purchases(user_id)
        purchase = next((p for p in purchases if p['id'] == purchase_id), None)
        
        return True, "Purchase successful!", purchase
    
    def send_card_to_user(self, user_id: int, purchase: dict) -> str:
        """
        Format purchased card details for delivery to user
        
        This should be sent privately and securely to the buyer
        """
        message = "🎉 **Your Gift Card Details**\n\n"
        message += f"Card Name: {purchase['card_name']}\n"
        message += f"Amount: ${purchase['amount']:.2f}\n\n"
        
        message += "**Card Information:**\n"
        if purchase.get('card_number'):
            message += f"💳 Card Number: `{purchase['card_number']}`\n"
        if purchase.get('exp_date'):
            message += f"📅 Expiration: `{purchase['exp_date']}`\n"
        if purchase.get('pin'):
            message += f"🔢 PIN: `{purchase['pin']}`\n"
        
        message += f"\n📅 Purchased: {purchase['purchased_at']}\n"
        message += "\n⚠️ Save this information securely!\n"
        message += "This message will not be shown again."
        
        return message
    
    def get_user_purchase_history(self, user_id: int) -> str:
        """
        Get formatted purchase history for a user
        """
        purchases = self.db.get_user_purchases(user_id)
        
        if not purchases:
            return "You haven't made any purchases yet."
        
        message = f"📋 **Your Purchase History** ({len(purchases)} items)\n\n"
        
        for idx, purchase in enumerate(purchases, 1):
            message += f"{idx}. {purchase['card_name']}\n"
            message += f"   💰 ${purchase['amount']:.2f}\n"
            message += f"   💳 ****{purchase['card_number'][-4:] if purchase.get('card_number') else 'N/A'}\n"
            message += f"   📅 {purchase['purchased_at']}\n\n"
        
        return message
    
    def send_card_images(self, card: dict) -> list:
        """
        Get list of image paths to send
        Returns list of (image_type, path) tuples
        """
        images = self.db.get_card_images(card)
        result = []
        
        if images['front']:
            result.append(('front', images['front']))
        if images['back']:
            result.append(('back', images['back']))
        
        return result


# Example usage
if __name__ == '__main__':
    print("=" * 60)
    print("Gift Card Bot Integration Example")
    print("=" * 60)
    
    # Initialize bot
    bot = GiftCardBot('/tmp/example_bot.db.json')
    
    # Example 1: Add card with auto-generation
    print("\n1. Adding card with auto-generated details...")
    card1 = bot.add_card_with_auto_generation(
        name="Netflix Premium 1 Month",
        description="Premium subscription",
        price=15.99,
        category="Entertainment",
        stock=10
    )
    print(f"   ✅ Added card: {card1['name']}")
    print(f"   Auto-generated card number: {card1['card_number']}")
    print(f"   Expiration: {card1['exp_date']}")
    print(f"   PIN: {card1['pin']}")
    
    # Example 2: Add card with manual details
    print("\n2. Adding card with manual details...")
    card2 = bot.add_card_with_manual_details(
        name="Amazon Gift Card $50",
        description="Use on Amazon.com",
        price=50.0,
        category="Shopping",
        card_number="4111111111111111",
        exp_date="12/25",
        pin="5678",
        image_front="images/amazon_front.jpg",
        image_back="images/amazon_back.jpg",
        stock=5
    )
    print(f"   ✅ Added card: {card2['name']}")
    
    # Example 3: Display card to user
    print("\n3. Displaying card (how it appears to user):")
    display_text = bot.display_card_to_user(card1)
    print(display_text)
    
    # Example 4: Process a purchase
    print("\n4. Processing purchase...")
    test_user_id = 123456789
    success, message, purchase = bot.process_purchase(test_user_id, card1['id'])
    print(f"   Status: {message}")
    if success:
        print(f"   Purchase ID: {purchase['id']}")
    
    # Example 5: Send card details to buyer
    if success:
        print("\n5. Card details sent to buyer:")
        delivery_message = bot.send_card_to_user(test_user_id, purchase)
        print(delivery_message)
    
    # Example 6: View purchase history
    print("\n6. User's purchase history:")
    history = bot.get_user_purchase_history(test_user_id)
    print(history)
    
    # Example 7: Get images for card
    print("\n7. Images to send:")
    images = bot.send_card_images(card2)
    for img_type, path in images:
        print(f"   {img_type}: {path}")
    
    print("\n" + "=" * 60)
    print("✅ Integration example completed successfully!")
    print("=" * 60)
    
    # Cleanup
    import os
    if os.path.exists('/tmp/example_bot.db.json'):
        os.remove('/tmp/example_bot.db.json')
