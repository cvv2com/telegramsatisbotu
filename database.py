"""
Veritabanı yönetimi - Database management

Note: The card generation functions use Python's `random` module for simplicity.
For production use with real payment cards, use the `secrets` module for 
cryptographically secure random number generation.
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import threading
import random
import string

class GiftCardDB:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.data = self._load()
        self._lock = threading.Lock()
    
    @staticmethod
    def generate_card_number(card_type: str = 'visa') -> str:
        """Generate a unique card number based on card type
        Args:
            card_type: 'visa', 'mc', 'mastercard', 'amex', or 'discover'
        Returns:
            Card number string (15 digits for Amex, 16 digits for others)
        """
        # BIN (Bank Identification Number) prefixes
        bin_prefixes = {
            'visa': ['4'],
            'mc': ['5'],  # MC cards start with 5
            'mastercard': ['5'],
            'amex': ['34', '37'],
            'discover': ['6011', '65']
        }
        
        prefix_list = bin_prefixes.get(card_type.lower(), ['4'])
        prefix = random.choice(prefix_list)
        
        # Generate remaining digits (16 total for visa/mc/discover, 15 for amex)
        target_length = 15 if card_type.lower() == 'amex' else 16
        remaining_length = target_length - len(prefix)
        
        card_number = prefix + ''.join([str(random.randint(0, 9)) for _ in range(remaining_length)])
        return card_number
    
    @staticmethod
    def generate_expiration_date(months_valid: int = 24) -> str:
        """Generate expiration date in MM/YY format
        Args:
            months_valid: Number of months from now (default: 24 months)
        Returns:
            Expiration date string in MM/YY format (uppercase)
        """
        exp_date = datetime.now() + timedelta(days=months_valid * 30)
        return exp_date.strftime('%m/%y').upper()
    
    @staticmethod
    def generate_pin(length: int = 3) -> str:
        """Generate a random PIN code
        Args:
            length: Number of digits (default: 3 for MC/Visa gift cards)
        Returns:
            PIN code string
        """
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    @staticmethod
    def generate_card_code(prefix: str = 'GC', length: int = 12) -> str:
        """Generate a unique gift card code
        Args:
            prefix: Code prefix (default: 'GC')
            length: Total length including prefix (default: 12)
        Returns:
            Unique card code string
        Raises:
            ValueError: If length is too small for the prefix
        """
        if length <= len(prefix):
            raise ValueError(f"Length ({length}) must be greater than prefix length ({len(prefix)})")
        
        code_length = length - len(prefix) - 1  # -1 for dash
        if code_length <= 0:
            raise ValueError(f"Length ({length}) is too small for prefix '{prefix}' plus separator")
        
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length))
        return f"{prefix}-{code}"
    
    def _load(self) -> Dict:
        """Veritabanını yükle / Load database"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load database file: {e}")
                print("Initializing with empty database...")
        return {
            'gift_cards': [],
            'categories': [],
            'orders': [],
            'gift_card_purchases': [],  # New: detailed purchase records
            'coupons': [],
            'users': {},  # Store user preferences like language
            'next_card_id': 1,
            'next_order_id': 1,
            'next_coupon_id': 1,
            'next_purchase_id': 1  # New: for gift_card_purchases
        }
    
    def _save(self):
        """Veritabanını kaydet / Save database"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error: Could not save database: {e}")
            raise
    
    def add_gift_card(self, name: str, description: str, price: float, 
                     category: str, code: str, image_url: Optional[str] = None, 
                     stock: int = 1, card_number: Optional[str] = None,
                     exp_date: Optional[str] = None, pin: Optional[str] = None,
                     image_front: Optional[str] = None, image_back: Optional[str] = None) -> int:
        """Gift card ekle / Add gift card
        
        Supports both legacy format (image_url) and new format (image_front/image_back).
        Supports both manual card details and auto-generation.
        
        Args:
            name: Card name
            description: Card description
            price: Card price
            category: Card category
            code: Card code/identifier
            image_url: Legacy - single image path (for backward compatibility)
            stock: Stock quantity (default: 1)
            card_number: Optional card number (auto-generated if not provided)
            exp_date: Optional expiration date in MM/YY format (auto-generated if not provided)
            pin: Optional PIN code (auto-generated if not provided)
            image_front: Optional front face image path
            image_back: Optional back face image path
        
        Returns:
            Card ID
        """
        with self._lock:
            card_id = self.data.get('next_card_id', 1)
            
            # Auto-generate card details if not provided
            if card_number is None:
                card_number = self.generate_card_number()
            if exp_date is None:
                exp_date = self.generate_expiration_date()
            if pin is None:
                pin = self.generate_pin()
            
            card = {
                'id': card_id,
                'name': name,
                'description': description,
                'price': price,
                'category': category,
                'code': code,
                'image_url': image_url,  # Legacy support
                'image_front': image_front,  # New format
                'image_back': image_back,  # New format
                'card_number': card_number,  # New: actual card number
                'exp_date': exp_date,  # New: expiration date
                'pin': pin,  # New: PIN code
                'stock': stock,
                'status': 'available',  # available, sold, reserved
                'created_at': datetime.now().isoformat(),
                'sold_at': None,
                'buyer_id': None
            }
            self.data['gift_cards'].append(card)
            self.data['next_card_id'] = card_id + 1
            
            # Kategoriyi ekle (yoksa)
            if category not in self.data['categories']:
                self.data['categories'].append(category)
            
            self._save()
            return card_id
    
    def get_all_cards(self, status: Optional[str] = None) -> List[Dict]:
        """Tüm kartları getir / Get all cards"""
        cards = self.data['gift_cards']
        if status:
            cards = [c for c in cards if c['status'] == status]
        return cards
    
    def get_card_by_id(self, card_id: int) -> Optional[Dict]:
        """ID'ye göre kart getir / Get card by ID"""
        for card in self.data['gift_cards']:
            if card['id'] == card_id:
                return card
        return None
    
    def get_cards_by_category(self, category: str, status: Optional[str] = 'available') -> List[Dict]:
        """Kategoriye göre kartları getir / Get cards by category"""
        cards = []
        for card in self.data['gift_cards']:
            if card['category'] == category:
                if status is None or card['status'] == status:
                    cards.append(card)
        return cards
    
    def get_categories(self) -> List[str]:
        """Kategorileri getir / Get categories"""
        return self.data['categories']
    
    def mark_as_sold(self, card_id: int, buyer_id: int) -> bool:
        """Kartı satılmış olarak işaretle / Mark card as sold
        Returns True if successful, False if card is not available"""
        with self._lock:
            for card in self.data['gift_cards']:
                if card['id'] == card_id:
                    if card['status'] != 'available':
                        return False
                    card['status'] = 'sold'
                    card['sold_at'] = datetime.now().isoformat()
                    card['buyer_id'] = buyer_id
                    self._save()
                    return True
            return False
    
    def delete_card(self, card_id: int) -> bool:
        """Kartı sil / Delete card"""
        with self._lock:
            for i, card in enumerate(self.data['gift_cards']):
                if card['id'] == card_id:
                    self.data['gift_cards'].pop(i)
                    self._save()
                    return True
            return False
    
    def add_order(self, buyer_id: int, card_id: int, amount: float):
        """Sipariş ekle / Add order"""
        with self._lock:
            order_id = self.data.get('next_order_id', 1)
            order = {
                'id': order_id,
                'buyer_id': buyer_id,
                'card_id': card_id,
                'amount': amount,
                'timestamp': datetime.now().isoformat()
            }
            self.data['orders'].append(order)
            self.data['next_order_id'] = order_id + 1
            self._save()
    
    def add_gift_card_purchase(self, user_id: int, card: Dict) -> int:
        """Record a detailed gift card purchase with card details
        
        This creates a permanent record of the card details delivered to the user.
        
        Args:
            user_id: Telegram user ID of the buyer
            card: Card dictionary with all details
        
        Returns:
            Purchase ID
        """
        with self._lock:
            # Initialize if not exists (for legacy databases)
            if 'gift_card_purchases' not in self.data:
                self.data['gift_card_purchases'] = []
            if 'next_purchase_id' not in self.data:
                self.data['next_purchase_id'] = 1
            
            purchase_id = self.data.get('next_purchase_id', 1)
            purchase = {
                'id': purchase_id,
                'user_id': user_id,
                'card_id': card['id'],
                'card_name': card['name'],
                'card_number': card.get('card_number'),
                'exp_date': card.get('exp_date'),
                'pin': card.get('pin'),
                'amount': card['price'],
                'purchased_at': datetime.now().isoformat()
            }
            self.data['gift_card_purchases'].append(purchase)
            self.data['next_purchase_id'] = purchase_id + 1
            self._save()
            return purchase_id
    
    def get_user_purchases(self, user_id: int) -> List[Dict]:
        """Get all gift card purchases for a specific user
        
        Args:
            user_id: Telegram user ID
        
        Returns:
            List of purchase records with card details
        """
        if 'gift_card_purchases' not in self.data:
            return []
        
        purchases = [p for p in self.data['gift_card_purchases'] if p['user_id'] == user_id]
        return sorted(purchases, key=lambda x: x['purchased_at'], reverse=True)
    
    def get_card_images(self, card: Dict) -> Dict[str, Optional[str]]:
        """Get card image paths, supporting both legacy and new formats
        
        Legacy format: card has 'image_url' field
        New format: card has 'image_front' and 'image_back' fields
        
        Args:
            card: Card dictionary
        
        Returns:
            Dictionary with 'front' and 'back' keys (values can be None)
        """
        # Check for new format first
        if card.get('image_front') or card.get('image_back'):
            return {
                'front': card.get('image_front'),
                'back': card.get('image_back')
            }
        
        # Legacy format: use image_url as front image
        if card.get('image_url'):
            return {
                'front': card.get('image_url'),
                'back': None
            }
        
        # No images
        return {
            'front': None,
            'back': None
        }
    
    def get_stats(self) -> Dict:
        """İstatistikleri getir / Get statistics"""
        total_cards = len(self.data['gift_cards'])
        available_cards = len([c for c in self.data['gift_cards'] if c['status'] == 'available'])
        sold_cards = len([c for c in self.data['gift_cards'] if c['status'] == 'sold'])
        total_revenue = sum(c['price'] for c in self.data['gift_cards'] if c['status'] == 'sold')
        
        return {
            'total_cards': total_cards,
            'available_cards': available_cards,
            'sold_cards': sold_cards,
            'total_revenue': total_revenue
        }
    
    # Alias methods for compatibility with bot.py
    def get_available_cards(self, category: Optional[str] = None) -> List[Dict]:
        """Get available cards (alias method)"""
        if category:
            return self.get_cards_by_category(category, status='available')
        return self.get_all_cards(status='available')
    
    def get_card(self, card_id: int) -> Optional[Dict]:
        """Get card by ID (alias method)"""
        return self.get_card_by_id(card_id)
    
    def delete_gift_card(self, card_id: int) -> bool:
        """Delete gift card (alias method)"""
        return self.delete_card(card_id)
    
    # User preference methods
    def set_user_language(self, user_id: int, language: str):
        """Set user language preference"""
        with self._lock:
            if 'users' not in self.data:
                self.data['users'] = {}
            if user_id not in self.data['users']:
                self.data['users'][user_id] = {}
            self.data['users'][user_id]['language'] = language
            self._save()
    
    def get_user_language(self, user_id: int) -> str:
        """Get user language preference"""
        if 'users' not in self.data:
            return 'tr'  # Default to Turkish
        user = self.data['users'].get(user_id, {})
        return user.get('language', 'tr')
    
    # Order methods
    def get_user_orders(self, user_id: int) -> List[Dict]:
        """Get all orders for a specific user"""
        orders = []
        for order in self.data.get('orders', []):
            if order['buyer_id'] == user_id:
                # Enrich order with card details
                card = self.get_card_by_id(order['card_id'])
                if card:
                    order_copy = order.copy()
                    order_copy['card_name'] = card['name']
                    order_copy['card_category'] = card['category']
                    orders.append(order_copy)
        return sorted(orders, key=lambda x: x['timestamp'], reverse=True)
    
    # Coupon methods
    def add_coupon(self, code: str, discount_type: str, discount_value: float, 
                   max_uses: int = None, expires_at: str = None) -> int:
        """Add a discount coupon"""
        with self._lock:
            if 'coupons' not in self.data:
                self.data['coupons'] = []
                self.data['next_coupon_id'] = 1
                
            coupon_id = self.data.get('next_coupon_id', 1)
            coupon = {
                'id': coupon_id,
                'code': code.upper(),
                'discount_type': discount_type,  # 'percentage' or 'fixed'
                'discount_value': discount_value,
                'max_uses': max_uses,
                'uses': 0,
                'active': True,
                'created_at': datetime.now().isoformat(),
                'expires_at': expires_at
            }
            self.data['coupons'].append(coupon)
            self.data['next_coupon_id'] = coupon_id + 1
            self._save()
            return coupon_id
    
    def get_coupon(self, code: str) -> Optional[Dict]:
        """Get coupon by code"""
        if 'coupons' not in self.data:
            return None
        for coupon in self.data['coupons']:
            if coupon['code'].upper() == code.upper() and coupon['active']:
                return coupon
        return None
    
    def validate_coupon(self, code: str) -> tuple[bool, str, Optional[Dict]]:
        """Validate if coupon can be used
        Returns: (is_valid, message, coupon_data)"""
        coupon = self.get_coupon(code)
        
        if not coupon:
            return False, "invalid", None
        
        # Check if expired
        if coupon.get('expires_at'):
            try:
                expires = datetime.fromisoformat(coupon['expires_at'])
                if datetime.now() > expires:
                    return False, "expired", None
            except:
                pass
        
        # Check max uses
        if coupon.get('max_uses') and coupon['uses'] >= coupon['max_uses']:
            return False, "max_uses", None
        
        return True, "valid", coupon
    
    def use_coupon(self, code: str) -> bool:
        """Increment coupon usage counter"""
        with self._lock:
            coupon = self.get_coupon(code)
            if coupon:
                for c in self.data['coupons']:
                    if c['id'] == coupon['id']:
                        c['uses'] = c.get('uses', 0) + 1
                        self._save()
                        return True
            return False
    
    def get_all_coupons(self) -> List[Dict]:
        """Get all coupons"""
        return self.data.get('coupons', [])
    
    def delete_coupon(self, coupon_id: int) -> bool:
        """Delete a coupon"""
        with self._lock:
            if 'coupons' not in self.data:
                return False
            for i, coupon in enumerate(self.data['coupons']):
                if coupon['id'] == coupon_id:
                    self.data['coupons'].pop(i)
                    self._save()
                    return True
            return False
    
    def calculate_discount(self, price: float, coupon: Dict) -> float:
        """Calculate discounted price"""
        if coupon['discount_type'] == 'percentage':
            discount = price * (coupon['discount_value'] / 100)
            return max(0, price - discount)
        else:  # fixed
            return max(0, price - coupon['discount_value'])
    
    # Stock management methods
    def check_low_stock(self, threshold: int = 5) -> List[Dict]:
        """Get cards with stock below threshold"""
        low_stock = []
        for card in self.data['gift_cards']:
            if card['status'] == 'available' and card.get('stock', 1) <= threshold:
                low_stock.append(card)
        return low_stock
    
    def update_stock(self, card_id: int, quantity: int) -> bool:
        """Update card stock"""
        with self._lock:
            for card in self.data['gift_cards']:
                if card['id'] == card_id:
                    card['stock'] = card.get('stock', 1) + quantity
                    if card['stock'] <= 0 and card['status'] == 'available':
                        card['status'] = 'sold'
                    self._save()
                    return True
            return False
    
    def bulk_add_cards(self, cards_data: List[Dict]) -> tuple[int, List[str]]:
        """Add multiple cards at once
        
        Supports both legacy and new format cards.
        Auto-generates card details if not provided.
        
        Returns: (success_count, error_messages)
        """
        success_count = 0
        errors = []
        
        for idx, card_data in enumerate(cards_data):
            try:
                self.add_gift_card(
                    name=card_data['name'],
                    description=card_data.get('description', ''),
                    price=float(card_data['price']),
                    category=card_data.get('category', 'General'),
                    code=card_data['code'],
                    image_url=card_data.get('image_url'),  # Legacy support
                    image_front=card_data.get('image_front'),  # New format
                    image_back=card_data.get('image_back'),  # New format
                    card_number=card_data.get('card_number'),  # Auto-generated if None
                    exp_date=card_data.get('exp_date'),  # Auto-generated if None
                    pin=card_data.get('pin'),  # Auto-generated if None
                    stock=int(card_data.get('stock', 1))
                )
                success_count += 1
            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")
        
        return success_count, errors
    
    # Balance management methods for MC/Visa system
    def get_user_balance(self, user_id: int) -> float:
        """Get user's current balance"""
        if 'users' not in self.data:
            self.data['users'] = {}
        user = self.data['users'].get(str(user_id), {})
        return float(user.get('balance', 0.0))
    
    def add_balance(self, user_id: int, amount: float) -> bool:
        """Add balance to user account
        Args:
            user_id: User's Telegram ID
            amount: Amount to add
        Returns:
            True if successful
        """
        with self._lock:
            if 'users' not in self.data:
                self.data['users'] = {}
            user_id_str = str(user_id)
            if user_id_str not in self.data['users']:
                self.data['users'][user_id_str] = {'balance': 0.0}
            
            current_balance = float(self.data['users'][user_id_str].get('balance', 0.0))
            self.data['users'][user_id_str]['balance'] = current_balance + amount
            self._save()
            return True
    
    def deduct_balance(self, user_id: int, amount: float) -> bool:
        """Deduct balance from user account
        Args:
            user_id: User's Telegram ID
            amount: Amount to deduct
        Returns:
            True if successful, False if insufficient balance
        """
        with self._lock:
            current_balance = self.get_user_balance(user_id)
            if current_balance < amount:
                return False
            
            user_id_str = str(user_id)
            self.data['users'][user_id_str]['balance'] = current_balance - amount
            self._save()
            return True
    
    # MC/Visa card specific methods
    def add_mc_numeric_card(self, quantity: int = 1) -> List[int]:
        """Add MC numeric gift cards
        Args:
            quantity: Number of cards to add
        Returns:
            List of card IDs
        """
        card_ids = []
        for i in range(quantity):
            card_number = self.generate_card_number('mc')
            exp_date = self.generate_expiration_date()
            pin = self.generate_pin(3)
            code = self.generate_card_code('MC', 12)
            
            card_id = self.add_gift_card(
                name=f"MC Gift Card ${20}",
                description="Mastercard Numeric Gift Card",
                price=20.0,
                category="MC Numeric",
                code=code,
                card_number=card_number,
                exp_date=exp_date,
                pin=pin,
                stock=1
            )
            card_ids.append(card_id)
        return card_ids
    
    def add_visa_numeric_card(self, quantity: int = 1) -> List[int]:
        """Add Visa numeric gift cards
        Args:
            quantity: Number of cards to add
        Returns:
            List of card IDs
        """
        card_ids = []
        for i in range(quantity):
            card_number = self.generate_card_number('visa')
            exp_date = self.generate_expiration_date()
            pin = self.generate_pin(3)
            code = self.generate_card_code('VISA', 12)
            
            card_id = self.add_gift_card(
                name=f"Visa Gift Card ${20}",
                description="Visa Numeric Gift Card",
                price=20.0,
                category="Visa Numeric",
                code=code,
                card_number=card_number,
                exp_date=exp_date,
                pin=pin,
                stock=1
            )
            card_ids.append(card_id)
        return card_ids
    
    def add_mc_picture_card(self, card_id_num: int) -> int:
        """Add MC picture gift card
        Args:
            card_id_num: ID number for image file naming
        Returns:
            Card ID
        """
        card_number = self.generate_card_number('mc')
        exp_date = self.generate_expiration_date()
        pin = self.generate_pin(3)
        code = self.generate_card_code('MC-PIC', 12)
        
        return self.add_gift_card(
            name="MC Gift Card Picture $50",
            description="Mastercard Picture Gift Card",
            price=50.0,
            category="MC Picture",
            code=code,
            card_number=card_number,
            exp_date=exp_date,
            pin=pin,
            image_front=f"/giftcards/mc{card_id_num}front.jpg",
            image_back=f"/giftcards/mc{card_id_num}back.jpg",
            stock=1
        )
    
    def add_visa_picture_card(self, card_id_num: int) -> int:
        """Add Visa picture gift card
        Args:
            card_id_num: ID number for image file naming
        Returns:
            Card ID
        """
        card_number = self.generate_card_number('visa')
        exp_date = self.generate_expiration_date()
        pin = self.generate_pin(3)
        code = self.generate_card_code('VISA-PIC', 12)
        
        return self.add_gift_card(
            name="Visa Gift Card Picture $50",
            description="Visa Picture Gift Card",
            price=50.0,
            category="Visa Picture",
            code=code,
            card_number=card_number,
            exp_date=exp_date,
            pin=pin,
            image_front=f"/giftcards/visa{card_id_num}front.jpg",
            image_back=f"/giftcards/visa{card_id_num}back.jpg",
            stock=1
        )
    
    def purchase_cards_by_quantity(self, user_id: int, card_type: str, quantity: int) -> tuple[bool, str, List[Dict]]:
        """Purchase cards by quantity with balance deduction
        Args:
            user_id: User's Telegram ID
            card_type: 'mc_numeric', 'visa_numeric', 'mc_picture', or 'visa_picture'
            quantity: Number of cards to purchase
        Returns:
            (success, message, list of purchased cards)
        """
        # Calculate total price
        if card_type in ['mc_numeric', 'visa_numeric']:
            price_per_card = 20.0
            category = "MC Numeric" if card_type == 'mc_numeric' else "Visa Numeric"
        elif card_type in ['mc_picture', 'visa_picture']:
            price_per_card = 50.0
            category = "MC Picture" if card_type == 'mc_picture' else "Visa Picture"
        else:
            return False, "Invalid card type", []
        
        total_price = price_per_card * quantity
        
        # Check balance
        user_balance = self.get_user_balance(user_id)
        if user_balance < total_price:
            return False, f"Insufficient balance. Required: ${total_price:.2f}, Available: ${user_balance:.2f}", []
        
        # Get available cards of the requested type
        available_cards = self.get_cards_by_category(category, status='available')
        if len(available_cards) < quantity:
            return False, f"Not enough cards in stock. Available: {len(available_cards)}, Requested: {quantity}", []
        
        # Deduct balance
        if not self.deduct_balance(user_id, total_price):
            return False, "Failed to deduct balance", []
        
        # Mark cards as sold and record purchases
        purchased_cards = []
        for i in range(quantity):
            card = available_cards[i]
            if self.mark_as_sold(card['id'], user_id):
                self.add_gift_card_purchase(user_id, card)
                self.add_order(user_id, card['id'], card['price'])
                purchased_cards.append(card)
        
        return True, f"Successfully purchased {len(purchased_cards)} cards", purchased_cards
