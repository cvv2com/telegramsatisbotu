#!/bin/bash
# Telegram Gift Card Satış Botu Başlatma Script'i
# Telegram Gift Card Sales Bot Startup Script

echo "🚀 Telegram Gift Card Satış Botu başlatılıyor..."
echo ""

# .env dosyası kontrolü / Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  .env dosyası bulunamadı!"
    echo "    .env.example dosyasını .env olarak kopyalayın ve düzenleyin."
    echo ""
    echo "    .env file not found!"
    echo "    Copy .env.example to .env and edit it."
    exit 1
fi

# Ortam değişkenlerini yükle / Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Bot token kontrolü / Check bot token
if [ "$TELEGRAM_BOT_TOKEN" = "your_bot_token_here" ] || [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ Hata: TELEGRAM_BOT_TOKEN ayarlanmamış!"
    echo "   .env dosyasında bot tokeninizi ayarlayın."
    echo ""
    echo "   Error: TELEGRAM_BOT_TOKEN not set!"
    echo "   Set your bot token in the .env file."
    exit 1
fi

# Admin ID kontrolü / Check admin IDs
if [ -z "$ADMIN_IDS" ]; then
    echo "⚠️  Uyarı: ADMIN_IDS ayarlanmamış!"
    echo "   Admin paneline erişemeyeceksiniz."
    echo ""
    echo "   Warning: ADMIN_IDS not set!"
    echo "   You won't be able to access the admin panel."
fi

# Python sanal ortamı kontrolü / Check for virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Sanal ortam bulunamadı. Oluşturuluyor..."
    echo "   Virtual environment not found. Creating..."
    python3 -m venv venv
fi

# Sanal ortamı etkinleştir / Activate virtual environment
echo "🔧 Sanal ortam etkinleştiriliyor..."
echo "   Activating virtual environment..."
source venv/bin/activate

# Bağımlılıkları yükle / Install dependencies
echo "📦 Bağımlılıklar kontrol ediliyor..."
echo "   Checking dependencies..."
pip install -q -r requirements.txt

# Botu başlat / Start the bot
echo ""
echo "✅ Bot başlatılıyor..."
echo "   Starting bot..."
echo ""
python bot.py
