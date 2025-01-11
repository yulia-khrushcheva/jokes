import os
import logging
from typing import List
import telebot
import requests
from telebot import types
from telebot.callback_data import CallbackData
from bot_func_abc import AtomicBotFunctionABC

class DogFactBotFunction(AtomicBotFunctionABC):
    """Реализация функции бота для получения интересных фактов о собаках.
    """

    commands: List[str] = ["dogfact", "df"]
    authors: List[str] = ["IHVH"]
    about: str = "Интересные факты о собаках."  # Измененная строка
    description: str = """Эта функция позволяет получать интересные факты о собаках. Просто вызовите команду /dogfact, и бот предоставит вам увлекательный факт. Узнайте больше о наших четвероногих друзьях!"""  # Измененная строка
    state: bool = True

    bot: telebot.TeleBot
    dog_fact_keyboard_factory: CallbackData

    def set_handlers(self, bot: telebot.TeleBot):
        self.bot = bot
        self.dog_fact_keyboard_factory = CallbackData('t_key_button', prefix=self.commands[0])

        @bot.message_handler(commands=self.commands)
        def dog_fact_message_handler(message: types.Message):
            chat_id_msg = f"\nCHAT ID = {message.chat.id}"
            try:
                url = "https://dog-api.kinduff.com/api/facts"
                response = requests.get(url)

                if response.status_code == 200:
                    facts_data = response.json()
                    fact_text = facts_data['facts'][0]

                    msg = (
                        f"Ваш запрос обработан в DogFactBotFunction! {chat_id_msg}\n"
                        f"ФАКТ: {fact_text}"
                    )
                    bot.send_message(chat_id=message.chat.id, text=msg)
                else:
                    bot.send_message(chat_id=message.chat.id, text="Произошла ошибка при получении факта.")
            except Exception as e:
                logging.error(f"Произошла ошибка при запросе к API: {e}")
                bot.send_message(chat_id=message.chat.id, text="К сожалению, возникла ошибка при общении с сервером. Попробуйте позже.")