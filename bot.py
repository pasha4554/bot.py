import time
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7692605583:AAH0eY48piz5p9IXJi00_JraLG5QIneZKCU"

# состояние пользователя
user_data = {}

keyboard = [["🚀 РОЗПОЧАТИ"]]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

QUESTION = "🔢 Завдання:\n\n👉 15 + 7 = ?"
ANSWER = "22"

TIME_LIMIT = 300  # 5 минут (в секундах)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Вітаємо!\n\n"
        "🎯 Натисни 'РОЗПОЧАТИ' щоб почати тест.\n"
        "⏳ У тебе буде 5 хвилин на відповідь!",
        reply_markup=reply_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    now = time.time()

    # старт
    if text == "🚀 РОЗПОЧАТИ":
        user_data[user_id] = {
            "start_time": now,
            "active": True
        }

        await update.message.reply_text(
            "🔥 Тест розпочато!\n"
            "⏳ У тебе 5 хвилин!\n\n"
            + QUESTION
        )
        return

    # якщо користувач не почав
    if user_id not in user_data or not user_data[user_id]["active"]:
        return

    # перевірка таймера
    if now - user_data[user_id]["start_time"] > TIME_LIMIT:
        user_data[user_id]["active"] = False

        await update.message.reply_text(
            "⛔ ЧАС ВИЧЕРПАНО!\n\n"
            "❌ Спробуй ще раз — натисни РОЗПОЧАТИ."
        )
        return

    # перевірка відповіді
    if text == ANSWER:
        user_data[user_id]["active"] = False

        await update.message.reply_text(
            "🎉 ПРАВИЛЬНО!\n\n"
            "🏆 Ти пройшов тест!\n\n"
            "📺 Пряма трансляція:\n"
            "https://t.me/+lKge-dH0Vqo0MzAy"
        )
    else:
        await update.message.reply_text(
            "❌ Невірно!\n"
            "⏳ Пам'ятай — у тебе 5 хвилин\n\n"
            + QUESTION
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("🤖 Бот запущений...")
app.run_polling()
