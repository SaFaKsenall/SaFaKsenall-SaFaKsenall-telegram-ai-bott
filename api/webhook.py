import os
from flask import Flask, request, Response
from telegram import Update
from telegram.ext import ApplicationBuilder

# Flask uygulamasını oluştur
flask_app = Flask(__name__)

# Telegram bot token'ınızı alın
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Bot uygulamasını oluşturun
application = ApplicationBuilder().token(TOKEN).build()

# Webhook endpoint
@flask_app.route('/api/webhook', methods=['POST'])
async def webhook():
    """Handle incoming webhook requests"""
    if request.method == "POST":
        try:
            # Telegram'dan gelen güncellemeyi al
            update = Update.de_json(request.get_json(force=True), application.bot)
            await application.update_queue.put(update)  # Güncellemeyi işleme al
            return Response('ok', status=200)  # Başarılı yanıt
        except Exception as e:
            print(f"Error in webhook: {str(e)}")
            return Response(str(e), status=500)  # Hata durumunda yanıt
    return Response('Method not allowed', status=405)  # Diğer metodlar için yanıt

@flask_app.route('/api/webhook', methods=['GET'])
def webhook_info():
    """Handle GET requests to check if the webhook is active"""
    return Response('Webhook is active', status=200)  # Webhook'un aktif olduğunu belirt

# Vercel için handler değişkenini tanımlayın
handler = flask_app  # Flask uygulamasını handler olarak ayarlayın

if __name__ == '__main__':
    # Flask uygulamasını başlat
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
