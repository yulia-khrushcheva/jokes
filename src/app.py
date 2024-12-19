"""Main module for running the bot"""

import logging
import sys
import os
import telebot
from load_atomic import load_atomic_functions
from bot_middleware import Middleware
from bot_callback_filter import BotCallbackCustomFilter

_START_COMANDS = ["start", "help", "info", "s", "h", "i"]

def get_log_level(env_key: str) -> int:
    """Get log level from environment variables"""
    str_level = os.environ.get(env_key)
    levels = logging.getLevelNamesMapping()
    if str_level in levels:
        return levels[str_level]
    return levels["INFO"]

def get_logger()-> logging.Logger:
    """Get a configured logger"""
    log = logging.getLogger(__name__)
    log.setLevel(get_log_level("LOGLEVEL"))
    handler = logging.FileHandler(f"{__name__}.log")
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    return log

def get_bot()-> telebot.TeleBot:
    """Get a configured bot"""
    token = os.environ["TBOTTOKEN"]
    telebot.logger.setLevel(get_log_level("TBOT_LOGLEVEL"))
    new_bot = telebot.TeleBot(token, use_class_middlewares=True)
    return new_bot

def starter_functions():
    """Decorate handlers functions"""
    logger.info("Number of modules found - %d", len(atom_functions_list))
    for funct in atom_functions_list:
        try:
            if funct.state:
                funct.set_handlers(bot)
                logger.info("%s - start OK!", funct)
            else:
                logger.info("%s - state FALSE!", funct)
        except Exception as ex: # pylint: disable=broad-except
            logger.error(ex)
            funct.state = False
            logger.warning("%s - start EXCEPTION!", funct)

    @bot.message_handler(commands=_START_COMANDS)
    def start_message(message):
        txt = "Доступные функции: \n"
        for funct in atom_functions_list:
            txt += f"/{funct.commands[0]} - {funct.about} \n"
        bot.send_message(text=txt, chat_id=message.chat.id)

    @bot.message_handler(func=lambda message: True)
    def text_messages(message):
        bot.reply_to(message, "Text = " + message.text)
        cmd = "\n /".join(_START_COMANDS)
        msg = f"To begin, enter one of the commands \n /{cmd}"
        bot.send_message(text=msg, chat_id=message.chat.id)


logger = get_logger()
bot = get_bot()
atom_functions_list = load_atomic_functions()

if __name__ == '__main__':
    logger.critical('-= START =-')
    starter_functions()
    bot.setup_middleware(Middleware(logger, bot))
    bot.add_custom_filter(BotCallbackCustomFilter())
    bot.infinity_polling()
