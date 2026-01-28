"""
Veritabanı yönetimi - Database management
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class GiftCardDB:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.data = self._load()
    
    def _load(self) -> Dict:
        """Veritabanını yükle / Load database"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'gift_cards': [],
            'categories': [],
            'orders': []
        }
    
    def _save(self):
        """Veritabanını kaydet / Save database"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_gift_card(self, name: str, description: str, price: float, 
                     category: str, code: str, image_url: Optional[str] = None) -> int:
        """Gift card ekle / Add gift card"""
        card_id = len(self.data['gift_cards']) + 1
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
    
    def mark_as_sold(self, card_id: int, buyer_id: int):
        """Kartı satılmış olarak işaretle / Mark card as sold"""
        for card in self.data['gift_cards']:
            if card['id'] == card_id:
                card['status'] = 'sold'
                card['sold_at'] = datetime.now().isoformat()
                card['buyer_id'] = buyer_id
                break
        self._save()
    
    def delete_card(self, card_id: int) -> bool:
        """Kartı sil / Delete card"""
        for i, card in enumerate(self.data['gift_cards']):
            if card['id'] == card_id:
                self.data['gift_cards'].pop(i)
                self._save()
                return True
        return False
    
    def add_order(self, buyer_id: int, card_id: int, amount: float):
        """Sipariş ekle / Add order"""
        order = {
            'id': len(self.data['orders']) + 1,
            'buyer_id': buyer_id,
            'card_id': card_id,
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        }
        self.data['orders'].append(order)
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
