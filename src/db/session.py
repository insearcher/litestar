from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.core.config import settings

# Создаем асинхронный движок
engine = create_async_engine(settings.DATABASE_URL)

# Создаем фабрику асинхронных сессий
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

# Провайдер сессии для внедрения зависимостей
async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Провайдер сессии БД для внедрения зависимостей."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
