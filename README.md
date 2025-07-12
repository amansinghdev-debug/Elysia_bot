# Elysia 2.0

A Python project for downloading Instagram Reels using Playwright automation and Telegram bot integration.

## Features
- Download Instagram Reels using Playwright
- Telegram bot integration for user interaction
- Error handling with debug screenshots and HTML dumps

## Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies

## Installation
1. Clone the repository or download the source code.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Instagram Reel Downloader
- The main logic is in `package/instragram.py`.
- Use the `reel_sync(url)` function to download a reel by URL.

### Telegram Bot
- The bot logic is in `main.py` and `package/telebot.py`.
- Set your Telegram bot token in the appropriate place (see `main.py`).
- Run the bot:
   ```bash
   python main.py
   ```

## Debugging
- If an error occurs during download, a screenshot (`debug.png`) and HTML dump (`debug.html`) are saved for troubleshooting.

## File Structure
```
main.py                # Entry point for the Telegram bot
requirements.txt       # Python dependencies
package/
    instragram.py      # Instagram reel downloader logic
    telebot.py         # Telegram bot handlers
    __init__.py        # Package init
    debug.png          # Debug screenshot (generated on error)
    __pycache__/       # Python cache files
```

## License
This project is for educational purposes only.
