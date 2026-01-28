"""
Main bot file
Telegram Gift Card Sales Bot
"""
import logging
import json
import csv
import io
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes, ConversationHandler
)

import config
from database import GiftCardDB
from translations import get_text

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Database
db = GiftCardDB(config.DATABASE_FILE)

# Conversation states
AWAITING_FILE, AWAITING_COUPON, AWAITING_PAYMENT = range(3)


def get_main_menu_keyboard(is_admin_user: bool, lang: str = 'tr'):
    """Create main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_text('view_cards', lang), callback_data='view_cards')],
        [InlineKeyboardButton(get_text('categories', lang), callback_data='categories')],
        [InlineKeyboardButton(get_text('my_orders', lang), callback_data='my_orders')],
    ]
    
    if is_admin_user:
        keyboard.append([InlineKeyboardButton(get_text('admin_panel', lang), callback_data='admin_panel')])
    
    keyboard.append([InlineKeyboardButton(get_text('language', lang), callback_data='language')])
    
    return InlineKeyboardMarkup(keyboard)


def get_welcome_text(user_first_name: str, lang: str = 'tr') -> str:
    """Create welcome message"""
    return get_text('welcome', lang, name=user_first_name)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start command handler"""
    user = update.effective_user
    is_admin_user = user.id in config.ADMIN_IDS
    lang = db.get_user_language(user.id)
    
    reply_markup = get_main_menu_keyboard(is_admin_user, lang)
    welcome_text = get_welcome_text(user.first_name, lang)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in config.ADMIN_IDS


async def add_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add new card (Admin only)"""
    user = update.effective_user
    lang = db.get_user_language(user.id)
    
    if not is_admin(user.id):
        await update.message.reply_text(get_text('unauthorized', lang))
        return

    # Usage: /addcard Name | Description | Price | Category | Code | Stock
    try:
        # Get the full message text after the command
        args_text = update.message.text.replace('/addcard', '').strip()
        
        if not args_text:
            raise ValueError("Empty arguments")
            
        parts = [p.strip() for p in args_text.split('|')]
        
        if len(parts) < 5 or len(parts) > 6:
            await update.message.reply_text(
                get_text('addcard_format_error', lang),
                parse_mode='Markdown'
            )
            return

        name = parts[0]
        description = parts[1]
        price_str = parts[2]
        category = parts[3]
        code = parts[4]
        stock = int(parts[5]) if len(parts) == 6 else 1
        
        price = float(price_str)
        
        # Add to DB
        card_id = db.add_gift_card(name, description, price, category, code, stock=stock)
        
        await update.message.reply_text(
            get_text('addcard_success', lang, 
                    name=name, price=price, currency=config.CURRENCY, 
                    stock=stock, id=card_id),
            parse_mode='Markdown'
        )
        
    except ValueError:
        await update.message.reply_text(get_text('addcard_price_error', lang))
    except Exception as e:
        logger.error(f"Error adding card: {e}")
        await update.message.reply_text(get_text('addcard_error', lang))


async def delete_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a card (Admin only)"""
    user = update.effective_user
    lang = db.get_user_language(user.id)
    
    if not is_admin(user.id):
        await update.message.reply_text(get_text('unauthorized', lang))
        return

    try:
        # Usage: /deletecard 1
        if not context.args:
            raise ValueError("No ID provided")
            
        card_id = int(context.args[0])
        success = db.delete_gift_card(card_id)
        
        if success:
            await update.message.reply_text(get_text('deletecard_success', lang, id=card_id))
        else:
            await update.message.reply_text(get_text('deletecard_not_found', lang, id=card_id))
            
    except (IndexError, ValueError):
        await update.message.reply_text(get_text('deletecard_format_error', lang), parse_mode='Markdown')


