"""
Модуль для получения данных другого API.
"""

from typing import List
import telebot
from telebot import types
from base_atomic_bot_function import BaseAtomicBotFunction


class BremAtomicFunction(BaseAtomicBotFunction):
    """
    Пример атомарной функции для другого источника данных.
    """

    commands: List[str] = ["brem"]
    authors: List[str] = ["FeyBM"]
    about: str = "Пример получения данных из другого API."
    description: str = "Используйте команду /brem <параметр> для получения данных."

    def set_handlers(self, bot: telebot.TeleBot):
        """Устанавливает обработчики для команды."""
        super().set_base_handlers(bot)

        @bot.message_handler(commands=self.commands)
        def send_data(message: types.Message):
            """Обрабатывает команду /brem."""
            # Пример использования аргумента message
            bot.send_message(
                message.chat.id,
                "Функционал команды /brem ещё не реализован. Ожидайте обновлений!"
            )
