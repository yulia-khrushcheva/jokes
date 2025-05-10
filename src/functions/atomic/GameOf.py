"""Module for Game of Thrones Quotes Bot Function."""

import logging
import requests
from typing import List
import telebot
from telebot import types
from bot_func_abc import AtomicBotFunctionABC

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Вывод в терминал
)
logger = logging.getLogger(__name__)

class GameOfThronesQuotesBotFunction(AtomicBotFunctionABC):
    """Function to get Game of Thrones quotes from API by command"""

    commands: List[str] = ["got", "gots"]
    authors: List[str] = ["bolse119"]
    about: str = "Получить цитаты из Игры Престолов!"
    description: str = (
        "Функция позволяет получить цитаты персонажей Игры Престолов.\n"
        "Использование:\n"
        "/gots - показать доступных персонажей\n"
        "/got <имя персонажа> - получить цитату\n"
        "Пример: /got tyrion\n"
        "Доступные персонажи: Tyrion, Jon, Daenerys, Jaime, Sansa, Petyr, "
        "Cersei, Arya, Eddard, Theon, Samwell, Varys\n"
        "API: https://api.gameofthronesquotes.xyz"
    )
    state: bool = True

    bot: telebot.TeleBot
    # Расширенный список персонажей с их slug
    characters: List[dict] = [
        {"name": "Tyrion Lannister", "slug": "tyrion"},
        {"name": "Jon Snow", "slug": "jon"},
        {"name": "Daenerys Targaryen", "slug": "daenerys"},
        {"name": "Jaime Lannister", "slug": "jaime"},
        {"name": "Sansa Stark", "slug": "sansa"},
        {"name": "Petyr Baelish", "slug": "petyr"},
        {"name": "Cersei Lannister", "slug": "cersei"},
        {"name": "Arya Stark", "slug": "arya"},
        {"name": "Eddard Stark", "slug": "eddard"},
        {"name": "Theon Greyjoy", "slug": "theon"},
        {"name": "Samwell Tarly", "slug": "samwell"},
        {"name": "Varys", "slug": "varys"}
    ]

    def set_handlers(self, bot: telebot.TeleBot):
        """Set message handlers"""
        logger.info("Инициализация обработчиков для команд %s", self.commands)
        self.bot = bot

        @bot.message_handler(commands=self.commands)
        def got_message_handler(message: types.Message):
            logger.info("Получена команда %s от пользователя %s в чате %s",
                       message.text, message.from_user.id, message.chat.id)

            command = message.text.split()[0].lower()

            if command == "/gots":
                logger.info("Запрос списка персонажей")
                characters_list = ", ".join(char["name"] for char in self.characters)
                bot.reply_to(
                    message,
                    f"Доступные персонажи: {characters_list}\n"
                    "Используйте: /got <имя персонажа>"
                )
                logger.info("Список персонажей отправлен в чат %s", message.chat.id)
                return

            # Обработка /got
            command_args = message.text.split(maxsplit=1)
            if len(command_args) < 2:
                logger.warning("Не указано имя персонажа для команды %s", message.text)
                bot.reply_to(
                    message,
                    "Укажите персонажа! Пример: /got tyrion\n"
                    f"Доступные персонажи: {', '.join(char['name'] for char in self.characters)}"
                )
                logger.info("Отправлено сообщение об ошибке в чат %s", message.chat.id)
                return

            character_input = command_args[1].lower().strip()
            logger.info("Пользователь запросил цитату для персонажа: %s", character_input)

            # Ищем персонажа в списке
            character = next(
                (char for char in self.characters
                 if char["name"].lower().startswith(character_input) or
                    char["slug"].lower() == character_input),
                None
            )

            if not character:
                logger.warning("Персонаж %s не найден", character_input)
                bot.reply_to(
                    message,
                    f"Персонаж '{character_input}' не найден!\n"
                    f"Доступные персонажи: {', '.join(char['name'] for char in self.characters)}"
                )
                logger.info("Отправлено сообщение об ошибке в чат %s", message.chat.id)
                return

            logger.info("Найден персонаж: %s (slug: %s)", character["name"], character["slug"])

            # Получаем цитату
            quote = self.__get_got_quote(character["slug"])

            if quote:
                logger.info("Цитата успешно получена для %s: %s",
                           character["slug"], quote["sentence"])
                bot.reply_to(
                    message,
                    f"📜 {quote['sentence']}\n— {quote['character']['name']}"
                )
                logger.info("Цитата отправлена в чат %s", message.chat.id)
            else:
                logger.warning("Не удалось получить цитату для персонажа %s", character["slug"])
                bot.reply_to(
                    message,
                    f"😔 Не удалось получить цитату для {character['name']}. Попробуйте еще раз."
                )
                logger.info("Отправлено сообщение об ошибке в чат %s", message.chat.id)

    def __get_got_quote(self, slug: str) -> dict:
        """Get random quote for specific character"""
        logger.info("Запрос цитаты для персонажа с slug: %s", slug)
        try:
            # Запрашиваем до 2 цитат
            response = requests.get(
                f"https://api.gameofthronesquotes.xyz/v1/author/{slug}/2",
                timeout=5
            )
            logger.info("Получен ответ от API для %s, статус: %d", slug, response.status_code)
            logger.debug("Полный ответ API: %s", response.text)
            response.raise_for_status()

            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                quote = data[0]
                if "sentence" in quote and "character" in quote:
                    logger.info("Цитата найдена для %s: %s", slug, quote["sentence"])
                    return quote
                logger.warning("Цитата не содержит ожидаемых полей: %s", quote)
                return None
            logger.warning("Некорректный или пустой ответ от API для персонажа %s: %s", slug, data)
            return None
        except requests.RequestException as ex:
            logger.error("Ошибка при запросе цитаты для %s: %s", slug, ex)
            return None
        except ValueError as json_err:
            logger.error("Ошибка парсинга JSON для %s: %s", slug, json_err)
            return None
