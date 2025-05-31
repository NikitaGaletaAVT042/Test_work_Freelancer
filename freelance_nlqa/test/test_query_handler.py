import pytest
import pandas as pd
from unittest.mock import MagicMock
from freelance_nlqa.query_handler import handle_query

class DummyLLM:
    def __init__(self):
        self.calls = []

    def ask(self, prompt: str) -> str:
        self.calls.append(prompt)
        if len(self.calls) == 1:
            return "SELECT * FROM Freelancers WHERE Experience_Level = 'Expert';"
        else:
            return "Тестовый ответ"


@pytest.fixture
def sample_df():
    data = {
        "Freelancer_ID": [1, 2, 3, 4],
        "Job_Category": ["Dev", "Design", "Dev", "Writing"],
        "Platform": ["Upwork", "Fiverr", "Upwork", "Freelancer"],
        "Experience_Level": ["Expert", "Intermediate", "Expert", "Beginner"],
        "Client_Region": ["US", "EU", "US", "Asia"],
        "Payment_Method": ["PayPal", "Payoneer", "PayPal", "Bank Transfer"],
        "Job_Completed": [120, 50, 80, 10],
        "Earnings_USD": [10000.0, 5000.0, 7000.0, 1000.0],
        "Hourly_Rate": [50, 30, 40, 15],
        "Job_Success_Rate": [95, 88, 92, 70],
        "Client_Rating": [4.8, 4.5, 4.9, 4.0],
        "Job_Duration_Days": [30, 20, 40, 10],
        "Project_Type": ["Fixed", "Hourly", "Fixed", "Fixed"],
        "Rehire_Rate": [0.3, 0.1, 0.5, 0.0],
        "Marketing_Spend": [100, 50, 200, 0],
    }
    return pd.DataFrame(data)
def test_handle_query_calls_llm_with_correct_prompt(sample_df):
    llm = DummyLLM()
    question = "Каков средний доход экспертов?"

    answer = handle_query(question, sample_df, llm)

    # Проверяем, что функция вернула "Тестовый ответ" (ответ второго вызова)
    assert answer == "Тестовый ответ"

    # Было ровно 2 вызова LLM
    assert len(llm.calls) == 2

    # Первый вызов — это промпт с описанием таблицы и вопросом, проверяем, что там есть вопрос
    assert question in llm.calls[0]

    # Первый вызов должен содержать описание таблицы (пример)
    assert "ТАБЛИЦА 'FREELANCERS'" in llm.calls[0].upper()

    # Второй вызов — промпт, который содержит и вопрос, и SQL-запрос
    assert question in llm.calls[1]
    assert "SELECT * FROM Freelancers" in llm.calls[1]
