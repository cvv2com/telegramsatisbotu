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
    
    # Get cards by category (all cards, not just available)
    mc_numeric = db.get_cards_by_category("MC Numeric", status=None)
    visa_numeric = db.get_cards_by_category("Visa Numeric", status=None)
    mc_picture = db.get_cards_by_category("MC Picture", status=None)
    visa_picture = db.get_cards_by_category("Visa Picture", status=None)
    
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

def payment_stats():
    """Ödeme istatistiklerini göster"""
    db = GiftCardDB(DB_FILE)
    stats = db.get_payment_stats()
    
    print("\n" + "="*70)
    print("ÖDEME İSTATİSTİKLERİ")
    print("="*70)
    print(f"\n📊 Genel:")
    print(f"   Toplam İşlem: {stats['total']}")
    print(f"   Bekleyen: {stats['pending']}")
    print(f"   Onaylanan: {stats['confirmed']}")
    print(f"   Başarısız: {stats['failed']}")
    print(f"   Timeout: {stats['timeout']}")
    print(f"\n💰 Toplam Hacim: ${stats['total_volume_usd']:.2f}")
    print("="*70 + "\n")

def pending_payments():
    """Bekleyen ödemeleri listele"""
    db = GiftCardDB(DB_FILE)
    pending = db.get_pending_transactions()
    
    if not pending:
        print("\n✅ Bekleyen ödeme yok.\n")
        return
    
    print("\n" + "="*70)
    print("BEKLEYEN ÖDEMELER")
    print("="*70)
    print(f"{'ID':<8} {'User ID':<15} {'Tutar':<20} {'USD':<12} {'Oluşturulma':<20}")
    print("-"*70)
    
    for tx in pending:
        amount_str = f"{tx['amount']:.8f} {tx['currency']}"
        usd_str = f"${tx.get('usd_equivalent', 0):.2f}"
        created = tx['created_at'][:19]
        print(f"{tx['id']:<8} {tx['user_id']:<15} {amount_str:<20} {usd_str:<12} {created:<20}")
    
    print("-"*70)
    print(f"Toplam bekleyen: {len(pending)}\n")

def confirm_payment_cmd(tx_hash):
    """Manuel ödeme onaylama"""
    if not tx_hash:
        print("❌ Transaction hash gerekli!")
        print("Kullanım: python admin.py confirm_payment <tx_hash>")
        return
    
    db = GiftCardDB(DB_FILE)
    
    # Find transaction by hash
    tx = db.get_transaction_by_hash(tx_hash)
    if not tx:
        print(f"❌ Transaction hash bulunamadı: {tx_hash}")
        return
    
    if tx['status'] != 'pending':
        print(f"❌ İşlem zaten {tx['status']} durumunda!")
        return
    
    # Confirm transaction
    success = db.confirm_transaction(tx['id'], tx_hash, credit_balance=True)
    
    if success:
        print(f"✅ İşlem onaylandı!")
        print(f"   İşlem ID: #{tx['id']}")
        print(f"   Kullanıcı: {tx['user_id']}")
        print(f"   Tutar: {tx['amount']:.8f} {tx['currency']}")
        print(f"   USD: ${tx.get('usd_equivalent', 0):.2f}")
        print(f"   Bakiye kredilendirildi!")
    else:
        print("❌ İşlem onaylanamadı!")

def cancel_payment_cmd(tx_id, reason=None):
    """Ödemeyi iptal et"""
    try:
        tx_id = int(tx_id)
    except ValueError:
        print("❌ Geçersiz işlem ID!")
        return
    
    if reason is None:
        reason = "Cancelled by admin"
    
    db = GiftCardDB(DB_FILE)
    
    # Get transaction
    tx = db.get_transaction_by_id(tx_id)
    if not tx:
        print(f"❌ İşlem bulunamadı: #{tx_id}")
        return
    
    if tx['status'] != 'pending':
        print(f"❌ İşlem zaten {tx['status']} durumunda!")
        return
    
    # Cancel transaction
    success = db.cancel_payment(tx_id, reason)
    
    if success:
        print(f"✅ İşlem iptal edildi!")
        print(f"   İşlem ID: #{tx_id}")
        print(f"   Kullanıcı: {tx['user_id']}")
        print(f"   Sebep: {reason}")
    else:
        print("❌ İşlem iptal edilemedi!")

