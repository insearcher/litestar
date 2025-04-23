from typing import AsyncGenerator
from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig
from advanced_alchemy.extensions.litestar import SQLAlchemyInitPlugin
from sqlalchemy.ext.asyncio import AsyncSession
from advanced_alchemy.config import EngineConfig

from src.core.config import settings

# Конфигурация для движка SQLAlchemy
engine_config = EngineConfig(echo=settings.DEBUG)

# Конфигурация SQLAlchemy для асинхронного подключения
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=settings.DATABASE_URL,
    engine_config=engine_config,
    create_all=True  # Автоматически создавать таблицы при старте
)

# Инициализация плагина SQLAlchemy для Litestar
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)

# Провайдер сессии для внедрения зависимостей
async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Провайдер сессии БД для внедрения зависимостей."""
    async with sqlalchemy_config.create_session_factory()() as session:
        yield session
