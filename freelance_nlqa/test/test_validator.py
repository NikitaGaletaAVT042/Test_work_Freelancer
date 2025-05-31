import pytest
from freelance_nlqa.validator import validate_question

def test_validate_question_valid():
    q = "Какой средний доход?"
    assert validate_question(q) is True

def test_validate_question_empty():
    assert validate_question("   ") is False
    assert validate_question("") is False

def test_validate_question_too_long():
    long_q = "x" * 501
    assert validate_question(long_q) is False

def test_validate_question_with_forbidden_symbols():
    assert validate_question("Вопрос с {фигурной} скобкой") is False
    assert validate_question("Вопрос с <угловой> скобкой") is False
    assert validate_question("Вопрос с ; точкой с запятой") is False
    assert validate_question("Вопрос с -- комментарием") is False