async def bulk_add_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bulk add cards from CSV/JSON (Admin only)"""
    user = update.effective_user
    lang = db.get_user_language(user.id)
    
    if not is_admin(user.id):
        await update.message.reply_text(get_text('unauthorized', lang))
        return
    
    # Send instructions
    await update.message.reply_text(get_text('bulkaddcard_usage', lang), parse_mode='Markdown')


async def handle_bulk_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle bulk file upload"""
    user = update.effective_user
    lang = db.get_user_language(user.id)
    
    if not is_admin(user.id):
        return
    
    try:
        # Get the file
        document = update.message.document
        if not document:
            return
        
        file = await context.bot.get_file(document.file_id)
        file_content = await file.download_as_bytearray()
        file_text = file_content.decode('utf-8')
        
        cards_data = []
        
        # Try JSON first
        if document.file_name.endswith('.json'):
            cards_data = json.loads(file_text)
        # Try CSV
        elif document.file_name.endswith('.csv'):
            csv_reader = csv.DictReader(io.StringIO(file_text))
            cards_data = list(csv_reader)
        else:
            await update.message.reply_text(get_text('bulkaddcard_send_file', lang))
            return
        
        # Bulk add
        success_count, errors = db.bulk_add_cards(cards_data)
        
        # Report results
        result_msg = get_text('bulkaddcard_success', lang, 
                             success=success_count, errors=len(errors))
        
        if errors:
            error_list = '\n'.join(errors[:10])  # Show first 10 errors
            result_msg += get_text('bulkaddcard_errors', lang, error_list=error_list)
        
        await update.message.reply_text(result_msg)
        
    except Exception as e:
        logger.error(f"Error in bulk add: {e}")
        await update.message.reply_text(get_text('bulkaddcard_error', lang, error=str(e)))


