from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    def ask(self, prompt: str) -> str:
        """
        Отправить prompt в модель и получить текстовый ответ.
        """
        pass
