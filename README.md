# LiteStar User Management API

REST API на базе LiteStar (Python 3.12) с CRUD-операциями для таблицы `user` в PostgreSQL.

## Стек технологий

- Backend: LiteStar 2.x
- База данных: PostgreSQL + Advanced-SQLAlchemy
- Инфраструктура: Docker
- Пакетный менеджер: Poetry 1.8.3

## Запуск проекта

### Через Docker Compose

1. Клонировать репозиторий:
   ```
   git clone https://github.com/insearcher/litestar.git
   cd litestar
   ```

2. Запустить контейнеры:
   ```
   docker compose up -d
   ```

   > Примечание: Миграции применяются автоматически при запуске через entrypoint скрипт.

3. API будет доступно по адресу: http://localhost:8000
4. Swagger UI доступен по адресу: http://localhost:8000/docs

#### Пересборка контейнеров

При внесении изменений в код необходимо пересобрать контейнеры:

```
docker compose build
docker compose up -d
```

#### Просмотр логов

Для просмотра логов приложения:

```
docker compose logs -f app
```

Для просмотра логов базы данных:

```
docker compose logs -f db
```

### Локальный запуск

1. Клонировать репозиторий:
   ```
   git clone https://github.com/insearcher/litestar.git
   cd litestar
   ```

2. Установить Poetry 1.8.3:
   ```
   pip install poetry==1.8.3
   ```

3. Установить зависимости:
   ```
   poetry install
   ```

4. Создать файл .env и настроить переменные окружения (пример в .env.example)

5. Запустить приложение:
   ```
   poetry run uvicorn src.app:app --host 127.0.0.1 --port 8000
   ```

6. Применить миграции:
   ```
   poetry run alembic upgrade head
   ```

7. API будет доступно по адресу: http://localhost:8000
8. Swagger UI доступен по адресу: http://localhost:8000/docs

## API Эндпоинты

- `POST /users` - Создание пользователя
- `GET /users` - Получение списка пользователей
- `GET /users/{user_id}` - Получение данных одного пользователя
- `PUT /users/{user_id}` - Обновление данных пользователя
- `DELETE /users/{user_id}` - Удаление пользователя
