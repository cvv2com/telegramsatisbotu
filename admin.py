#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin Utility Script - MC/Visa Gift Card System
Bakiye yönetimi, kart ekleme ve kullanıcı yönetimi için yardımcı script
"""

import sys
from datetime import datetime
from database import GiftCardDB

# Initialize database
DB_FILE = 'gift_cards.db.json'

def get_stats():
    """Genel istatistikleri göster"""
    db = GiftCardDB(DB_FILE)
    
    # Get cards by category
    mc_numeric = db.get_cards_by_category("MC Numeric")
    visa_numeric = db.get_cards_by_category("Visa Numeric")
    mc_picture = db.get_cards_by_category("MC Picture")
    visa_picture = db.get_cards_by_category("Visa Picture")
    
    mc_numeric_available = len([c for c in mc_numeric if c['status'] == 'available'])
    visa_numeric_available = len([c for c in visa_numeric if c['status'] == 'available'])
    mc_picture_available = len([c for c in mc_picture if c['status'] == 'available'])
    visa_picture_available = len([c for c in visa_picture if c['status'] == 'available'])
    
    mc_numeric_sold = len([c for c in mc_numeric if c['status'] == 'sold'])
    visa_numeric_sold = len([c for c in visa_numeric if c['status'] == 'sold'])
    mc_picture_sold = len([c for c in mc_picture if c['status'] == 'sold'])
    visa_picture_sold = len([c for c in visa_picture if c['status'] == 'sold'])
    
    # Calculate revenue
    all_cards = db.get_all_cards()
    total_revenue = sum(c['price'] for c in all_cards if c['status'] == 'sold')
    
    print("\n" + "="*60)
    print("MC/VISA GIFT CARD SİSTEMİ - İSTATİSTİKLER")
    print("="*60)
    print(f"\n💳 MC Numerik:")
    print(f"   Mevcut: {mc_numeric_available}")
    print(f"   Satılan: {mc_numeric_sold}")
    print(f"\n💳 Visa Numerik:")
    print(f"   Mevcut: {visa_numeric_available}")
    print(f"   Satılan: {visa_numeric_sold}")
    print(f"\n🖼️ MC Resimli:")
    print(f"   Mevcut: {mc_picture_available}")
    print(f"   Satılan: {mc_picture_sold}")
    print(f"\n🖼️ Visa Resimli:")
    print(f"   Mevcut: {visa_picture_available}")
    print(f"   Satılan: {visa_picture_sold}")
    print(f"\n💰 Toplam Gelir: ${total_revenue:.2f}")
    print("="*60 + "\n")

def add_mc_numeric(quantity):
    """MC numerik kartları ekle"""
    try:
        quantity = int(quantity)
        if quantity <= 0:
            print("❌ Adet pozitif bir sayı olmalıdır!")
            return
    except ValueError:
        print("❌ Geçersiz adet!")
        return
    
    db = GiftCardDB(DB_FILE)
    print(f"\n🔄 {quantity} adet MC numerik kart ekleniyor...")
    
    card_ids = db.add_mc_numeric_card(quantity)
    
    print(f"✅ {len(card_ids)} adet MC numerik kart başarıyla eklendi!")
    print(f"   Kart ID'leri: {', '.join(map(str, card_ids))}")

def add_visa_numeric(quantity):
    """Visa numerik kartları ekle"""
    try:
        quantity = int(quantity)
        if quantity <= 0:
            print("❌ Adet pozitif bir sayı olmalıdır!")
            return
    except ValueError:
        print("❌ Geçersiz adet!")
        return
    
    db = GiftCardDB(DB_FILE)
    print(f"\n🔄 {quantity} adet Visa numerik kart ekleniyor...")
    
    card_ids = db.add_visa_numeric_card(quantity)
    
    print(f"✅ {len(card_ids)} adet Visa numerik kart başarıyla eklendi!")
    print(f"   Kart ID'leri: {', '.join(map(str, card_ids))}")

def add_mc_picture(card_id_num):
    """MC resimli kart ekle"""
    try:
        card_id_num = int(card_id_num)
        if card_id_num <= 0:
            print("❌ ID pozitif bir sayı olmalıdır!")
            return
    except ValueError:
        print("❌ Geçersiz ID!")
        return
    
    db = GiftCardDB(DB_FILE)
    print(f"\n🔄 MC resimli kart ekleniyor (ID: {card_id_num})...")
    print(f"   Görsel dosyaları:")
    print(f"   - /giftcards/mc{card_id_num}front.jpg")
    print(f"   - /giftcards/mc{card_id_num}back.jpg")
    
    card_id = db.add_mc_picture_card(card_id_num)
    
    print(f"✅ MC resimli kart başarıyla eklendi!")
    print(f"   Kart ID: {card_id}")

def add_visa_picture(card_id_num):
    """Visa resimli kart ekle"""
    try:
        card_id_num = int(card_id_num)
        if card_id_num <= 0:
            print("❌ ID pozitif bir sayı olmalıdır!")
            return
    except ValueError:
        print("❌ Geçersiz ID!")
        return
    
    db = GiftCardDB(DB_FILE)
    print(f"\n🔄 Visa resimli kart ekleniyor (ID: {card_id_num})...")
    print(f"   Görsel dosyaları:")
    print(f"   - /giftcards/visa{card_id_num}front.jpg")
    print(f"   - /giftcards/visa{card_id_num}back.jpg")
    
    card_id = db.add_visa_picture_card(card_id_num)
    
    print(f"✅ Visa resimli kart başarıyla eklendi!")
    print(f"   Kart ID: {card_id}")

def add_balance_to_user(user_id, amount):
    """Kullanıcıya bakiye ekle"""
    try:
        user_id = int(user_id)
        amount = float(amount)
        
        if user_id <= 0:
            print("❌ Kullanıcı ID'si pozitif bir sayı olmalıdır!")
            return
        
        if amount <= 0:
            print("❌ Miktar pozitif bir sayı olmalıdır!")
            return
    except ValueError:
        print("❌ Geçersiz giriş!")
        return
    
    db = GiftCardDB(DB_FILE)
    
    # Get current balance
    current_balance = db.get_user_balance(user_id)
    
    # Add balance
    if db.add_balance(user_id, amount):
        new_balance = db.get_user_balance(user_id)
        print(f"✅ Bakiye eklendi!")
        print(f"   Kullanıcı ID: {user_id}")
        print(f"   Eklenen: ${amount:.2f}")
        print(f"   Önceki: ${current_balance:.2f}")
        print(f"   Yeni Bakiye: ${new_balance:.2f}")
    else:
        print("❌ Bakiye eklenemedi!")

def list_users():
    """Tüm kullanıcıları listele"""
    db = GiftCardDB(DB_FILE)
    
    if 'users' not in db.data or not db.data['users']:
        print("\n⚠️ Henüz kullanıcı bulunmuyor.\n")
        return
    
    print("\n" + "="*70)
    print("KULLANICILAR LİSTESİ")
    print("="*70)
    print(f"{'User ID':<15} {'Balance':<15} {'Language':<15}")
    print("-"*70)
    
    for user_id_str, user_data in db.data['users'].items():
        balance = user_data.get('balance', 0.0)
        language = user_data.get('language', 'tr')
        print(f"{user_id_str:<15} ${balance:<14.2f} {language:<15}")
    
    print("-"*70)
    print(f"Toplam kullanıcı: {len(db.data['users'])}\n")

def print_help():
    """Yardım mesajını göster"""
    print("""
