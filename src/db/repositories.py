from typing import List, Optional, Type, TypeVar, Generic

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Базовый репозиторий для работы с моделями."""
    
    model: Type[T]
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, instance: T) -> T:
        """Добавить экземпляр модели."""
        self.session.add(instance)
        return instance
    
    async def get(self, id: int) -> Optional[T]:
        """Получить экземпляр модели по ID."""
        return await self.session.get(self.model, id)
    
    async def list(self) -> List[T]:
        """Получить список всех экземпляров модели."""
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())
    
    async def delete(self, id: int) -> None:
        """Удалить экземпляр модели по ID."""
        await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )


class UserRepository(BaseRepository[User]):
    """Репозиторий для работы с пользователями."""
    
    model = User
