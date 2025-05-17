from typing import List
import requests
from telebot.types import Message
from bot_func_abc import AtomicBotFunctionABC

def escape_markdown_v2(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join('\\' + ch if ch in escape_chars else ch for ch in text)

class FactSvNFunction(AtomicBotFunctionABC):
    commands = ["factsvn"]
    authors = ["Kylon2308"]
    about = "Вывод случайного факта"
    description = "Команда /factsvn показывает указанное количество случайных фактов с внешнего API"
    state = True

    def set_handlers(self, bot):
        @bot.message_handler(commands=self.commands)
        def handle_factsvn(message: Message):
            try:
                arr = message.text.strip().split()
                count = 1  # По умолчанию один факт
                if len(arr) == 2 and arr[1].isdigit():
                    count = int(arr[1])
                    if count > 10:
                        count = 10  # ограничим до 10 фактов

                facts = []
                for i in range(count):
                    response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en", timeout=5)
                    response.raise_for_status()
                    fact = response.json().get("text", "Не удалось получить факт.")
                    fact = escape_markdown_v2(fact)
                    facts.append(f"{i+1}\\. {fact}")

                message_text = "*Did you know?*\n\n" + "\n\n".join(facts)
                bot.send_message(message.chat.id, message_text, parse_mode="MarkdownV2")

            except Exception as e:
                bot.send_message(message.chat.id, f"Ошибка: {e}")
