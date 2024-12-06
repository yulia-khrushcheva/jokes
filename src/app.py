import logging
import sys
import os
import telebot
from bot_middleware import Middleware
from bot_callback_filter import BotCallbackCustomFilter
from load_atomic import LoadAtomic

_START_COMANDS = ["start", "s"]

def get_log_level(env_key: str) -> int:
    str_level = os.environ.get(env_key)
    if str_level in logging._nameToLevel.keys():
        return logging._nameToLevel[str_level]
    else:
        return logging._nameToLevel["INFO"]
            
def get_logger()-> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(get_log_level("LOGLEVEL"))
    handler = logging.FileHandler(f"{__name__}.log")
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

def get_bot()-> telebot.TeleBot:
    token = os.environ["TBOTTOKEN"]
    telebot.logger.setLevel(get_log_level("TBOT_LOGLEVEL"))
    bot = telebot.TeleBot(token, use_class_middlewares=True)
    return bot

def starter_functions():
    logger.info(f'Number of modules found - {len(atom_functions_list)}')
    for funct in atom_functions_list:
        try:
            if(funct.state):
                funct.set_handlers(bot)
                logger.info(f'{funct} - start OK!')
            else:
                logger.info(f'{funct} - state FALSE!')
        except Exception as e:
            logger.error(e)
            funct.state = False
            logger.warning(f'{funct} - start EXCEPTION!')

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
        bot.send_message(text=f"To begin, enter one of the commands \n /{cmd}", chat_id=message.chat.id)


logger = get_logger()
bot = get_bot()
atom_functions_list = LoadAtomic.load_functions()

if __name__ == '__main__':
    logger.critical('-= START =-')
    starter_functions()
    bot.setup_middleware(Middleware(logger, bot))
    bot.add_custom_filter(BotCallbackCustomFilter())
    bot.infinity_polling()
