"""
Базовый класс для атомарных функций телеграм-бота.
"""

from typing import List
import telebot
from telebot.callback_data import CallbackData
from bot_func_abc import AtomicBotFunctionABC


class BaseAtomicBotFunction(AtomicBotFunctionABC):
    """
    Базовый класс для атомарных функций, предоставляющий общие методы и свойства.
    """

    commands: List[str] = []
    state: bool = True
    bot: telebot.TeleBot
    keyboard_factory: CallbackData

    def set_base_handlers(self, bot: telebot.TeleBot):
        """Устанавливает общие обработчики для команды."""
        self.bot = bot
        self.keyboard_factory = CallbackData('t_key_button', prefix=self.commands[0])
