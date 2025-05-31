import argparse
import logging
from freelance_nlqa.data_loader import load_data
from freelance_nlqa.query_handler import handle_query
from freelance_nlqa.llm.ollama import OllamaLLM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Freelance Earnings NLQA")
    parser.add_argument("--data", required=True, help="Путь к CSV файлу с данными")
    args = parser.parse_args()

    try:
        df = load_data(args.data)
    except Exception as e:
        logger.error(f"Не удалось загрузить данные: {e}")
        return

    llm = OllamaLLM()

    print("Введите ваш вопрос (или 'exit' для выхода):", flush=True)
    while True:
        question = input("> ").strip()
        if question.lower() in ("exit", "quit", "выход"):
            break
        answer = handle_query(question, df, llm)
        print("Ответ:", answer, flush=True)

if __name__ == "__main__":
    main()
