@echo off
REM Telegram Gift Card Satis Botu Baslatma Script'i
REM Telegram Gift Card Sales Bot Startup Script

echo.
echo Telegram Gift Card Satis Botu baslatiliyor...
echo.

REM .env dosyasi kontrolu / Check for .env file
if not exist .env (
    echo Uyari: .env dosyasi bulunamadi!
    echo         .env.example dosyasini .env olarak kopyalayin ve duzenleyin.
    echo.
    echo Warning: .env file not found!
    echo          Copy .env.example to .env and edit it.
    pause
    exit /b 1
)

REM Python sanal ortami kontrolu / Check for virtual environment
if not exist venv (
    echo Sanal ortam bulunamadi. Olusturuluyor...
    echo Virtual environment not found. Creating...
    python -m venv venv
)

REM Sanal ortami etkinlestir / Activate virtual environment
echo Sanal ortam etkinlestiriliyor...
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Bagimliliklari yukle / Install dependencies
echo Bagimliliklar kontrol ediliyor...
echo Checking dependencies...
pip install -q -r requirements.txt

REM Botu baslat / Start the bot
echo.
echo Bot baslatiliyor...
echo Starting bot...
echo.
python bot.py

pause
