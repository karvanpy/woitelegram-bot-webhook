from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os 

# Initialize Flask app
app = Flask(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize the Telegram bot application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Define a simple command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your Telegram bot hosted on Vercel.")

# Define a message handler
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

# Add handlers to the bot
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Define the webhook route for Flask
@app.route("/webhook", methods=["POST"])
def webhook():
    # Get the JSON data from the request
    update_data = request.get_json()
    update = Update.de_json(update_data, application.bot)
    
    # Process the update asynchronously
    application.process_update(update)
    return '', 200

# Run the Flask app locally (for testing purposes)
if __name__ == "__main__":
    app.run(port=5000)