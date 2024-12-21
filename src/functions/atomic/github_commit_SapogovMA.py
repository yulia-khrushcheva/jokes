import requests  # Импортируем модуль для работы с HTTP-запросами

from typing import List
import telebot
from telebot import types
from telebot.callback_data import CallbackData
from bot_func_abc import AtomicBotFunctionABC

class CountryCodesBot(AtomicBotFunctionABC):
    commands: List[str] = ["Countries", "ebf"]
    authors: List[str] = ["TestStudentMichael"]
    about: str = "Получение доступных и недоступных стран и вывод административных единиц выбранной страны!"
    description: str = """
                        `/Countries` - функция выводит список доступных ISO-кодов стран, а после принимает код от пользователя
                        и выводит в ответ административные единицы
                        /ebf - Вот доступные ISO-коды стран:RU, US\n\nПожалуйста, введите код страны:RU\n\nАдминистративные единицы для страны с кодом RU\n\nJaroslavl
                        """
    state: bool = True

    bot: telebot.TeleBot
    example_keyboard_factory: CallbackData

    # Метод установки обработчиков событий для бота
    def set_handlers(self, bot: telebot.TeleBot):
        # Сохраняем экземпляр бота в атрибуте класса
        self.bot = bot

        # Обработчик команды "/Countries"
        @bot.message_handler(commands=["Countries"])
        def handle_countries_command(message: types.Message):
            # Получаем список доступных ISO-кодов стран
            iso_country_codes = self.get_iso_country_codes()

            # Форматируем список в виде строки, разделённой переносами строк
            text = '\n'.join(iso_country_codes)

            # Отправляем пользователю список доступных ISO-кодов
            bot.reply_to(message, f"Вот доступные ISO-коды стран:\n{text}\n\nПожалуйста, введите код страны:")

            # Устанавливаем следующий шаг для ожидания ввода кода страны
            bot.register_next_step_handler(message, handle_user_input)

        # Обработчик ввода кода страны от пользователя
        def handle_user_input(message: types.Message):
            # Получаем код страны из сообщения пользователя
            country_code = message.text.strip().upper()

            # Проверяем, существует ли такой код в списке доступных ISO-кодов
            if country_code in self.get_iso_country_codes():
                # Получаем административные единицы для указанного кода страны
                administrative_divisions = self.get_administrative_divisions(country_code)

                # Если административные единицы были успешно получены
                if administrative_divisions:
                    # Форматируем результат в виде строки, разделенной переносами строк
                    text = '\n'.join(administrative_divisions)
                    
                    # Отправка результата пользователю
                    bot.reply_to(message, f"Административные единицы для страны с кодом {country_code}:\n{text}")
                else:
                    # Сообщение об ошибке, если административные единицы не были найдены
                    bot.reply_to(message, f"Не удалось найти административные единицы для страны с кодом {country_code}")
            else:
                # Сообщение об ошибке, если указанный код страны отсутствует в списке доступных ISO-кодов
                bot.reply_to(message, f"Код страны {country_code} не найден в списке доступных ISO-кодов.")

    # Метод для получения ISO-кодов стран
    def get_iso_country_codes(self):
        # URL для получения данных о странах
        url = "https://restcountries.com/v3.1/all"
        
        # Выполнение GET-запроса к указанному URL
        response = requests.get(url)

        # Проверка успешного выполнения запроса (статус-код 200)
        if response.status_code == 200:
            # Преобразование ответа сервера в формат JSON
            countries_data = response.json()
            
            # Создание пустого списка для хранения ISO-кодов стран
            country_codes = []

            # Перебор всех элементов списка стран
            for country in countries_data:
                # Проверка наличия ключа 'cca2' (двухбуквенного кода страны)
                if 'cca2' in country:
                    # Добавление кода страны в список
                    country_codes.append(country['cca2'])

            # Возврат списка ISO-кодов стран
            return country_codes
        else:
            # Логирование ошибки в случае неудачного запроса
            print("Ошибка при получении данных")
            # Возврат пустого списка
            return []

    # Метод для получения административных единиц страны по её коду
    def get_administrative_divisions(self, country_code):
        # Формирование URL для получения административных единиц указанной страны
        url = f"https://rawcdn.githack.com/kamikazechaser/administrative-divisions-db/master/api/{country_code}.json"

        try:
            # Выполнение GET-запроса к сформированному URL
            response = requests.get(url)
            
            # Проверка статуса ответа; если статус не 200, выбрасывается исключение HTTPError
            response.raise_for_status()
            
            # Преобразование ответа сервера в формат JSON
            divisions = response.json()
            
            # Возврат полученных данных
            return divisions
        except requests.exceptions.HTTPError as err:
            # Логирование ошибки HTTP
            print(f"Произошла ошибка HTTP: {err}")
        except Exception as err:
            # Логирование любой другой ошибки
            print(f"Произошла ошибка: {err}")
