import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

# Telegram bot token'ınızı alın
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Bot uygulamasını oluşturun
application = ApplicationBuilder().token(TOKEN).build()

# Komut işleyicileri
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot başlatıldı!")

# Webhook endpoint
@app.route('/api/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return 'ok', 200

# Botu başlatın
if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)))
