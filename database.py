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
            'next_card_id': 1,
            'next_order_id': 1
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
                     category: str, code: str, image_url: Optional[str] = None) -> int:
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
