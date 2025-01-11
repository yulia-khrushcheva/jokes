"""
Модуль для получения случайных цитат из сериала Breaking Bad.
"""

from typing import List
import telebot
from telebot import types
import requests
from base_atomic_bot_function import BaseAtomicBotFunction


class AtomicExampleBotFunction(BaseAtomicBotFunction):
    """
    Реализация атомарной функции для получения цитат Breaking Bad.
    """

    commands: List[str] = ["quote"]
    authors: List[str] = ["FeyBM"]
    about: str = "Получение цитат из Breaking Bad!"
    description: str = (
        "Этот бот позволяет получать случайные цитаты из сериала Breaking Bad.\n"
        "Для получения цитат используйте команду /quote <количество>."
    )

    def set_handlers(self, bot: telebot.TeleBot):
        """Устанавливает обработчики для команды."""
        super().set_base_handlers(bot)

        @bot.message_handler(commands=self.commands)
        def send_quote(message: types.Message):
            """Обрабатывает команду /quote."""
            try:
                num_quotes = int(message.text.split()[1])
            except (IndexError, ValueError):
                bot.send_message(
                    message.chat.id,
                    "Пожалуйста, укажите количество цитат. Пример: /quote 3"
                )
                return

            quotes = self._fetch_quotes(num_quotes)
            if not quotes:
                bot.send_message(message.chat.id, "Не удалось получить цитаты.")
                return

            for quote in quotes:
                bot.send_message(message.chat.id, quote)

    def _fetch_quotes(self, num: int):
        """
        Получение случайных цитат из API Breaking Bad.
        """
        quotes = []
        for _ in range(num):
            try:
                response = requests.get("https://api.breakingbadquotes.xyz/v1/quotes", timeout=5)
                if response.status_code == 200:
                    data = response.json()[0]
                    quotes.append(f"Цитата: {data['quote']}\nАвтор: {data['author']}")
                else:
                    return []
            except requests.RequestException:
                return []
        return quotes