async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's order history"""
    user = update.effective_user
    lang = db.get_user_language(user.id)
    
    orders = db.get_user_orders(user.id)
    
    if not orders:
        await update.message.reply_text(get_text('no_orders', lang))
        return
    
    # Build order list
    text = get_text('my_orders_title', lang)
    
    for order in orders[:10]:  # Show last 10 orders
        date = datetime.fromisoformat(order['timestamp']).strftime('%Y-%m-%d %H:%M')
        text += get_text('order_item', lang,
                        name=order['card_name'],
                        price=order['amount'],
                        currency=config.CURRENCY,
                        date=date)
    
    keyboard = [[InlineKeyboardButton(get_text('main_menu', lang), callback_data='main_menu')]]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def add_coupon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a discount coupon (Admin only)"""
    user = update.effective_user
    lang = db.get_user_language(user.id)
    
    if not is_admin(user.id):
        await update.message.reply_text(get_text('unauthorized', lang))
        return
    
    try:
        # Usage: /addcoupon CODE | TYPE | VALUE | MAX_USES | DAYS
        args_text = update.message.text.replace('/addcoupon', '').strip()
        
        if not args_text:
            await update.message.reply_text(get_text('addcoupon_usage', lang), parse_mode='Markdown')
            return
        
        parts = [p.strip() for p in args_text.split('|')]
        
        if len(parts) < 3:
            await update.message.reply_text(get_text('addcoupon_usage', lang), parse_mode='Markdown')
            return
        
        code = parts[0]
        discount_type = parts[1]  # percentage or fixed
        discount_value = float(parts[2])
        max_uses = int(parts[3]) if len(parts) > 3 else None
        days = int(parts[4]) if len(parts) > 4 else None
        
        # Calculate expiration
        expires_at = None
        if days:
            expires_at = (datetime.now() + timedelta(days=days)).isoformat()
        
        # Add coupon
        coupon_id = db.add_coupon(code, discount_type, discount_value, max_uses, expires_at)
        
        discount_str = f"{discount_value}%" if discount_type == 'percentage' else f"{discount_value}{config.CURRENCY}"
        expires_str = f"{days} days" if days else "No expiration"
        max_uses_str = str(max_uses) if max_uses else "Unlimited"
        
        await update.message.reply_text(
            get_text('addcoupon_success', lang,
                    code=code, discount=discount_str,
                    max_uses=max_uses_str, expires=expires_str)
        )
        
    except Exception as e:
        logger.error(f"Error adding coupon: {e}")
        await update.message.reply_text(get_text('addcoupon_error', lang, error=str(e)))


async def delete_coupon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a coupon (Admin only)"""
    user = update.effective_user
    lang = db.get_user_language(user.id)
    
    if not is_admin(user.id):
        await update.message.reply_text(get_text('unauthorized', lang))
        return
    
    try:
        if not context.args:
            await update.message.reply_text("❌ Usage: `/deletecoupon <ID>`", parse_mode='Markdown')
            return
        
        coupon_id = int(context.args[0])
        success = db.delete_coupon(coupon_id)
        
        if success:
            await update.message.reply_text(f"✅ Coupon ID: {coupon_id} deleted successfully.")
        else:
            await update.message.reply_text(f"❌ Coupon ID: {coupon_id} not found.")
            
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Usage: `/deletecoupon <ID>`", parse_mode='Markdown')


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Language selection command"""
    user = update.effective_user
    lang = db.get_user_language(user.id)
    
    keyboard = [
        [InlineKeyboardButton("🇹🇷 Türkçe", callback_data='lang_tr')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
    ]
    
    await update.message.reply_text(
        get_text('select_language', lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    is_admin_user = is_admin(user_id)
    lang = db.get_user_language(user_id)
    
    if data == 'main_menu':
        await back_to_main(query, context)
    
    elif data.startswith('lang_'):
        # Language selection
        new_lang = data.split('_')[1]
        db.set_user_language(user_id, new_lang)
        await query.edit_message_text(
            get_text('language_changed', new_lang),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(get_text('main_menu', new_lang), callback_data='main_menu')
            ]])
        )
    
    elif data == 'language':
        # Show language selection
        keyboard = [
            [InlineKeyboardButton("🇹🇷 Türkçe", callback_data='lang_tr')],
            [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
            [InlineKeyboardButton(get_text('back', lang), callback_data='main_menu')]
        ]
        await query.edit_message_text(
            get_text('select_language', lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    elif data == 'my_orders':
        # Show user's orders
        orders = db.get_user_orders(user_id)
        
        if not orders:
            await query.edit_message_text(
                get_text('no_orders', lang),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(get_text('back', lang), callback_data='main_menu')
                ]])
            )
            return
        
        # Build order list
        text = get_text('my_orders_title', lang)
        
        for order in orders[:10]:  # Show last 10 orders
            date = datetime.fromisoformat(order['timestamp']).strftime('%Y-%m-%d %H:%M')
            text += get_text('order_item', lang,
                            name=order['card_name'],
                            price=order['amount'],
                            currency=config.CURRENCY,
                            date=date)
        
        keyboard = [[InlineKeyboardButton(get_text('back', lang), callback_data='main_menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif data == 'view_cards':
        # List all available cards
        cards = db.get_available_cards()
        if not cards:
            await query.edit_message_text(
                get_text('no_cards', lang),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(get_text('back', lang), callback_data='main_menu')
                ]])
            )
            return
            
        keyboard = []
        for card in cards:
            stock_info = f" (📦 {card.get('stock', 1)})" if card.get('stock', 1) > 1 else ""
            keyboard.append([InlineKeyboardButton(
                f"{card['name']} - {card['price']}{config.CURRENCY}{stock_info}", 
                callback_data=f"detail_{card['id']}"
            )])
        keyboard.append([InlineKeyboardButton(get_text('back', lang), callback_data='main_menu')])
        
        await query.edit_message_text(
            get_text('available_cards', lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    elif data == 'categories':
        # List categories
        categories = db.get_categories()
        if not categories:
            await query.edit_message_text(
                get_text('no_categories', lang),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(get_text('back', lang), callback_data='main_menu')
                ]])
            )
            return

        keyboard = []
        for cat in categories:
            keyboard.append([InlineKeyboardButton(cat, callback_data=f"cat_{cat}")])
        keyboard.append([InlineKeyboardButton(get_text('back', lang), callback_data='main_menu')])

        await query.edit_message_text(
            get_text('categories_list', lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    elif data.startswith('cat_'):
        # Filter by category
        category = data.split('_', 1)[1]
        cards = db.get_available_cards(category=category)
        
        if not cards:
            await query.edit_message_text(
                get_text('no_cards_in_category', lang, category=category),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(get_text('back', lang), callback_data='categories')
                ]]),
                parse_mode='Markdown'
            )
            return

        keyboard = []
        for card in cards:
            stock_info = f" (📦 {card.get('stock', 1)})" if card.get('stock', 1) > 1 else ""
            keyboard.append([InlineKeyboardButton(
                f"{card['name']} - {card['price']}{config.CURRENCY}{stock_info}", 
                callback_data=f"detail_{card['id']}"
            )])
        keyboard.append([InlineKeyboardButton(get_text('back', lang), callback_data='categories')])
        
        await query.edit_message_text(
            get_text('category_title', lang, category=category),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    elif data.startswith('detail_'):
        # Show card details
        card_id = int(data.split('_')[1])
        card = db.get_card(card_id)
        
        if not card or card['status'] != 'available':
            await query.edit_message_text(
                get_text('card_unavailable', lang),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(get_text('back', lang), callback_data='view_cards')
                ]])
            )
            return
            
        text = get_text('card_detail', lang,
                       name=card['name'],
                       description=card['description'],
                       category=card['category'],
                       price=card['price'],
                       currency=config.CURRENCY,
                       stock=card.get('stock', 1))
        
        keyboard = [
            [InlineKeyboardButton(get_text('buy_now', lang), callback_data=f"buy_{card_id}")],
            [InlineKeyboardButton(get_text('back', lang), callback_data='view_cards')]
        ]
        
        await query.edit_message_text(
            text, 
            reply_markup=InlineKeyboardMarkup(keyboard), 
            parse_mode='Markdown'
        )

    elif data.startswith('buy_'):
        # Buy process
        card_id = int(data.split('_')[1])
        card = db.get_card(card_id)
        
        if not card or card['status'] != 'available':
            await query.answer(get_text('card_unavailable_alert', lang), show_alert=True)
            return
        
        # Check stock
        if card.get('stock', 1) <= 0:
            await query.answer(get_text('out_of_stock', lang), show_alert=True)
            return
            
        # Process sale
        success = db.mark_as_sold(card_id, user_id)
        
        if success:
            # Add order record
            db.add_order(user_id, card_id, card['price'])
            
            # Decrease stock
            db.update_stock(card_id, -1)
            
            # Send code privately via spoiler
            code_text = f"||{card['code']}||"  # Spoiler format
            
            await query.edit_message_text(
                get_text('purchase_success', lang,
                        name=card['name'],
                        code=code_text),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(get_text('main_menu', lang), callback_data='main_menu')
                ]]),
                parse_mode='MarkdownV2' 
            )
            
            # Notify Admin
            for admin_id in config.ADMIN_IDS:
                try:
                    await context.bot.send_message(
                        chat_id=admin_id,
                        text=get_text('new_sale_admin', lang,
                                    user=query.from_user.first_name,
                                    item=card['name'],
                                    price=card['price'],
                                    currency=config.CURRENCY),
                        parse_mode='Markdown'
                    )
                except:
                    pass
            
            # Check for low stock and alert admin
            low_stock = db.check_low_stock(config.LOW_STOCK_THRESHOLD)
            if low_stock:
                cards_list = '\n'.join([f"- {c['name']} (Stock: {c.get('stock', 0)})" for c in low_stock])
                for admin_id in config.ADMIN_IDS:
                    try:
                        await context.bot.send_message(
                            chat_id=admin_id,
                            text=get_text('low_stock_alert', lang, cards=cards_list),
                            parse_mode='Markdown'
                        )
                    except:
                        pass
        else:
            await query.answer(get_text('purchase_error', lang), show_alert=True)

    elif data == 'admin_panel':
        if not is_admin_user:
            await query.answer(get_text('unauthorized_alert', lang), show_alert=True)
            return
            
        stats = db.get_stats()
        
        text = get_text('admin_stats', lang,
                       total=stats['total_cards'],
                       available=stats['available_cards'],
                       sold=stats['sold_cards'],
                       revenue=stats['total_revenue'],
                       currency=config.CURRENCY)
        
        keyboard = [[InlineKeyboardButton(get_text('main_menu', lang), callback_data='main_menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')


async def back_to_main(query, context):
    """Return to main menu helper"""
    user = query.from_user
    lang = db.get_user_language(user.id)
    reply_markup = get_main_menu_keyboard(is_admin(user.id), lang)
    welcome_text = get_welcome_text(user.first_name, lang)
    await query.edit_message_text(welcome_text, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/help command handler"""
    user = update.effective_user
    lang = db.get_user_language(user.id)
    
    help_text = get_text('help', lang)
    await update.message.reply_text(help_text, parse_mode='Markdown')


def main():
    """Main function"""
    # Create Application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Add Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addcard", add_card))
    application.add_handler(CommandHandler("deletecard", delete_card))
    application.add_handler(CommandHandler("bulkaddcard", bulk_add_card))
    application.add_handler(CommandHandler("myorders", my_orders))
    application.add_handler(CommandHandler("addcoupon", add_coupon))
    application.add_handler(CommandHandler("deletecoupon", delete_coupon))
    application.add_handler(CommandHandler("language", language_command))
    
    # File handler for bulk uploads
    application.add_handler(MessageHandler(filters.Document.ALL, handle_bulk_file))
    
    # Button handler
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start Bot
    print("Bot is running with multi-language support (TR/EN)...")
    print("New features: Stock management, Bulk add, Order history, Coupons, Payments")
    application.run_polling()


if __name__ == '__main__':
    main()
