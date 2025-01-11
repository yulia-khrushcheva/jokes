import requests
from typing import List
import telebot
from telebot import types
from telebot.callback_data import CallbackData
from bot_func_abc import AtomicBotFunctionABC

class AtomicExampleBotFunction(AtomicBotFunctionABC):
    """Модуль для получения цитат из сериала Breaking Bad через Telegram бота."""

    commands: List[str] = ["quote"]
    authors: List[str] = ["Efrem1"]
    about: str = "Получение цитат из Breaking Bad!"
    description: str = (
        "Этот бот позволяет получать случайные цитаты из сериала Breaking Bad. "
        "Для получения цитат используйте команду /quote <количество>"
    )
    state: bool = True

    bot: telebot.TeleBot
    example_keyboard_factory: CallbackData

    def set_handlers(self, bot: telebot.TeleBot):
        self.bot = bot
        self.example_keyboard_factory = CallbackData('t_key_button', prefix=self.commands[0])

        @bot.message_handler(commands=self.commands)
        def send_quote(message: types.Message):
            try:
                num_quotes = int(message.text.split()[1])  # Получаем число после команды /quote
            except (IndexError, ValueError):
                bot.send_message(message.chat.id, "Пожалуйста, укажите количество цитат. Пример: /quote 3")
                return

            quotes = []
            for _ in range(num_quotes):
                response = requests.get("https://api.breakingbadquotes.xyz/v1/quotes", timeout=10)
                if response.status_code == 200:
                    data = response.json()[0]
                    quote = data['quote']
                    author = data['author']
                    quotes.append(f"Цитата: {quote}\nАвтор: {author}")
                else:
                    bot.send_message(message.chat.id, "Не удалось получить цитату.")
                    return

            for quote in quotes:
                bot.send_message(message.chat.id, quote)
