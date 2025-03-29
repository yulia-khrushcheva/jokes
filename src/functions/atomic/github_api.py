"""Module implement github API"""

from typing import List
import telebot
from telebot import types
from bot_func_abc import AtomicBotFunctionABC

class GithubAPICommits(AtomicBotFunctionABC):
    """Function work with github API
    """

    commands: List[str] = ["github", "git"]
    authors: List[str] = ["IHVH"]
    about: str = "Информация о коммитах"
    description: str = """Функция предназначена для получения информации о
      коммитах в репозитори https://github.com/IHVH/system-integration-bot-2 
      для вызова функции можно использовать команды `/git` `/github`  
      """
    state: bool = True

    bot: telebot.TeleBot

    def set_handlers(self, bot: telebot.TeleBot):
        """Set message handlers"""

        self.bot = bot

        @bot.message_handler(commands=self.commands)
        def message_hendler_for_github_api(message: types.Message):

            bot.send_message(text="TEST TEXT 11111", chat_id=message.chat.id)
