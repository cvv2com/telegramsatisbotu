@echo off
REM Start script for Telegram Gift Card Sales Bot (Windows)

echo =========================================
echo Telegram Gift Card Sales Bot
echo =========================================
echo.

REM Check if config.py exists
if not exist "config.py" (
    echo ERROR: config.py not found!
    echo.
    echo Please run setup.bat first, or copy config.example.py to config.py
    echo and edit it with your bot token.
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run setup.bat first to create the virtual environment
    echo and install dependencies.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Check dependencies
echo Checking dependencies...
pip show python-telegram-bot >nul 2>&1
if errorlevel 1 (
    echo WARNING: Dependencies not installed!
    echo Installing dependencies now...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo.
echo Starting bot...
echo Press Ctrl+C to stop the bot
echo.

REM Start the bot
python bot.py

REM If bot exits with error
if errorlevel 1 (
    echo.
    echo ERROR: Bot stopped with an error!
    echo.
    echo Common issues:
    echo   - Invalid bot token in config.py
    echo   - Missing config.py file
    echo   - Network connection issues
    echo.
    echo Run 'python verify.py' to check your configuration
    echo.
    pause
    exit /b 1
)
