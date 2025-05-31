import os
import pytest
from freelance_nlqa.config import Config

def test_config_loads_defaults(monkeypatch):
    monkeypatch.delenv("OLLAMA_API_URL", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL_NAME", raising=False)
    monkeypatch.delenv("REQUEST_TIMEOUT", raising=False)

    config = Config()
    assert config.OLLAMA_API_URL == "http://localhost:11434"
    assert config.OLLAMA_MODEL_NAME == "llama3.2"
    assert config.REQUEST_TIMEOUT == 10

def test_config_loads_custom(monkeypatch):
    monkeypatch.setenv("OLLAMA_API_URL", "http://custom-host:8000")
    monkeypatch.setenv("OLLAMA_MODEL_NAME", "mistral-test")
    monkeypatch.setenv("REQUEST_TIMEOUT", "7")

    config = Config()
    assert config.OLLAMA_API_URL == "http://custom-host:8000"
    assert config.OLLAMA_MODEL_NAME == "mistral-test"
    assert config.REQUEST_TIMEOUT == 7

def test_invalid_url(monkeypatch):
    monkeypatch.setenv("OLLAMA_API_URL", "invalid_url")
    monkeypatch.setenv("OLLAMA_MODEL_NAME", "model")
    with pytest.raises(ValueError, match="OLLAMA_API_URL должен быть валидным URL"):
        Config()

def test_missing_model(monkeypatch):
    monkeypatch.setenv("OLLAMA_API_URL", "http://localhost:11434")
    monkeypatch.setenv("OLLAMA_MODEL_NAME", "")
    with pytest.raises(ValueError, match="OLLAMA_MODEL_NAME не должен быть пустым"):
        Config()

def test_invalid_timeout(monkeypatch):
    monkeypatch.setenv("OLLAMA_API_URL", "http://localhost:11434")
    monkeypatch.setenv("OLLAMA_MODEL_NAME", "model")
    monkeypatch.setenv("REQUEST_TIMEOUT", "-42")
    # WARNING: config не бросает исключение, а возвращает default
    config = Config()
    assert config.REQUEST_TIMEOUT == 10  # Значение по умолчанию

