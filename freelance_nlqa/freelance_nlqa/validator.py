import re

def validate_question(question: str) -> bool:
    """
    Простая валидация вопроса: проверяем на пустую строку,
    отсутствие потенциально опасных символов и слишком длинный ввод.
    """
    if not question or not question.strip():
        return False
    if len(question) > 500:
        return False
    # Запретим символы, которые могут использоваться для инъекций
    forbidden_patterns = [
        r"[{}<>]",  # скобки угловые и фигурные
        r";",       # точка с запятой
        r"--",      # SQL комментарии
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, question):
            return False
    return True
