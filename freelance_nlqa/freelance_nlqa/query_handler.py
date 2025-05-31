import logging
import pandas as pd
from freelance_nlqa.llm.base import LLMInterface
from freelance_nlqa.prompts import build_sql_prompt, build_explanation_prompt, generate_schema_description
from freelance_nlqa.validator import validate_question
import pandasql
logger = logging.getLogger(__name__)


def handle_query(question: str, df: pd.DataFrame, llm: LLMInterface) -> str:
    #if not validate_question(question):
        #logger.warning(f"Невалидный вопрос: {question}")
        #return "Вопрос некорректен. Пожалуйста, задайте корректный вопрос."

    try:
        schema_description = generate_schema_description(df)
        sql_prompt = build_sql_prompt(schema_description, question)
        sql_query = llm.ask(sql_prompt).strip()

        #logger.info(f"Сгенерированный SQL: {sql_query}")

        try:
            # Оборачиваем df в словарь под названием 'Freelancers'
            pysqldf = lambda q: pandasql.sqldf(q, {"Freelancers": df})
            result_df = pysqldf(sql_query)
        except Exception as e:
            logger.error(f"Ошибка SQL-запроса: {e}")
            return f"Ошибка в SQL-запросе. Попробуйте переформулировать вопрос.\n{e}"

        if result_df.empty:
            return "Результат пуст. Возможно, нет данных, удовлетворяющих условиям."

        result_str = result_df.to_string(index=False)

        explanation_prompt = build_explanation_prompt(question, sql_query, result_str)
        answer = llm.ask(explanation_prompt)

        return answer
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {e}")
        return "Произошла ошибка при обработке запроса. Попробуйте позже."
