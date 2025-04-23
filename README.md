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
   docker-compose up -d
   ```

3. Применить миграции:
   ```
   docker-compose exec app litestar database upgrade
   ```

4. API будет доступно по адресу: http://localhost:8000
5. Swagger UI доступен по адресу: http://localhost:8000/docs

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
   poetry run litestar database upgrade
   ```

7. API будет доступно по адресу: http://localhost:8000
8. Swagger UI доступен по адресу: http://localhost:8000/docs

## API Эндпоинты

- `POST /users` - Создание пользователя
- `GET /users` - Получение списка пользователей
- `GET /users/{user_id}` - Получение данных одного пользователя
- `PUT /users/{user_id}` - Обновление данных пользователя
- `DELETE /users/{user_id}` - Удаление пользователя
