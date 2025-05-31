def build_sql_prompt(schema_description: str, user_question: str) -> str:
    return (
        "У тебя есть таблица 'Freelancers' со следующими столбцами:\n"
        f"{schema_description}\n\n"
        "Сгенерируй SQL-запрос на языке SQLite, который позволяет ответить на вопрос:\n"
        f"'{user_question}'\n\n"
        "Запрос должен сравнивать значения между категориями, если вопрос об этом. "
        "Используй агрегатные функции (например, AVG или SUM), если нужно. "
        "Имя таблицы — строго 'Freelancers'.\n"
        "Верни только сам SQL-запрос, без пояснений, без ```sql."
    )


def build_explanation_prompt(user_question: str, sql_query: str, sql_result: str) -> str:
    return (
        "Ты получил следующий SQL-запрос:\n"
        f"{sql_query}\n\n"
        "Он был выполнен, и результат:\n"
        f"{sql_result}\n\n"
        f"Ответь на вопрос пользователя на основе результата: {user_question}\n"
        "Дай развернутое объяснение, сделай сравнение, если оно требуется. Не ссылайся на SQL напрямую, говори человеческим языком."
    )


def generate_schema_description(df) -> str:
    """Создаёт текстовое описание схемы DataFrame для передачи в prompt."""
    lines = ["Схема таблицы:"]
    for col in df.columns:
        dtype = str(df[col].dtype)
        sample_vals = df[col].dropna().unique()[:5]
        samples = ", ".join(map(str, sample_vals))
        lines.append(f"- {col} (тип: {dtype}, примеры: {samples})")
    return "\n".join(lines)
