import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import openai

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Временное хранилище уровней пользователей
user_levels = {}

LEVEL_PROMPTS = {
    "A1": "Vasta väga lihtsate ja lühikeste fraasidega, nagu räägiksid algajaga.",
    "A2": "Räägi lihtsas keeles ja kasuta sagedasi igapäevaseid väljendeid.",
    "B1": "Räägi nagu igapäevases vestluses tavalise eesti keele kõnelejaga.",
    "B2": "Räägi loomulikult ja vabalt, nagu räägiksid sõbraga keerukamatel teemadel."
}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("A1", callback_data="level_A1"),
            InlineKeyboardButton("A2", callback_data="level_A2"),
            InlineKeyboardButton("B1", callback_data="level_B1"),
            InlineKeyboardButton("B2", callback_data="level_B2"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Millisel tasemel soovid vestelda?", reply_markup=reply_markup
    )

# Выбор уровня
async def level_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    level = query.data.split("_")[1]
    user_id = query.from_user.id
    user_levels[user_id] = level
    await query.edit_message_text(text=f"Tase valitud: {level}. Alustame vestlust!")

# Обработка сообщений
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    level = user_levels.get(user_id)

    if not level:
        await update.message.reply_text("Palun vali vestlustase esmalt käsuga /start.")
        return

    prompt = LEVEL_PROMPTS[level]
    user_message = update.message.text

    messages = [
        {"role": "system", "content": f"Ole vestluspartner eesti keeles. {prompt}"},
        {"role": "user", "content": user_message}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message["content"]
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Viga suhtlemisel ChatGPT-ga.")

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(level_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot on käivitamisel...")
    app.run_polling()