def transaction_history(user_id):
    """Kullanıcının işlem geçmişini göster"""
    try:
        user_id = int(user_id)
    except ValueError:
        print("❌ Geçersiz kullanıcı ID!")
        return
    
    db = GiftCardDB(DB_FILE)
    transactions = db.get_user_transactions(user_id)
    
    if not transactions:
        print(f"\n⚠️ Kullanıcı {user_id} için işlem bulunamadı.\n")
        return
    
    print("\n" + "="*80)
    print(f"KULLANICI {user_id} - İŞLEM GEÇMİŞİ")
    print("="*80)
    print(f"{'ID':<8} {'Tutar':<25} {'USD':<12} {'Durum':<12} {'Tarih':<20}")
    print("-"*80)
    
    for tx in transactions:
        amount_str = f"{tx['amount']:.8f} {tx['currency']}"
        usd_str = f"${tx.get('usd_equivalent', 0):.2f}"
        created = tx['created_at'][:19]
        print(f"{tx['id']:<8} {amount_str:<25} {usd_str:<12} {tx['status']:<12} {created:<20}")
    
    print("-"*80)
    print(f"Toplam işlem: {len(transactions)}\n")

def print_help():
    """Yardım mesajını göster"""
    print("""
Admin Utility Script - MC/Visa Gift Card System

Kullanım:
    python admin.py [komut] [parametreler]

Gift Card Komutları:
    stats                           - Sistem istatistiklerini göster
    addmcnumeric <adet>             - MC numerik kart ekle
    addvisanumeric <adet>           - Visa numerik kart ekle
    addmcpicture <id>               - MC resimli kart ekle
    addvisapicture <id>             - Visa resimli kart ekle
    addbalance <user_id> <tutar>    - Kullanıcıya bakiye ekle
    users                           - Tüm kullanıcıları listele

Ödeme Komutları:
    payment_stats                   - Ödeme istatistiklerini göster
    pending_payments                - Bekleyen ödemeleri listele
    confirm_payment <tx_hash>       - Ödemeyi manuel onayla
    cancel_payment <tx_id> [sebep]  - Ödemeyi iptal et
    transaction_history <user_id>   - Kullanıcı işlem geçmişi

Genel:
    help                            - Bu yardım mesajını göster

Örnekler:
    python admin.py stats
    python admin.py addmcnumeric 10
    python admin.py addbalance 123456789 100.50
    python admin.py payment_stats
    python admin.py pending_payments
    python admin.py confirm_payment abc123def456...
    python admin.py cancel_payment 5 "User requested"
    python admin.py transaction_history 123456789
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
    elif command == 'payment_stats':
        payment_stats()
    elif command == 'pending_payments':
        pending_payments()
    elif command == 'confirm_payment':
        if len(sys.argv) < 3:
            print("❌ Transaction hash gerekli!")
            print("Kullanım: python admin.py confirm_payment <tx_hash>")
            return
        confirm_payment_cmd(sys.argv[2])
    elif command == 'cancel_payment':
        if len(sys.argv) < 3:
            print("❌ İşlem ID gerekli!")
            print("Kullanım: python admin.py cancel_payment <tx_id> [sebep]")
            return
        reason = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else None
        cancel_payment_cmd(sys.argv[2], reason)
    elif command == 'transaction_history':
        if len(sys.argv) < 3:
            print("❌ Kullanıcı ID gerekli!")
            print("Kullanım: python admin.py transaction_history <user_id>")
            return
        transaction_history(sys.argv[2])
    elif command == 'help':
        print_help()
    else:
        print(f"❌ Bilinmeyen komut: {command}")
        print_help()

if __name__ == '__main__':
    main()
