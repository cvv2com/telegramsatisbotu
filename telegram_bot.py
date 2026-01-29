#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MC/Visa Gift Card Bot - Telegram Bot Implementation
Versiyon 3.0 - Adet bazlı sipariş sistemi + Crypto Payment System
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
from database import GiftCardDB
from translations import get_text
from config import BOT_TOKEN, ADMIN_IDS, GIFT_CARD_CONFIG, CRYPTO_WALLETS, PAYMENT_CONFIG
from payment_handler import PaymentHandler
from timeout_handler import TimeoutHandler
import config as app_config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db = GiftCardDB('gift_cards.db.json')

# Initialize payment handler
payment_handler = PaymentHandler(db, app_config.__dict__)

# Conversation states
SELECTING_CARD_TYPE, ENTERING_QUANTITY, CONFIRMING_PURCHASE, ENTERING_BALANCE = range(4)
SELECTING_CURRENCY, ENTERING_PAYMENT_AMOUNT, ENTERING_TX_HASH = range(4, 7)

# Callback data prefixes
CARD_TYPE_PREFIX = "card_type:"
CONFIRM_PREFIX = "confirm:"
CURRENCY_PREFIX = "currency:"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user = update.effective_user
    user_id = user.id
    
    # Get user language
    lang = db.get_user_language(user_id)
    
    # Welcome message
    welcome_text = get_text('welcome', lang, name=user.first_name)
    
    # Main menu keyboard
    keyboard = [
        [InlineKeyboardButton(get_text('view_balance', lang), callback_data='view_balance')],
        [InlineKeyboardButton(get_text('create_payment', lang), callback_data='create_payment')],
        [InlineKeyboardButton(get_text('buy_cards', lang), callback_data='buy_cards')],
        [InlineKeyboardButton(get_text('my_purchases', lang), callback_data='my_purchases')],
        [InlineKeyboardButton(get_text('language', lang), callback_data='language')]
    ]
    
    # Add admin panel button for admins
    if user_id in ADMIN_IDS:
        keyboard.append([InlineKeyboardButton(get_text('admin_panel', lang), callback_data='admin')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def view_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View balance handler"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    balance = db.get_user_balance(user_id)
    balance_text = get_text('current_balance', lang, balance=balance)
    
    if balance < GIFT_CARD_CONFIG['minimum_balance']:
        balance_text += "\n\n" + get_text('minimum_balance_required', lang)
    
    keyboard = [
        [InlineKeyboardButton(get_text('add_balance', lang), callback_data='add_balance')],
        [InlineKeyboardButton(get_text('back', lang), callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(balance_text, reply_markup=reply_markup, parse_mode='Markdown')

async def add_balance_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start adding balance"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    text = get_text('enter_amount', lang)
    await query.edit_message_text(text, parse_mode='Markdown')
    
    return ENTERING_BALANCE

async def add_balance_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process balance addition"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    try:
        amount = float(update.message.text)
        if amount < GIFT_CARD_CONFIG['minimum_balance']:
            await update.message.reply_text(get_text('invalid_amount', lang))
            return ENTERING_BALANCE
        
        # Add balance (in real implementation, this would require payment verification)
        db.add_balance(user_id, amount)
        new_balance = db.get_user_balance(user_id)
        
        text = get_text('balance_added', lang, balance=new_balance)
        await update.message.reply_text(text, parse_mode='Markdown')
        
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(get_text('invalid_amount', lang))
        return ENTERING_BALANCE

async def buy_cards_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start buying cards - show card types"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    # Check minimum balance
    balance = db.get_user_balance(user_id)
    if balance < GIFT_CARD_CONFIG['minimum_balance']:
        text = get_text('balance_too_low', lang)
        keyboard = [[InlineKeyboardButton(get_text('add_balance', lang), callback_data='add_balance')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return ConversationHandler.END
    
    # Show card types
    text = get_text('select_card_type', lang)
    keyboard = [
        [InlineKeyboardButton(get_text('mc_numeric', lang), callback_data=f'{CARD_TYPE_PREFIX}mc_numeric')],
        [InlineKeyboardButton(get_text('visa_numeric', lang), callback_data=f'{CARD_TYPE_PREFIX}visa_numeric')],
        [InlineKeyboardButton(get_text('mc_picture', lang), callback_data=f'{CARD_TYPE_PREFIX}mc_picture')],
        [InlineKeyboardButton(get_text('visa_picture', lang), callback_data=f'{CARD_TYPE_PREFIX}visa_picture')],
        [InlineKeyboardButton(get_text('back', lang), callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return SELECTING_CARD_TYPE

async def card_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle card type selection"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    # Extract card type from callback data
    card_type = query.data.replace(CARD_TYPE_PREFIX, '')
    context.user_data['card_type'] = card_type
    
    # Get price based on card type
    if card_type in ['mc_numeric', 'visa_numeric']:
        price = GIFT_CARD_CONFIG['numeric_card_price']
    else:
        price = GIFT_CARD_CONFIG['picture_card_price']
    
    balance = db.get_user_balance(user_id)
    
    # Get card type name
    card_type_name = get_text(card_type, lang)
    
    text = get_text('enter_quantity', lang, card_type=card_type_name, price=price, balance=balance)
    await query.edit_message_text(text, parse_mode='Markdown')
    
    return ENTERING_QUANTITY

async def quantity_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quantity input"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            await update.message.reply_text(get_text('invalid_quantity', lang))
            return ENTERING_QUANTITY
        
        context.user_data['quantity'] = quantity
        card_type = context.user_data['card_type']
        
        # Calculate price
        if card_type in ['mc_numeric', 'visa_numeric']:
            price_per_card = GIFT_CARD_CONFIG['numeric_card_price']
        else:
            price_per_card = GIFT_CARD_CONFIG['picture_card_price']
        
        total_price = price_per_card * quantity
        balance = db.get_user_balance(user_id)
        remaining = balance - total_price
        
        # Check if user has enough balance
        if total_price > balance:
            shortage = total_price - balance
            text = get_text('insufficient_balance', lang, required=total_price, available=balance, shortage=shortage)
            await update.message.reply_text(text, parse_mode='Markdown')
            return ConversationHandler.END
        
        # Get card type name
        card_type_name = get_text(card_type, lang)
        
        # Show confirmation
        text = get_text('purchase_confirmation', lang, 
                       card_type=card_type_name,
                       quantity=quantity,
                       total=total_price,
                       remaining=remaining)
        
        keyboard = [
            [InlineKeyboardButton(get_text('confirm', lang), callback_data=f'{CONFIRM_PREFIX}yes')],
            [InlineKeyboardButton(get_text('cancel', lang), callback_data=f'{CONFIRM_PREFIX}no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return CONFIRMING_PURCHASE
        
    except ValueError:
        await update.message.reply_text(get_text('invalid_quantity', lang))
        return ENTERING_QUANTITY

async def purchase_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle purchase confirmation"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    # Check if user confirmed
    if query.data == f'{CONFIRM_PREFIX}no':
        text = get_text('purchase_cancelled', lang)
        await query.edit_message_text(text)
        context.user_data.clear()  # Clean up context
        return ConversationHandler.END
    
    # Get purchase details from context
    card_type = context.user_data['card_type']
    quantity = context.user_data['quantity']
    
    # Process purchase
    success, message, purchased_cards = db.purchase_cards_by_quantity(user_id, card_type, quantity)
    
    if not success:
        await query.edit_message_text(f"❌ {message}")
        context.user_data.clear()  # Clean up context
        return ConversationHandler.END
    
    # Get remaining balance
    balance = db.get_user_balance(user_id)
    
    # Calculate total amount
    if card_type in ['mc_numeric', 'visa_numeric']:
        price_per_card = GIFT_CARD_CONFIG['numeric_card_price']
    else:
        price_per_card = GIFT_CARD_CONFIG['picture_card_price']
    
    total_amount = price_per_card * quantity
    
    # Get card type name
    card_type_name = get_text(card_type, lang)
    
    # Build success message
    text = get_text('purchase_success', lang, 
                   quantity=quantity,
                   card_type=card_type_name,
                   amount=total_amount,
                   balance=balance)
    
    # Add card details
    for idx, card in enumerate(purchased_cards, 1):
        if card_type in ['mc_picture', 'visa_picture']:
            images = db.get_card_images(card)
            text += get_text('card_details_picture', lang,
                           index=idx,
                           card_number=card['card_number'],
                           exp_date=card['exp_date'],
                           pin=card['pin'],
                           front=images['front'] or 'N/A',
                           back=images['back'] or 'N/A')
        else:
            text += get_text('card_details', lang,
                           index=idx,
                           card_number=card['card_number'],
                           exp_date=card['exp_date'],
                           pin=card['pin'])
    
    await query.edit_message_text(text, parse_mode='Markdown')
    
    # Clear context
    context.user_data.clear()
    
    return ConversationHandler.END

async def my_purchases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's purchase history"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    purchases = db.get_user_purchases(user_id)
    
    if not purchases:
        text = get_text('no_purchases', lang)
    else:
        text = get_text('purchases_title', lang, count=len(purchases))
        
        for purchase in purchases[:10]:  # Show last 10 purchases
            card_number = purchase.get('card_number', '')
            last4 = card_number[-4:] if len(card_number) >= 4 else '****'
            
            text += get_text('purchase_item', lang,
                           name=purchase['card_name'],
                           last4=last4,
                           date=purchase['purchased_at'][:10],
                           price=purchase['amount'])
    
    keyboard = [[InlineKeyboardButton(get_text('back', lang), callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # Check if user is admin
    if user_id not in ADMIN_IDS:
        text = get_text('unauthorized', 'tr')
        await query.edit_message_text(text)
        return
    
    lang = db.get_user_language(user_id)
    
    # Get statistics
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
    
    all_cards = db.get_all_cards()
    revenue = sum(c['price'] for c in all_cards if c['status'] == 'sold')
    
    text = get_text('admin_stats', lang,
                   mc_numeric_available=mc_numeric_available,
                   mc_numeric_sold=mc_numeric_sold,
                   visa_numeric_available=visa_numeric_available,
                   visa_numeric_sold=visa_numeric_sold,
                   mc_picture_available=mc_picture_available,
                   mc_picture_sold=mc_picture_sold,
                   visa_picture_available=visa_picture_available,
                   visa_picture_sold=visa_picture_sold,
                   revenue=revenue)
    
    keyboard = [[InlineKeyboardButton(get_text('back', lang), callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def language_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Language selection"""
    query = update.callback_query
    await query.answer()
    
    text = get_text('select_language', 'tr')
    keyboard = [
        [InlineKeyboardButton("🇹🇷 Türkçe", callback_data='lang:tr')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang:en')],
        [InlineKeyboardButton(get_text('back', 'tr'), callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def language_changed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language change"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    lang = query.data.split(':')[1]
    
    db.set_user_language(user_id, lang)
    
    text = get_text('language_changed', lang)
    await query.edit_message_text(text)

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to main menu"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    user_id = user.id
    lang = db.get_user_language(user_id)
    
    welcome_text = get_text('welcome', lang, name=user.first_name)
    
    keyboard = [
        [InlineKeyboardButton(get_text('view_balance', lang), callback_data='view_balance')],
        [InlineKeyboardButton(get_text('create_payment', lang), callback_data='create_payment')],
        [InlineKeyboardButton(get_text('buy_cards', lang), callback_data='buy_cards')],
        [InlineKeyboardButton(get_text('my_purchases', lang), callback_data='my_purchases')],
        [InlineKeyboardButton(get_text('language', lang), callback_data='language')]
    ]
    
    if user_id in ADMIN_IDS:
        keyboard.append([InlineKeyboardButton(get_text('admin_panel', lang), callback_data='admin')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    text = get_text('help', lang)
    await update.message.reply_text(text, parse_mode='Markdown')

# Payment system commands

async def create_payment_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start creating a payment"""
    query = update.callback_query
    if query:
        await query.answer()
    
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    # Show currency selection
    text = get_text('select_currency', lang)
    keyboard = []
    
    for currency in ['BTC', 'ETH', 'USDT', 'LTC']:
        if currency.lower() in CRYPTO_WALLETS:
            keyboard.append([InlineKeyboardButton(
                f"💰 {currency}",
                callback_data=f'{CURRENCY_PREFIX}{currency.lower()}'
            )])
    
    keyboard.append([InlineKeyboardButton(get_text('back', lang), callback_data='back_to_main')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    return SELECTING_CURRENCY

async def currency_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle currency selection"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    # Extract currency from callback data
    currency = query.data.replace(CURRENCY_PREFIX, '')
    context.user_data['payment_currency'] = currency
    
    # Ask for amount
    text = get_text('enter_payment_amount', lang)
    await query.edit_message_text(text, parse_mode='Markdown')
    
    return ENTERING_PAYMENT_AMOUNT

async def payment_amount_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle payment amount input"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    try:
        amount = float(update.message.text)
        
        # Validate amount
        min_amount = PAYMENT_CONFIG.get('minimum_payment_usd', 20.0)
        max_amount = PAYMENT_CONFIG.get('maximum_payment_usd', 10000.0)
        
        if amount < min_amount or amount > max_amount:
            text = get_text('invalid_payment_amount', lang, min=min_amount, max=max_amount)
            await update.message.reply_text(text, parse_mode='Markdown')
            return ENTERING_PAYMENT_AMOUNT
        
        currency = context.user_data.get('payment_currency', 'btc')
        
        # For demo purposes, use fixed exchange rates
        # In production, fetch real-time rates from an API
        exchange_rates = {
            'btc': 42500.0,
            'eth': 2200.0,
            'usdt': 1.0,
            'ltc': 65.0
        }
        
        exchange_rate = exchange_rates.get(currency, 1.0)
        
        # Create payment
        success, message, tx_id = payment_handler.create_payment(
            user_id=user_id,
            usd_amount=amount,
            currency=currency.upper(),
            exchange_rate=exchange_rate
        )
        
        if not success:
            text = get_text('payment_creation_error', lang, error=message)
            await update.message.reply_text(text, parse_mode='Markdown')
            return ConversationHandler.END
        
        # Get payment instructions
        instructions = payment_handler.get_payment_instructions(tx_id, lang)
        
        if instructions:
            text = get_text('payment_instructions', lang,
                          usd=instructions['usd_amount'],
                          crypto=instructions['crypto_amount_formatted'],
                          currency=instructions['currency'],
                          wallet=instructions['wallet_address'],
                          timeout=instructions['timeout_minutes'],
                          network=instructions['network_name'],
                          confirmations=instructions['required_confirmations'])
            
            text += f"\n\n{get_text('payment_created', lang, tx_id=tx_id)}"
            text += f"\n\n{get_text('enter_tx_hash', lang)}"
            
            # Store transaction ID for later
            context.user_data['current_payment_tx_id'] = tx_id
            
            await update.message.reply_text(text, parse_mode='Markdown')
            return ENTERING_TX_HASH
        else:
            await update.message.reply_text("Error getting payment instructions", parse_mode='Markdown')
            return ConversationHandler.END
        
    except ValueError:
        text = get_text('invalid_amount', lang)
        await update.message.reply_text(text, parse_mode='Markdown')
        return ENTERING_PAYMENT_AMOUNT

async def tx_hash_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle TX hash input"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    tx_hash = update.message.text.strip()
    tx_id = context.user_data.get('current_payment_tx_id')
    
    if not tx_id:
        await update.message.reply_text("Error: No payment transaction found", parse_mode='Markdown')
        return ConversationHandler.END
    
    # Get transaction
    tx = db.get_transaction_by_id(tx_id)
    if not tx:
        await update.message.reply_text("Error: Transaction not found", parse_mode='Markdown')
        return ConversationHandler.END
    
    # Validate TX hash
    is_valid, message = payment_handler.validate_payment(tx_hash, tx['currency'])
    
    if not is_valid:
        await update.message.reply_text(f"❌ {message}", parse_mode='Markdown')
        return ENTERING_TX_HASH
    
    # Update transaction with TX hash (but keep it pending for admin confirmation)
    db.update_transaction_status(tx_id, 'pending', tx_hash=tx_hash)
    
    text = (
        f"✅ Transaction hash received!\n\n"
        f"Your payment is being verified. You will be notified once it's confirmed.\n\n"
        f"Transaction ID: #{tx_id}\n"
        f"TX Hash: `{tx_hash[:16]}...`"
    )
    
    await update.message.reply_text(text, parse_mode='Markdown')
    
    # Clear context
    context.user_data.pop('current_payment_tx_id', None)
    context.user_data.pop('payment_currency', None)
    
    return ConversationHandler.END

async def payment_status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check payment status"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    # Get user's pending transactions
    pending = db.get_user_transactions(user_id, status='pending')
    
    if not pending:
        text = "✅ No pending payments."
        await update.message.reply_text(text, parse_mode='Markdown')
        return
    
    # Show pending transactions
    text = "⏳ **Pending Payments:**\n\n"
    
    for tx in pending[:5]:  # Show last 5
        message = payment_handler.format_transaction_message(tx['id'], lang)
        if message:
            text += message + "\n\n━━━━━━━━━━━━━━━━━━\n\n"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def payment_history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View payment history"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    
    transactions = db.get_user_transactions(user_id)
    
    if not transactions:
        text = get_text('no_payment_history', lang)
        await update.message.reply_text(text, parse_mode='Markdown')
        return
    
    text = get_text('payment_history_title', lang)
    
    for tx in transactions[:10]:  # Show last 10
        text += get_text('payment_history_item', lang,
                        id=tx['id'],
                        currency=tx['currency'],
                        status=tx['status'],
                        amount=tx['amount'],
                        usd=tx.get('usd_equivalent', 0),
                        date=tx['created_at'][:10])
    
    await update.message.reply_text(text, parse_mode='Markdown')

# Admin payment commands

async def admin_pending_payments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: View pending payments"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text(get_text('unauthorized', 'tr'))
        return
    
    lang = db.get_user_language(user_id)
    
    pending = db.get_pending_transactions()
    
    if not pending:
        text = get_text('no_pending_payments', lang)
        await update.message.reply_text(text, parse_mode='Markdown')
        return
    
    text = get_text('pending_payments_title', lang)
    
    for tx in pending[:10]:  # Show last 10
        text += get_text('pending_payment_item', lang,
                        id=tx['id'],
                        user_id=tx['user_id'],
                        amount=tx['amount'],
                        currency=tx['currency'],
                        usd=tx.get('usd_equivalent', 0),
                        date=tx['created_at'][:19],
                        timeout=tx['timeout_at'][:19])
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def admin_confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: Confirm payment"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text(get_text('unauthorized', 'tr'))
        return
    
    lang = db.get_user_language(user_id)
    
    if not context.args:
        text = get_text('confirm_payment_usage', lang)
        await update.message.reply_text(text, parse_mode='Markdown')
        return
    
    tx_hash = context.args[0]
    
    # Find transaction
    tx = db.get_transaction_by_hash(tx_hash)
    if not tx:
        text = get_text('payment_not_found', lang)
        await update.message.reply_text(text, parse_mode='Markdown')
        return
    
    # Confirm payment
    success, message = payment_handler.confirm_payment(tx['id'], tx_hash)
    
    if success:
        text = f"✅ {message}"
    else:
        text = f"❌ {message}"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def admin_refund_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: Refund/cancel payment"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text(get_text('unauthorized', 'tr'))
        return
    
    lang = db.get_user_language(user_id)
    
    if len(context.args) < 2:
        text = get_text('refund_payment_usage', lang)
        await update.message.reply_text(text, parse_mode='Markdown')
        return
    
    try:
        tx_id = int(context.args[0])
        reason = ' '.join(context.args[1:])
    except ValueError:
        await update.message.reply_text("Invalid transaction ID", parse_mode='Markdown')
        return
    
    # Cancel payment
    success, message = payment_handler.cancel_payment(tx_id, reason)
    
    if success:
        text = f"✅ {message}"
    else:
        text = f"❌ {message}"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def admin_payment_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: View payment statistics"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text(get_text('unauthorized', 'tr'))
        return
    
    lang = db.get_user_language(user_id)
    
    stats = db.get_payment_stats()
    
    text = get_text('payment_stats', lang,
                   total=stats['total'],
                   pending=stats['pending'],
                   confirmed=stats['confirmed'],
                   failed=stats['failed'],
                   timeout=stats['timeout'],
                   volume=stats['total_volume_usd'])
    
    await update.message.reply_text(text, parse_mode='Markdown')


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    context.user_data.clear()
    return ConversationHandler.END

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Initialize timeout handler
    timeout_handler = TimeoutHandler(db, application, check_interval_minutes=PAYMENT_CONFIG.get('check_interval_minutes', 5))
    
    # Add conversation handler for buying cards
    buy_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(buy_cards_start, pattern='^buy_cards$')],
        states={
            SELECTING_CARD_TYPE: [CallbackQueryHandler(card_type_selected, pattern=f'^{CARD_TYPE_PREFIX}')],
            ENTERING_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, quantity_entered)],
            CONFIRMING_PURCHASE: [CallbackQueryHandler(purchase_confirmed, pattern=f'^{CONFIRM_PREFIX}')],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Add conversation handler for adding balance
    balance_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_balance_start, pattern='^add_balance$')],
        states={
            ENTERING_BALANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_balance_amount)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Add conversation handler for creating payment
    payment_conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(create_payment_start, pattern='^create_payment$'),
            CommandHandler('create_payment', create_payment_start)
        ],
        states={
            SELECTING_CURRENCY: [CallbackQueryHandler(currency_selected, pattern=f'^{CURRENCY_PREFIX}')],
            ENTERING_PAYMENT_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, payment_amount_entered)],
            ENTERING_TX_HASH: [MessageHandler(filters.TEXT & ~filters.COMMAND, tx_hash_entered)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(buy_conv_handler)
    application.add_handler(balance_conv_handler)
    application.add_handler(payment_conv_handler)
    application.add_handler(CallbackQueryHandler(view_balance, pattern='^view_balance$'))
    application.add_handler(CallbackQueryHandler(my_purchases, pattern='^my_purchases$'))
    application.add_handler(CallbackQueryHandler(admin_panel, pattern='^admin$'))
    application.add_handler(CallbackQueryHandler(language_select, pattern='^language$'))
    application.add_handler(CallbackQueryHandler(language_changed, pattern='^lang:'))
    application.add_handler(CallbackQueryHandler(back_to_main, pattern='^back_to_main$'))
    
    # Payment commands
    application.add_handler(CommandHandler("payment_status", payment_status_command))
    application.add_handler(CommandHandler("payment_history", payment_history_command))
    
    # Admin payment commands
    application.add_handler(CommandHandler("pending_payments", admin_pending_payments))
    application.add_handler(CommandHandler("confirm_payment", admin_confirm_payment))
    application.add_handler(CommandHandler("refund_payment", admin_refund_payment))
    application.add_handler(CommandHandler("admin_payments", admin_payment_stats))
    
    # Start bot
    logger.info("Starting MC/Visa Gift Card Bot with Crypto Payment System...")
    application.run_polling()

if __name__ == '__main__':
    main()
