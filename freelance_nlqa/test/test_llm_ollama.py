import pytest
from unittest.mock import patch, Mock
from freelance_nlqa.llm.ollama import OllamaLLM
import requests

def test_ollama_ask_success():
    llm = OllamaLLM()
    mock_response = Mock()
    mock_response.iter_lines.return_value = [
        b'{"message": {"content": "Test"}}',
        b'{"message": {"content": " answer"}}'
    ]
    mock_response.raise_for_status = lambda: None

    with patch("requests.post", return_value=mock_response) as mock_post:
        answer = llm.ask("Test prompt")
        assert answer == "Test answer"
        mock_post.assert_called_once()

def test_ollama_ask_http_error():
    llm = OllamaLLM()
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("HTTP Error")

    with patch("requests.post", return_value=mock_response):
        with pytest.raises(RuntimeError, match="Ошибка запроса к LLM:"):
            llm.ask("Test prompt")

def test_ollama_ask_invalid_response():
    llm = OllamaLLM()
    mock_response = Mock()
    mock_response.iter_lines.return_value = [b'{}']
    mock_response.raise_for_status = lambda: None

    with patch("requests.post", return_value=mock_response):
        answer = llm.ask("Test prompt")
        assert answer == "Ответ от модели пуст."
