@echo off
REM Setup script for Telegram Gift Card Sales Bot (Windows)
REM This script helps set up the bot on Windows

echo =========================================
echo Telegram Gift Card Sales Bot - Setup
echo =========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo.

REM Check if config.py exists
if exist "config.py" (
    echo Config file found: config.py
) else (
    if exist "config.example.py" (
        echo Config file not found. Creating from example...
        copy config.example.py config.py
        echo.
        echo WARNING: Please edit config.py and add your bot token!
        echo   1. Get a token from @BotFather on Telegram
        echo   2. Edit config.py and replace BOT_TOKEN value
        echo   3. Add your cryptocurrency wallet addresses
        echo.
    ) else (
        echo ERROR: config.example.py not found!
        pause
        exit /b 1
    )
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment and install dependencies
echo Installing dependencies...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

REM Create gift_cards directory if it doesn't exist
if not exist "gift_cards" (
    echo Creating gift_cards directory...
    mkdir gift_cards
)

echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Next steps:
echo   1. Edit config.py and add your bot token from @BotFather
echo   2. Add your cryptocurrency wallet addresses to config.py
echo   3. Add gift card images to the gift_cards\ directory
echo   4. Run: start.bat
echo.
echo For verification, run: python verify.py
echo For admin operations: python admin.py help
echo.
pause
