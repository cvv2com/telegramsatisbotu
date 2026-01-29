#!/bin/bash
# Setup script for Telegram Gift Card Sales Bot

echo "==========================================="
echo "Telegram Gift Card Sales Bot - Setup"
echo "==========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    exit 1
fi

# Create gift_cards directory if not exists
if [ ! -d "gift_cards" ]; then
    echo ""
    echo "Creating gift_cards directory..."
    mkdir -p gift_cards
fi

# Check if config.py exists
if [ ! -f "config.py" ]; then
    echo ""
    echo "⚠️  Warning: config.py not found!"
    echo "Please create config.py from config.example.py and add your bot token"
    echo ""
    echo "cp config.example.py config.py"
    echo "nano config.py  # Edit and add your bot token"
else
    echo ""
    echo "✅ config.py found"
fi

# Setup complete
echo ""
echo "==========================================="
echo "✅ Setup Complete!"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. Edit config.py and add your bot token from @BotFather"
echo "2. Add your cryptocurrency wallet addresses to config.py"
echo "3. Add gift card images to the gift_cards/ directory"
echo "4. Run the bot: python3 bot.py"
echo ""
echo "For admin operations: python3 admin.py help"
echo ""
