from telegram import Update
from telegram.ext import ContextTypes,CommandHandler,MessageHandler,filters,ApplicationBuilder
from playwright.async_api import async_playwright
import asyncio
import requests
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()

Bot_token = os.getenv("Telegram_token")
if not Bot_token:
    raise ValueError("Telegram token is not set in the environment variables.")

async def reel(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # 👈 force visible!
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        print("✅ Opening page...")
        await page.goto("https://igram.world/reels-downloader", timeout=60000)

        print("✅ Filling URL...")
        await page.fill("#search-form-input", url)

        print("✅ Clicking download...")
        await page.click("#app > section.form-block > div > form > button")

        print("⏳ Waiting for link...")
        await page.wait_for_timeout(10000)  # wait for JS

        try:
            await page.wait_for_selector("#app > div.search-result.show > div > div > ul.output-list__list.output-list__list--one-item > li > div.media-content__info > a", timeout=50000)
            
            download_element = await page.query_selector("#app > div.search-result.show > div > div > ul.output-list__list.output-list__list--one-item > li > div.media-content__info > a")
            download_url = await download_element.get_attribute("href")
            print("✅ Got link, wait at least 2 min !")
        except Exception as e:
            print("❌ Error:", e)
            await page.screenshot(path="debug.png")
            html = await page.content()
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(html)
            download_url = None

        await browser.close()
        return download_url
    
# ✅ WRAPPER
def reel_sync(url: str) -> str:
    return asyncio.run(reel(url))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! I am Elysia, please share your instragram reel link?"
    )
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/about - About this bot\n"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "This is Elysia, a telebot designed to download insta reel"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "instagram.com/reel/" not in text:
        await update.message.reply_text(
            "Please provide a valid Instagram link."
        )
        return
    
    await update.message.reply_text("getting your link...Please wait at least 1 min !")

    # ✅ Run in separate thread
    video_url = await asyncio.to_thread(reel_sync, text)
    await update.message.reply_text("your reel is ready, downloading...")
        
    if not video_url:
        await update.message.reply_text("couldn't fetch the link, please try again")
        return

    try:
        response = requests.get(video_url, timeout=60)
        response.raise_for_status()  # Check for HTTP errors
        video_data = response.content
        print("✅ Downloaded video data")
        await update.message.reply_text("reel downloaded successfully, sending...")
    except requests.RequestException as e:
        await update.message.reply_text(f"download fail: {e}")
        return
    # Use temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(video_data)
        tmp_file_path = tmp_file.name

    with open(tmp_file_path, "rb") as f:
        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=f,
            caption="✅ Here’s your Reel!"
        )

    os.remove(tmp_file_path)

def main():
    app = ApplicationBuilder().token(Bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("about", about))

    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    app.add_handler(echo_handler)

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
