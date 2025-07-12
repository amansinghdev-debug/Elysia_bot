from package import *

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