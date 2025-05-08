import requests
from src.functions.atomic.atomic_bot_function_abc import AtomicBotFunctionABC

"""
Интеграция с Disify: получаем информацию о почте и проверяем, является ли она одноразовой.
"""

class DisifyIntegrationFunction(AtomicBotFunctionABC):
    """
    Команда /disify <email>
    Ответ: email, disposable, quality.
    """
    commands = ["disify", "check_email"]
    authors = ["your_github_login"]
    about = "Проверка e-mail через Disify"
    description = (
        "Используйте: /disify test@example.com — узнаёте, одноразовая ли почта, "
        "качество и дополнительные данные."
    )
    state = True

    API_URL = "https://www.disify.com/api/email/"
    TIMEOUT = 5

    def handle(self, message, **kwargs):
        """
        Обрабатывает команду, запрашивает API Disify и отправляет результат.
        """
        email = kwargs.get("text", "").strip()
        if not email:
            self.reply(message, "Укажите email: `/disify test@example.com`")
            return

        try:
            response = requests.get(f"{self.API_URL}{email}", timeout=self.TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as err:
            status = err.response.status_code if hasattr(err, 'response') and err.response else 'N/A'
            self.reply(message, f"Ошибка запроса (код {status}).")
            return

        data = response.json()
        reply = (
            f"Email: {data.get('email')}\n"
            f"Disposable: {data.get('disposable')}\n"
            f"Quality: {data.get('quality')}\n"
            f"Полный ответ: `{data}`"
        )
        self.reply(message, reply)
