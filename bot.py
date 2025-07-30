import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Загружаем токен из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tere tulemast! Olen sinu eesti keele vestlusrobot. Räägime!")

# любое сообщение
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    if "tere" in user_message:
        reply = "Tere! Kuidas sul läheb?"
    elif "hästi" in user_message:
        reply = "Väga tore kuulda! Kas soovid vestelda edasi?"
    elif "jah" in user_message:
        reply = "Räägi mulle endast natuke."
    elif "ei" in user_message:
        reply = "Olgu, siis kohtume hiljem! Head päeva!"
    else:
        reply = "Väga huvitav! Räägi veel!"

    await update.message.reply_text(reply)

# запускаем бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot on käivitamisel...")
    app.run_polling()
