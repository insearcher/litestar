FROM python:3.12-slim

# Установка Poetry
RUN pip install "poetry==1.8.3"

# Настройка Poetry: отключаем создание виртуального окружения в контейнере
RUN poetry config virtualenvs.create false

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей
RUN poetry install --no-root --no-dev

# Копирование исходного кода
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Запуск приложения
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
