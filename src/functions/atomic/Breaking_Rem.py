from typing import List
import telebot
from telebot import types
from telebot.callback_data import CallbackData
import requests
from bot_func_abc import AtomicBotFunctionABC

"""
Модуль реализует атомарную функцию для получения цитат из сериала Breaking Bad.
"""

class AtomicExampleBotFunction(AtomicBotFunctionABC):
    """Пример реализации атомарной функции"""

    commands: List[str] = ["quote"]
    authors: List[str] = ["Efrem1"]
    about: str = "Получение цитат из Breaking Bad!"
    description: str = (
        "Этот бот позволяет получать случайные цитаты из сериала Breaking Bad.\n"
        "Для получения цитат используйте команду /quote <количество>."
    )
    state: bool = True

    bot: telebot.TeleBot
    example_keyboard_factory: CallbackData

    def set_handlers(self, bot: telebot.TeleBot):
        """Устанавливает обработчики для команды"""

        self.bot = bot
        self.example_keyboard_factory = CallbackData('t_key_button', prefix=self.commands[0])

        @bot.message_handler(commands=self.commands)
        def send_quote(message: types.Message):
            """Обрабатывает команду /quote"""
            try:
                # Извлечение количества цитат из сообщения
                num_quotes = int(message.text.split()[1])
            except (IndexError, ValueError):
                bot.send_message(
                    message.chat.id,
                    "Пожалуйста, укажите количество цитат. Пример: /quote 3"
                )
                return

            # Получение цитат с API
            quotes = self._fetch_quotes(num_quotes)
            if not quotes:
                bot.send_message(message.chat.id, "Не удалось получить цитаты.")
                return

            # Отправка полученных цитат
            for quote in quotes:
                bot.send_message(message.chat.id, quote)

    def _fetch_quotes(self, num: int) -> List[str]:
        """
        Получение случайных цитат из API Breaking Bad.
        Возвращает список строк с цитатами.
        """
        quotes = []
        for _ in range(num):
            try:
                response = requests.get(
                    "https://api.breakingbadquotes.xyz/v1/quotes",
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()[0]
                    quotes.append(f"Цитата: {data['quote']}\nАвтор: {data['author']}")
                else:
                    return []
            except requests.RequestException:
                return []
        return quotes
