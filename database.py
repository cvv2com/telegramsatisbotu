"""
Veritabanı yönetimi - Database management
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
import threading

class GiftCardDB:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.data = self._load()
        self._lock = threading.Lock()
    
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
            'coupons': [],
            'users': {},  # Store user preferences like language
            'next_card_id': 1,
            'next_order_id': 1,
            'next_coupon_id': 1
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
                     stock: int = 1) -> int:
        """Gift card ekle / Add gift card"""
        with self._lock:
            card_id = self.data.get('next_card_id', 1)
            card = {
                'id': card_id,
                'name': name,
                'description': description,
                'price': price,
                'category': category,
                'code': code,
                'image_url': image_url,
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
        Returns: (success_count, error_messages)"""
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
                    image_url=card_data.get('image_url'),
                    stock=int(card_data.get('stock', 1))
                )
                success_count += 1
            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")
        
        return success_count, errors
