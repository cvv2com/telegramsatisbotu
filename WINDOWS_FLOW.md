# Windows User Flow - Quick Reference

## Setup Flow (First Time)

```
┌──────────────────────────────────────────────────────────┐
│  1. Download & Extract Project                           │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  2. Open Command Prompt in project folder                │
│     (Shift + Right-click → "Open PowerShell here")       │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  3. Run: setup.bat                                        │
│     • Checks Python installation                         │
│     • Creates virtual environment                        │
│     • Installs dependencies                              │
│     • Creates config.py from template                    │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  4. Get Bot Token from @BotFather                        │
│     • Open Telegram                                      │
│     • Message @BotFather                                 │
│     • Send: /newbot                                      │
│     • Copy the token                                     │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  5. Edit config.py                                        │
│     • Open with Notepad or any text editor              │
│     • Paste bot token                                    │
│     • Add wallet addresses                               │
│     • Save and close                                     │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  6. (Optional) Verify configuration                      │
│     Run: python verify.py                                │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  7. Add Gift Card Images to gift_cards\ folder          │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  8. Run: start.bat                                        │
│     ✅ Bot is now running!                               │
└──────────────────────────────────────────────────────────┘
```

## Daily Use Flow

```
┌──────────────────────────────────────────────────────────┐
│  Start Bot                                               │
│  Run: start.bat                                          │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  Bot Running...                                          │
│  • Users can interact with bot                          │
│  • Monitor the console for logs                         │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ├─────────────────────────────────────┐
                     │                                     │
                     ▼                                     ▼
┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│  User Sends Payment              │  │  Admin Tasks                     │
│  1. User sends crypto            │  │  Run: python admin.py ...        │
│  2. Check blockchain             │  │                                  │
│  3. Verify payment               │  │  • List users                    │
└────────────────────┬─────────────┘  │  • Add balance                   │
                     │                 │  • View stats                    │
                     │                 │  • View history                  │
                     │                 └──────────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────────────┐
│  Add Balance                                             │
│  Run: python admin.py add USER_ID AMOUNT                │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  User Buys Gift Card                                     │
│  • Balance deducted automatically                        │
│  • Gift card image sent                                  │
└──────────────────────────────────────────────────────────┘
```

## Troubleshooting Flow

```
┌──────────────────────────────────────────────────────────┐
│  Error Occurred?                                         │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  Check Error Type                                        │
└────────┬───────────┬────────────┬────────────┬───────────┘
         │           │            │            │
         ▼           ▼            ▼            ▼
    ┌────────┐  ┌────────┐  ┌──────────┐  ┌────────────┐
    │Python  │  │Config  │  │Module    │  │Network     │
    │Missing │  │Missing │  │Missing   │  │Error       │
    └───┬────┘  └───┬────┘  └────┬─────┘  └─────┬──────┘
        │           │            │              │
        ▼           ▼            ▼              ▼
    Install   Run setup.bat  Run setup.bat  Check Internet
    Python    or copy file   to reinstall  & Bot Token
```

## File Structure for Windows

```
telegramsatisbotu-main/
│
├── setup.bat              ← Run this first!
├── start.bat              ← Run this to start bot
│
├── config.example.py      ← Template
├── config.py              ← Your actual config (created by setup.bat)
│
├── bot.py                 ← Main bot code
├── admin.py               ← Admin tools
├── verify.py              ← Config checker
│
├── WINDOWS.md             ← Complete Windows guide (Turkish)
├── README.md              ← General documentation
│
├── requirements.txt       ← Python packages
│
├── venv/                  ← Virtual environment (created by setup.bat)
│   └── Scripts/
│       └── activate.bat   ← Activation script
│
└── gift_cards/            ← Put your gift card images here
    ├── mastercard_50.jpg
    ├── visa_30.jpg
    └── ...
```

## Quick Commands Reference

### Setup (First Time)
```cmd
setup.bat
```

### Start Bot
```cmd
start.bat
```

### Stop Bot
```
Press Ctrl+C in the console window
```

### Check Configuration
```cmd
python verify.py
```

### Admin Commands
```cmd
REM List all users
python admin.py users

REM View user details
python admin.py user 123456789

REM Add balance after payment verification
python admin.py add 123456789 100.00

REM View statistics
python admin.py stats

REM Show help
python admin.py help
```

## Common Error Messages and Solutions

### ❌ "'python' is not recognized"
**Solution:** Install Python from python.org and check "Add Python to PATH"

### ❌ "config.py not found"
**Solution:** Run `setup.bat` or `copy config.example.py config.py`

### ❌ "No module named 'telegram'"
**Solution:** Run `setup.bat` to install dependencies

### ❌ "telegram.error.InvalidToken"
**Solution:** Check bot token in config.py - get new one from @BotFather

### ❌ "'cp' is not recognized"
**Solution:** Use Windows commands:
- Instead of `cp file1 file2` → use `copy file1 file2`
- Instead of `./script.sh` → use `script.bat`

## Tips for Windows Users

1. **Always use setup.bat and start.bat** - Don't try to use Linux commands
2. **Keep the console window open** - Don't close it while bot is running
3. **Use Notepad++ or VS Code** - Better than regular Notepad for editing config.py
4. **Check Windows Firewall** - Make sure Python is allowed
5. **Antivirus** - Some antivirus may block the bot, add exception if needed

## Need More Help?

See detailed documentation:
- [WINDOWS.md](WINDOWS.md) - Complete Windows setup guide (Turkish)
- [README.md](README.md) - General documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Advanced deployment options
