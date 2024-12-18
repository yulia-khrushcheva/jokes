from telebot import types
from telebot.callback_data import CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

class BotCallbackCustomFilter(AdvancedCustomFilter):
    key = 'config'
    def check(self, message: types.CallbackQuery, text: CallbackDataFilter):
        return text.check(query=message)