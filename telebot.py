from telegram import Update
from telegram.ext import ContextTypes,CommandHandler,MessageHandler,filters,ApplicationBuilder
import asyncio
import requests
import tempfile
from .instragram import reel, reel_sync
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! I am Elysia, your telebot . How can I assist you today?"
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
        "This is Elysia, a telebot designed to assist you with various tasks. "
        "Feel free to ask me anything!"
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
