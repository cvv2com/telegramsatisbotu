"""
Main bot file
Telegram Gift Card Sales Bot
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes
)

import config
from database import GiftCardDB

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Database
db = GiftCardDB(config.DATABASE_FILE)


def get_main_menu_keyboard(is_admin_user: bool):
    """Create main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🎁 View Gift Cards", callback_data='view_cards')],
        [InlineKeyboardButton("📂 Categories", callback_data='categories')],
    ]
    
    if is_admin_user:
        keyboard.append([InlineKeyboardButton("⚙️ Admin Panel", callback_data='admin_panel')])
    
    return InlineKeyboardMarkup(keyboard)


def get_welcome_text(user_first_name: str) -> str:
    """Create welcome message"""
    return f"""
🎉 Welcome {user_first_name}!

You can buy gift cards using this bot.

🎁 Use the buttons below to view Gift Cards.
📦 You can also browse by categories.
💳 Select the card you want and complete the purchase.

Use /help for more information.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start command handler"""
    user = update.effective_user
    is_admin_user = user.id in config.ADMIN_IDS
    
    reply_markup = get_main_menu_keyboard(is_admin_user)
    welcome_text = get_welcome_text(user.first_name)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in config.ADMIN_IDS


async def add_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add new card (Admin only)"""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("⛔ You are not authorized to use this command.")
        return

    # Usage: /addcard Name | Description | Price | Category | Code
    try:
        # Get the full message text after the command
        args_text = update.message.text.replace('/addcard', '').strip()
        
        if not args_text:
            raise ValueError("Empty arguments")
            
        parts = [p.strip() for p in args_text.split('|')]
        
        if len(parts) != 5:
            await update.message.reply_text(
                "❌ **Incorrect Format!**\n\n"
                "Usage:\n"
                "`/addcard Name | Description | Price | Category | Code`\n\n"
                "Example:\n"
                "`/addcard Netflix 10$ | 1 Month Sub | 10 | Entertainment | NF-12345`",
                parse_mode='Markdown'
            )
            return

        name, description, price_str, category, code = parts
        price = float(price_str)
        
        # Add to DB
        card_id = db.add_gift_card(name, description, price, category, code)
        
        await update.message.reply_text(
            f"✅ **Gift card added successfully!**\n\n"
            f"🎁 {name}\n"
            f"💰 {price}{config.CURRENCY}\n"
            f"ID: {card_id}",
            parse_mode='Markdown'
        )
        
    except ValueError:
        await update.message.reply_text("❌ Price must be a number (e.g., 10 or 10.5)")
    except Exception as e:
        logger.error(f"Error adding card: {e}")
        await update.message.reply_text("❌ An error occurred while adding the card.")


async def delete_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a card (Admin only)"""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("⛔ You are not authorized.")
        return

    try:
        # Usage: /deletecard 1
        if not context.args:
            raise ValueError("No ID provided")
            
        card_id = int(context.args[0])
        success = db.delete_gift_card(card_id)
        
        if success:
            await update.message.reply_text(f"✅ Card ID: {card_id} deleted successfully.")
        else:
            await update.message.reply_text(f"❌ Card ID: {card_id} not found.")
            
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Usage: `/deletecard <ID>`", parse_mode='Markdown')


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    is_admin_user = is_admin(user_id)
    
    if data == 'main_menu':
        await back_to_main(query, context)
        
    elif data == 'view_cards':
        # List all available cards
        cards = db.get_available_cards()
        if not cards:
            await query.edit_message_text(
                "😔 No gift cards available at the moment.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data='main_menu')]])
            )
            return
            
        keyboard = []
        for card in cards:
            keyboard.append([InlineKeyboardButton(
                f"{card['name']} - {card['price']}{config.CURRENCY}", 
                callback_data=f"detail_{card['id']}"
            )])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='main_menu')])
        
        await query.edit_message_text(
            "🎁 **Available Gift Cards:**\nSelect one to see details.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    elif data == 'categories':
        # List categories
        categories = db.get_categories()
        if not categories:
            await query.edit_message_text(
                "😔 No categories found.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data='main_menu')]])
            )
            return

        keyboard = []
        for cat in categories:
            keyboard.append([InlineKeyboardButton(cat, callback_data=f"cat_{cat}")])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='main_menu')])

        await query.edit_message_text(
            "📂 **Categories:**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    elif data.startswith('cat_'):
        # Filter by category
        category = data.split('_', 1)[1]
        cards = db.get_available_cards(category=category)
        
        if not cards:
            await query.edit_message_text(
                f"😔 No cards found in **{category}** category.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data='categories')]]),
                parse_mode='Markdown'
            )
            return

        keyboard = []
        for card in cards:
            keyboard.append([InlineKeyboardButton(
                f"{card['name']} - {card['price']}{config.CURRENCY}", 
                callback_data=f"detail_{card['id']}"
            )])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='categories')])
        
        await query.edit_message_text(
            f"📂 Category: **{category}**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    elif data.startswith('detail_'):
        # Show card details
        card_id = int(data.split('_')[1])
        card = db.get_card(card_id)
        
        if not card or card['status'] != 'available':
            await query.edit_message_text(
                "❌ This card is no longer available.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data='view_cards')]])
            )
            return
            
        text = f"""
🎁 *{card['name']}*

📝 {card['description']}

📂 Category: {card['category']}
💰 Price: *{card['price']}{config.CURRENCY}*
"""
        keyboard = [
            [InlineKeyboardButton("💳 Buy Now", callback_data=f"buy_{card_id}")],
            [InlineKeyboardButton("🔙 Back", callback_data='view_cards')]
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
            await query.answer("❌ Card unavailable!", show_alert=True)
            return
            
        # Process sale
        success = db.mark_as_sold(card_id, user_id)
        
        if success:
            # Send code privately via spoiler
            code_text = f"||{card['code']}||"  # Spoiler format
            
            await query.edit_message_text(
                f"✅ **Purchase Successful!**\n\n"
                f"Thank you for buying **{card['name']}**.\n\n"
                f"👇 **YOUR CODE IS BELOW (Click to reveal):**\n"
                f"{code_text}\n\n"
                f"⚠️ *Please save this code. This message is for you only.*",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]]),
                parse_mode='MarkdownV2' 
            )
            
            # Notify Admin (Optional)
            for admin_id in config.ADMIN_IDS:
                try:
                    await context.bot.send_message(
                        chat_id=admin_id,
                        text=f"💰 **New Sale!**\nUser: {query.from_user.first_name}\nItem: {card['name']}\nPrice: {card['price']}{config.CURRENCY}",
                        parse_mode='Markdown'
                    )
                except:
                    pass
        else:
            await query.answer("❌ Error processing transaction.", show_alert=True)

    elif data == 'admin_panel':
        if not is_admin_user:
            await query.answer("⛔ Authorized personnel only!", show_alert=True)
            return
            
        stats = db.get_stats()
        
        text = f"""
⚙️ **Admin Panel**

📊 **Statistics:**
Total Cards: {stats['total_cards']}
Available: {stats['available_cards']}
Sold: {stats['sold_cards']}
Total Revenue: {stats['total_revenue']}{config.CURRENCY}

Use `/addcard` command to add new cards.
Use `/deletecard <ID>` command to delete cards.
"""
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='main_menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')


async def back_to_main(query, context):
    """Return to main menu helper"""
    user = query.from_user
    reply_markup = get_main_menu_keyboard(is_admin(user.id))
    welcome_text = get_welcome_text(user.first_name)
    await query.edit_message_text(welcome_text, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/help command handler"""
    help_text = """
📚 *Help*

*User Commands:*
/start - Start the bot
/help - Show this help message

*Admin Commands:*
/addcard - Add a new gift card
/deletecard - Delete a gift card

*How to Use:*
1️⃣ View Categories
2️⃣ Select a Gift Card
3️⃣ Check Details
4️⃣ Click Buy
5️⃣ Get your Code!

Contact admin for support.
"""
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
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start Bot
    print("Bot is running... (EN)")
    application.run_polling()


if __name__ == '__main__':
    main()
