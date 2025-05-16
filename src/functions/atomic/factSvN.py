from telebot import types
import requests

class FactSvNFunction:
    commands = ["factSvN"]
    authors = ["Kylon2308"]
    about = "Вывод случайного факта"
    description = "Команда /factSvN показывает случайный факт с внешнего API"

    def __init__(self, bot):
        self.bot = bot

    def register_handlers(self):
        @self.bot.message_handler(commands=self.commands)
        def handle_fact(message):
            API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
            try:
                response = requests.get(API_URL, timeout=5)
                response.raise_for_status()
                data = response.json()
                text = data.get("text", "Не удалось получить факт.")
            except Exception as e:
                text = f"Ошибка при получении факта: {e}"

            self.bot.send_message(chat_id=message.chat.id, text=f"💡 Did you know?\n\n{text}")
