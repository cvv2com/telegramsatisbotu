#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MC/Visa Gift Card Bot - Telegram Bot Implementation
Versiyon 3.0 - Adet bazlı sipariş sistemi
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
from config import BOT_TOKEN, ADMIN_IDS, GIFT_CARD_CONFIG

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db = GiftCardDB('gift_cards.db.json')

# Conversation states
SELECTING_CARD_TYPE, ENTERING_QUANTITY, CONFIRMING_PURCHASE, ENTERING_BALANCE = range(4)

# Callback data prefixes
CARD_TYPE_PREFIX = "card_type:"
CONFIRM_PREFIX = "confirm:"

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

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    context.user_data.clear()
    return ConversationHandler.END

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
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
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(buy_conv_handler)
    application.add_handler(balance_conv_handler)
    application.add_handler(CallbackQueryHandler(view_balance, pattern='^view_balance$'))
    application.add_handler(CallbackQueryHandler(my_purchases, pattern='^my_purchases$'))
    application.add_handler(CallbackQueryHandler(admin_panel, pattern='^admin$'))
    application.add_handler(CallbackQueryHandler(language_select, pattern='^language$'))
    application.add_handler(CallbackQueryHandler(language_changed, pattern='^lang:'))
    application.add_handler(CallbackQueryHandler(back_to_main, pattern='^back_to_main$'))
    
    # Start bot
    logger.info("Starting MC/Visa Gift Card Bot...")
    application.run_polling()

if __name__ == '__main__':
    main()
