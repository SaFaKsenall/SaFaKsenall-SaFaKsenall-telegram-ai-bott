from http.server import BaseHTTPRequestHandler
import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder

# Telegram bot token'ınızı alın
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Bot uygulamasını oluşturun
application = ApplicationBuilder().token(TOKEN).build()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = Update.de_json(json.loads(post_data), application.bot)
            
            # Set response headers
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            
            # Send response
            self.wfile.write("ok".encode())
            
            # Process update
            application.update_queue.put(update)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(e).encode())

    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Webhook is active".encode())

if __name__ == '__main__':
    # Flask uygulamasını başlat
    from http.server import HTTPServer
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 5000))), handler)
    server.serve_forever()
