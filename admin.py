#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin Utility Script
Manuel bakiye yönetimi ve kullanıcı yönetimi için yardımcı script
"""

import sqlite3
import sys
from datetime import datetime

def get_all_users():
    """Tüm kullanıcıları listele"""
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id, username, balance, created_at FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()
    
    conn.close()
    
    print("\n" + "="*70)
    print("KULLANICILAR LİSTESİ")
    print("="*70)
    print(f"{'User ID':<15} {'Username':<20} {'Balance':<15} {'Created At'}")
    print("-"*70)
    
    for user in users:
        user_id, username, balance, created_at = user
        username = username or "N/A"
        print(f"{user_id:<15} {username:<20} ${balance:<14.2f} {created_at}")
    
    print("-"*70)
    print(f"Toplam kullanıcı: {len(users)}\n")

def add_balance(user_id, amount):
    """Kullanıcıya bakiye ekle"""
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    # Kullanıcının var olup olmadığını kontrol et
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    if not cursor.fetchone():
        print(f"❌ Kullanıcı bulunamadı: {user_id}")
        conn.close()
        return
    
    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    cursor.execute(
        'INSERT INTO transactions (user_id, transaction_type, amount, description) VALUES (?, ?, ?, ?)',
        (user_id, 'deposit', amount, 'Admin tarafından manuel yükleme')
    )
    
    conn.commit()
    
    # Güncel bakiyeyi göster
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    new_balance = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"✅ Bakiye eklendi!")
    print(f"   Kullanıcı: {user_id}")
    print(f"   Eklenen: ${amount:.2f}")
    print(f"   Yeni Bakiye: ${new_balance:.2f}")

def get_user_info(user_id):
    """Kullanıcı bilgilerini göster"""
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id, username, balance, created_at FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    if not user:
        print(f"❌ Kullanıcı bulunamadı: {user_id}")
        conn.close()
        return
    
    user_id, username, balance, created_at = user
    
    print("\n" + "="*50)
    print(f"KULLANICI BİLGİLERİ - {user_id}")
    print("="*50)
    print(f"Username: {username or 'N/A'}")
    print(f"Balance: ${balance:.2f}")
    print(f"Created: {created_at}")
    
    # İşlem geçmişi
    cursor.execute(
        'SELECT transaction_type, amount, description, created_at FROM transactions WHERE user_id = ? ORDER BY created_at DESC LIMIT 20',
        (user_id,)
    )
    transactions = cursor.fetchall()
    
    print("\nSon İşlemler:")
    print("-"*50)
    for trans in transactions:
        trans_type, amount, desc, created = trans
        emoji = "➕" if trans_type == "deposit" else "➖"
        print(f"{emoji} ${amount:.2f} - {desc}")
        print(f"   {created}")
    
    print("="*50 + "\n")
    
    conn.close()

def get_stats():
    """Genel istatistikleri göster"""
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    # Toplam kullanıcı
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    # Toplam bakiye
    cursor.execute('SELECT SUM(balance) FROM users')
    total_balance = cursor.fetchone()[0] or 0
    
    # Toplam işlem
    cursor.execute('SELECT COUNT(*) FROM transactions')
    total_transactions = cursor.fetchone()[0]
    
    # Toplam satış
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE transaction_type = "purchase"')
    total_sales = cursor.fetchone()[0] or 0
    
    # Toplam yükleme
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE transaction_type = "deposit"')
    total_deposits = cursor.fetchone()[0] or 0
    
    conn.close()
    
    print("\n" + "="*50)
    print("SİSTEM İSTATİSTİKLERİ")
    print("="*50)
    print(f"Toplam Kullanıcı: {total_users}")
    print(f"Toplam Bakiye: ${total_balance:.2f}")
    print(f"Toplam İşlem: {total_transactions}")
    print(f"Toplam Satış: ${total_sales:.2f}")
    print(f"Toplam Yükleme: ${total_deposits:.2f}")
    print(f"Net Gelir: ${total_sales - total_balance:.2f}")
    print("="*50 + "\n")

def print_help():
    """Yardım mesajını göster"""
    print("""
Admin Utility Script - Telegram Gift Card Bot

Kullanım:
    python admin.py [komut] [parametreler]

Komutlar:
    users                   - Tüm kullanıcıları listele
    user <user_id>          - Kullanıcı bilgilerini göster
    add <user_id> <amount>  - Kullanıcıya bakiye ekle
    stats                   - Genel istatistikleri göster
    help                    - Bu yardım mesajını göster

Örnekler:
    python admin.py users
    python admin.py user 123456789
    python admin.py add 123456789 100.50
    python admin.py stats
    """)

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'users':
        get_all_users()
    elif command == 'user':
        if len(sys.argv) < 3:
            print("❌ Kullanıcı ID'si gerekli!")
            print("Kullanım: python admin.py user <user_id>")
            return
        user_id = int(sys.argv[2])
        get_user_info(user_id)
    elif command == 'add':
        if len(sys.argv) < 4:
            print("❌ Kullanıcı ID'si ve miktar gerekli!")
            print("Kullanım: python admin.py add <user_id> <amount>")
            return
        user_id = int(sys.argv[2])
        amount = float(sys.argv[3])
        add_balance(user_id, amount)
    elif command == 'stats':
        get_stats()
    elif command == 'help':
        print_help()
    else:
        print(f"❌ Bilinmeyen komut: {command}")
        print_help()

if __name__ == '__main__':
    main()
