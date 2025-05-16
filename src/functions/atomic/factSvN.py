import requests
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"

async def fact_svn_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        text = data.get("text", "Couldn't fetch a fact.")
    except Exception as e:
        text = f"Error fetching fact: {e}"
    
    await update.message.reply_text(f"💡 Did you know?\n\n{text}")

def get_fact_svn_handler():
    return CommandHandler("factSvN", fact_svn_handler)
