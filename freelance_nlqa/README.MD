# Отчет по тестовому заданию 
## Подход к решению

Система построена по принципу Natural Language to SQL:
1. Пользователь вводит вопрос.
2. LLM генерирует SQL-запрос на основание схемы данных (без доступа к самим данным).
3. Запрос исполняется над датафреймом через SQLite.
4. Ответ выводится в CLI.

Применялись следующие технологии:
- Python 3.10
- Pandas, SQLite, Langchain
- Ollama:`llama3`

## Эффективность и точность

- Вопросы обрабатываются корректно, если они соответствуют схеме.
- Ошибки LLM перехватываются, пользователь получает сообщение.

## Методы и технологии

Что сработало:
- Разделение schema и data
- Простая CLI-интеграция
- Валидация SQL перед выполнением

Что не сработало:
- Иногда LLM добавляет несуществующие поля (решается валидацией schema)

## Критерии оценки качества

- Процент корректно обработанных вопросов: ~80%
- Покрытие тестами (модульные): >70%
- Структура кода соответствует best-practices

## Компиляция и запуск проекта

Установка зависимостей:
Рекомендуется использовать виртуальное окружение: python -m venv .venv source .venv/bin/activate 
Linux/MacOS ..venv\Scripts\activate 
Windows PowerShell Установите необходимые пакеты: pip install -r requirements.txt

Запуск сервера: 
Ollama Если вы используете локальный сервер Ollama (для LLM llama3.2), убедитесь, что он запущен и доступен. ollama serve llama3.2 
Проверьте, что сервер работает и слушает нужный порт.

Подготовка данных:
Убедитесь, что файл с данными находится в папке data/: data/freelancer_earnings_bd.csv

Запуск CLI-приложения:
Запустите основную программу с указанием файла данных: python -m freelance_nlqa.main --data data/freelancer_earnings_bd.csv

Использование:
После запуска программа предложит ввести вопрос на естественном языке. Введите интересующий запрос или напишите exit для выхода.

## Пример вопросов 

Насколько выше доход у фрилансеров, принимающих оплату в криптовалюте, по сравнению с другими способами оплаты?
Как распределяется доход фрилансеров в зависимости от региона проживания?
Какой процент фрилансеров, считающих себя экспертами, выполнил менее 100 проектов?
