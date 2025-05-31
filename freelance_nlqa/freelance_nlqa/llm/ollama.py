import requests
import logging
import json
from freelance_nlqa.llm.base import LLMInterface
from freelance_nlqa.config import config

logger = logging.getLogger(__name__)

class OllamaLLM(LLMInterface):
    def __init__(self):
        self.api_url = config.OLLAMA_API_URL  # например http://localhost:11434
        self.model = config.OLLAMA_MODEL_NAME  # например "llama3.2"
        self.timeout = config.REQUEST_TIMEOUT

    def ask(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 256,
            "stream": True  # Включаем стриминговый режим
        }

        try:
            response = requests.post(
                f"{self.api_url}/api/chat",
                json=payload,
                timeout=self.timeout,
                stream=True  # Читаем по частям
            )
            response.raise_for_status()

            chunks = []
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        content = data.get("message", {}).get("content", "")
                        if content:
                            chunks.append(content)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Ошибка JSON-декодирования: {e} | строка: {line}")

            full_response = "".join(chunks).strip()

            if not full_response:
                logger.warning("Ответ от LLM пустой")
                return "Ответ от модели пуст."

            return full_response

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса к Ollama API: {e}")
            raise RuntimeError(f"Ошибка запроса к LLM: {e}")

        except Exception as e:
            logger.error(f"Непредвиденная ошибка при обработке ответа от LLM: {e}")
            raise RuntimeError("Ошибка при обработке ответа от LLM.")
