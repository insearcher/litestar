# Этап сборки
FROM python:3.12-slim AS build

# Установка Poetry
RUN pip install "poetry==1.8.3"

# Настройка Poetry: отключаем создание виртуального окружения в контейнере
RUN poetry config virtualenvs.create false

# Установка рабочей директории
WORKDIR /app

# Копирование только файлов для установки зависимостей
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей без разработческих
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

# Этап выполнения
FROM python:3.12-slim

# Установка необходимых инструментов
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создание непривилегированного пользователя
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Копирование установленных зависимостей из предыдущего этапа
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Копирование исходного кода и конфигурационных файлов
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY docker-entrypoint.sh ./

# Делаем entrypoint скрипт исполняемым
RUN chmod +x /app/docker-entrypoint.sh && \
    chown -R appuser:appuser /app

# Переменные среды
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Проверка работоспособности
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Установка рабочего пользователя
USER appuser

# Entrypoint для предварительных действий
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Запуск приложения
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
