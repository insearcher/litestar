import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Загрузка переменных окружения из .env файла
load_dotenv()


class AppSettings(BaseSettings):
    """Настройки приложения."""

    # Настройки базы данных
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/user"
    )

    # Настройки приложения
    APP_TITLE: str = "User Management API"
    APP_DESCRIPTION: str = "REST API for managing users"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Игнорировать дополнительные поля


# Экземпляр настроек для использования в приложении
settings = AppSettings()
