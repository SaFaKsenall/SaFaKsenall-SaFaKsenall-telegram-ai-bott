import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import json
from http.server import BaseHTTPRequestHandler

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

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """POST isteklerini işleyin"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = Update.de_json(json.loads(post_data), application.bot)
            
            # Yanıt başlıklarını ayarlayın
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            
            # Yanıt gönder
            self.wfile.write("ok".encode())
            
            # Güncellemeyi işleyin
            application.update_queue.put(update)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(e).encode())

# Botu başlatın
if __name__ == "__main__":
    application.add_handler(CommandHandler("start", start))
    app.run(port=int(os.environ.get("PORT", 5000)))
