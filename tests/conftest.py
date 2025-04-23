import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from litestar.testing import TestClient
from src.app import app
from src.db.models import User
from src.db.repositories import UserRepository

# Set test database URL
test_db_url = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/test_userdb",
)

# Create test engine
engine = create_async_engine(test_db_url, poolclass=NullPool)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Fixture that creates a new database session for a test."""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(User.metadata.create_all)

    async with async_session_maker() as session:
        yield session

    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(User.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def user_repository(db_session: AsyncSession) -> UserRepository:
    """Fixture that creates a user repository."""
    return UserRepository(session=db_session)


@pytest.fixture(scope="function")
def test_client() -> Generator[TestClient, None, None]:
    """Fixture that creates a test client for the application."""
    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
