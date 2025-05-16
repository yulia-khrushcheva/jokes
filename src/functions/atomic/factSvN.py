from typing import List
import requests
from telebot.types import Message
from bot_func_abc import AtomicBotFunctionABC

class FactSvNFunction(AtomicBotFunctionABC):
    commands = ["factsvn"]
    authors = ["Kylon2308"]
    about = "Вывод случайного факта"
    description = "Команда /factsvn показывает случайный факт с внешнего API"
    state = True

    def set_handlers(self, bot):
        @bot.message_handler(commands=self.commands)
        def handle_fact(message: Message):
            try:
                response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en", timeout=5)
                response.raise_for_status()
                fact = response.json().get("text", "Не удалось получить факт.")
            except Exception as e:
                fact = f"Ошибка: {e}"
            bot.send_message(message.chat.id, f"💡 Did you know?\n\n{fact}")
