import logging
import requests
import telebot
from telebot import types
from bot_func_abc import AtomicBotFunctionABC

class AtomicRandomDuckBotFunction(AtomicBotFunctionABC):
    commands = ["randomduck", "multiduck", "ducktype"]
    authors = ["GrandGeraldio"]
    about = "Генератор картинок уток!"
    description = "Команды: /randomduck - одно изображение, /multiduck <1-7> - несколько, /ducktype <gif|jpg|jpeg|png> - по типу."
    state = True

    def set_handlers(self, bot: telebot.TeleBot):
        self.bot = bot

        @bot.message_handler(commands=self.commands)
        def handle_commands(message: types.Message):
            cmd = message.text.split()[0][1:]
            if cmd == "randomduck":
                self._send_duck_images(message, count=1)
            elif cmd == "multiduck":
                try:
                    count = int(message.text.split()[1])
                    if 1 <= count <= 7:
                        self._send_duck_images(message, count)
                    else:
                        bot.send_message(message.chat.id, "Число от 1 до 7!")
                except (IndexError, ValueError):
                    bot.send_message(message.chat.id, "Использование: /multiduck <1-7>")
            elif cmd == "ducktype":
                try:
                    ext = message.text.split()[1].lower()
                    if ext in ('gif', 'jpg', 'jpeg', 'png'):
                        self._send_duck_images(message, count=1, extension=ext)
                    else:
                        bot.send_message(message.chat.id, "Тип: gif, jpg, jpeg, png")
                except IndexError:
                    bot.send_message(message.chat.id, "Использование: /ducktype <gif|jpg|jpeg|png>")

    def _send_duck_images(self, message: types.Message, count=1, extension=None):
        images = self._get_random_duck_images(count, extension)
        if not images:
            self.bot.send_message(message.chat.id, f"Не удалось получить {'изображение' if count == 1 else 'изображения'}. Попробуйте снова!")
            return
        for img in images:
            self.bot.send_photo(message.chat.id, img)

    def _get_random_duck_images(self, count=1, extension=None):
        images = []
        attempts = 0
        max_attempts = count * 7
        while len(images) < count and attempts < max_attempts:
            try:
                response = requests.get("https://random-d.uk/api/v2/random", timeout=5)
                response.raise_for_status()
                img_url = response.json().get("url")
                if not isinstance(img_url, str):
                    attempts += 1
                    continue
                if extension and not img_url.lower().endswith(f".{extension}"):
                    attempts += 1
                    continue
                if img_url and img_url not in images:
                    images.append(img_url)
                attempts += 1
            except (requests.exceptions.RequestException, ValueError) as ex:
                logging.exception(ex)
                attempts += 1
        return images
