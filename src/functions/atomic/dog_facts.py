"""
Модуль для реализации функции бота для получения интересных фактов о собаках.
"""

import logging
from typing import List
import telebot
import requests
from telebot import types
from bot_func_abc import AtomicBotFunctionABC

class DogFactBotFunction(AtomicBotFunctionABC):
    """
    Реализация функции бота для получения интересных фактов о собаках.
    """

    commands: List[str] = ["dogfact", "df"]
    authors: List[str] = ["IHVH"]
    about: str = "Интересные факты о собаках."
    description: str = ("Эта функция позволяет получать интересные факты о "
                        "собаках. Просто вызовите команду /dogfact, и бот "
                        "предоставит вам увлекательный факт. Узнайте больше о "
                        "наших четвероногих друзьях!")
    state: bool = True

    DOG_FACT_API_URL = "https://dog-api.kinduff.com/api/facts"

    def __init__(self):
        super().__init__()
        self.bot = None

    def set_handlers(self, bot: telebot.TeleBot):
        """
        Устанавливает обработчики команд для бота.

        :param bot: Экземпляр TeleBot.
        """
        self.bot = bot

        @self.bot.message_handler(commands=self.commands)
        def dog_fact_message_handler(message: types.Message):
            chat_id_msg = f"\nCHAT ID = {message.chat.id}"
            try:
                response = requests.get(
                    DogFactBotFunction.DOG_FACT_API_URL,
                    timeout=5  # Добавлен таймаут
                )

                if response.status_code == 200:
                    facts_data = response.json()
                    fact_text = facts_data['facts'][0]

                    msg = (
                        f"Ваш запрос обработан в DogFactBotFunction!"
                        f"{chat_id_msg}\n"
                        f"ФАКТ: {fact_text}"
                    )
                    self.bot.send_message(chat_id=message.chat.id, text=msg)
                else:
                    self.bot.send_message(chat_id=message.chat.id, text="Произошла ошибка.")
            except requests.exceptions.RequestException as e:
                logging.error("Произошла ошибка при запросе к API: %s", e)
                self.bot.send_message(chat_id=message.chat.id, text="Попробуйте позже.")
    def check_bot_state(self) -> bool:
        """
        Проверяет состояние бота перед выполнением основной функции.

        :return: True, если состояние бота активно, иначе False.
        """
        return self.state
