"""Module implementation of the atomic function of the telegram bot. Example of implementation."""

import os
import logging
from typing import List
import telebot
from telebot import types
from telebot.callback_data import CallbackData
import requests
from bot_func_abc import AtomicBotFunctionABC


class AtomicExampleBotFunction(AtomicBotFunctionABC):
    """Example of implementation of atomic function"""

    commands: List[str] = ["example", "ebf", "har"]
    authors: List[str] = ["IHVH"]
    about: str = "Пример функции бота!"
    description: str = """В поле  *description* поместите подробную информацию о работе функции.
    Описание способов использования, логики работы. Примеры вызова функции - /ebf 
    Возможные параметры функции `/example`  """
    state: bool = True

    bot: telebot.TeleBot
    example_keyboard_factory: CallbackData

    def set_handlers(self, bot: telebot.TeleBot):

        self.bot = bot
        self.example_keyboard_factory = CallbackData('t_key_button', prefix=self.commands[0])
        @bot.message_handler(commands=["find"])
        def find_book_by_name(message: types.Message):
            name = "+".join(message.text.replace(" ", "+").split("+")[1:])
            print(name)
            req = "https://openlibrary.org/search.json?q=" + name + "&page=1&limit=1&mode=everything"
            r = requests.get(url=req)
            bookdata = r.json()
            print(bookdata)
            reply = f"Автор: {bookdata['docs'][0]['author_name'][0]}, \nГод издания: {bookdata['docs'][0]['first_publish_year']}, \nСреднее количество страниц: {bookdata['docs'][0]['number_of_pages_median']}\n"
            bot.send_photo(caption=reply, photo="https://covers.openlibrary.org/b/OLID/" + str(
                dict(bookdata)["docs"][0]["cover_edition_key"]) + "-L.jpg", chat_id=message.chat.id)

        @bot.message_handler(commands=["author"])
        def find_book_by_author(message: types.Message):
            name = "+".join(message.text.replace(" ", "+").split("+")[1:])
            print(name)
            req = "https://openlibrary.org/search/authors.json?q=" + name + "&page=1&limit=3&mode=everything"
            r = requests.get(url=req)
            bookdata = r.json()
            print(bookdata)
            r = requests.get(
                f"https://openlibrary.org/authors/{str(dict(bookdata)['docs'][0]['key'])}/works.json?limit=3")
            print(r.json())
            reply = f"Автор: {bookdata['docs'][0]['name']}\nПопулярные работы:\n"
            c = 1
            for e in r.json()["entries"]:
                reply += str(c) + ') ' + e["title"] + '\n'
                c += 1
            bot.send_photo(caption=reply, photo="https://covers.openlibrary.org/a/OLID/" + str(
                dict(bookdata)["docs"][0]["key"]) + "-L.jpg", chat_id=message.chat.id)
