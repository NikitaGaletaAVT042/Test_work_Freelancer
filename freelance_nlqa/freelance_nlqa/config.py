import os
from dotenv import load_dotenv
import logging

load_dotenv()  # Загружаем переменные окружения из .env

logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        self.OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        self.OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3.2")
        self.REQUEST_TIMEOUT = self._parse_int_env("REQUEST_TIMEOUT", 10)

        self.validate()

    def _parse_int_env(self, var_name: str, default: int) -> int:
        val = os.getenv(var_name)
        if val is None:
            return default
        try:
            intval = int(val)
            if intval <= 0:
                raise ValueError
            return intval
        except ValueError:
            logger.warning(f"Переменная окружения {var_name} должна быть положительным числом. Используется значение по умолчанию {default}.")
            return default

    def validate(self):
        if not self.OLLAMA_API_URL.startswith("http"):
            raise ValueError("OLLAMA_API_URL должен быть валидным URL")
        if not self.OLLAMA_MODEL_NAME:
            raise ValueError("OLLAMA_MODEL_NAME не должен быть пустым")
        if self.REQUEST_TIMEOUT <= 0:
            raise ValueError("REQUEST_TIMEOUT должен быть положительным числом")

# Создаём глобальный экземпляр конфигурации
config = Config()
