import requests
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import filters
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton 
import requests

def get_random_dog():
    """Возвращает URL случайного изображения собаки с random.dog."""
    while True:
        response = requests.get('https://random.dog/woof.json')
        data = response.json()
        if data['url'].endswith(('.jpg', '.jpeg', '.png')):
            return data['url']

async def send_dog_images(update, context, count):
    """Отправляет указанное количество изображений собак в чат."""
    for _ in range(count):
        image_url = get_random_dog()
        await update.message.reply_photo(photo=image_url)
    await update.message.reply_text('Готово!')

async def handle_dog_command(update, context):
    """Обрабатывает команду /dog с выбором количества изображений."""
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data='1'),
         InlineKeyboardButton("2", callback_data='2'),
         InlineKeyboardButton("3", callback_data='3')]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard)
    await update.message.reply_text('Сколько изображений сгенерировать?', reply_markup=markup)

async def handle_dog_callback(update, context):
    """Обрабатывает callback с выбором количества изображений."""
    query = update.callback_query
    await query.answer()
    count = int(query.data)
    await send_dog_images(query.message, context, count)
    reply_keyboard = [['/dog']] 
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    await query.message.reply_text('Хочешь еще?', reply_markup=markup)