Admin Utility Script - MC/Visa Gift Card System

Kullanım:
    python admin.py [komut] [parametreler]

Komutlar:
    stats                           - Sistem istatistiklerini göster
    addmcnumeric <adet>             - MC numerik kart ekle
    addvisanumeric <adet>           - Visa numerik kart ekle
    addmcpicture <id>               - MC resimli kart ekle
    addvisapicture <id>             - Visa resimli kart ekle
    addbalance <user_id> <tutar>    - Kullanıcıya bakiye ekle
    users                           - Tüm kullanıcıları listele
    help                            - Bu yardım mesajını göster

Örnekler:
    python admin.py stats
    python admin.py addmcnumeric 10
    python admin.py addvisanumeric 5
    python admin.py addmcpicture 1
    python admin.py addvisapicture 2
    python admin.py addbalance 123456789 100.50
    python admin.py users
    """)

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'stats':
        get_stats()
    elif command == 'addmcnumeric':
        if len(sys.argv) < 3:
            print("❌ Adet gerekli!")
            print("Kullanım: python admin.py addmcnumeric <adet>")
            return
        add_mc_numeric(sys.argv[2])
    elif command == 'addvisanumeric':
        if len(sys.argv) < 3:
            print("❌ Adet gerekli!")
            print("Kullanım: python admin.py addvisanumeric <adet>")
            return
        add_visa_numeric(sys.argv[2])
    elif command == 'addmcpicture':
        if len(sys.argv) < 3:
            print("❌ ID gerekli!")
            print("Kullanım: python admin.py addmcpicture <id>")
            return
        add_mc_picture(sys.argv[2])
    elif command == 'addvisapicture':
        if len(sys.argv) < 3:
            print("❌ ID gerekli!")
            print("Kullanım: python admin.py addvisapicture <id>")
            return
        add_visa_picture(sys.argv[2])
    elif command == 'addbalance':
        if len(sys.argv) < 4:
            print("❌ Kullanıcı ID'si ve tutar gerekli!")
            print("Kullanım: python admin.py addbalance <user_id> <tutar>")
            return
        add_balance_to_user(sys.argv[2], sys.argv[3])
    elif command == 'users':
        list_users()
    elif command == 'help':
        print_help()
    else:
        print(f"❌ Bilinmeyen komut: {command}")
        print_help()

if __name__ == '__main__':
    main()
