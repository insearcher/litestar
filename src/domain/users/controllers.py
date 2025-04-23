from typing import List, Optional

from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.params import Parameter, Query
from litestar.status_codes import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from passlib.hash import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.db.repositories import UserRepository
from src.domain.users.schemas import (UserCreateSchema, UserSchema,
                                      UserUpdateSchema)


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    """Провайдер репозитория пользователей.
    
    Args:
        db_session: Асинхронная сессия SQLAlchemy.
        
    Returns:
        UserRepository: Репозиторий для работы с пользователями.
    """
    return UserRepository(session=db_session)


def user_to_schema(user: User) -> UserSchema:
    """Преобразует модель пользователя в схему DTO.
    
    Args:
        user: Экземпляр модели пользователя.
        
    Returns:
        UserSchema: Схема DTO с данными пользователя.
    """
    return UserSchema(
        id=user.id,
        name=user.name,
        surname=user.surname,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


class UserController(Controller):
    """Контроллер для управления пользователями через REST API."""

    path = "/users"
    dependencies = {"user_repo": Provide(provide_user_repo)}

    @post(status_code=HTTP_201_CREATED)
    async def create_user(
        self, user_repo: UserRepository, data: UserCreateSchema
    ) -> UserSchema:
        """Создание нового пользователя.
        
        Args:
            user_repo: Репозиторий пользователей.
            data: Данные для создания пользователя.
            
        Returns:
            UserSchema: Данные созданного пользователя.
            
        Raises:
            HTTPException: При ошибке создания пользователя.
        """
        try:
            user = User(
                name=data.name,
                surname=data.surname,
                password=bcrypt.hash(data.password),  # Хеширование пароля
            )
            
            async with user_repo.session.begin():
                await user_repo.add(user)
                
            return user_to_schema(user)
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Ошибка при создании пользователя: {str(e)}"
            )

    @get()
    async def list_users(
        self, 
        user_repo: UserRepository,
        page: int = Query(default=1, ge=1, title="Номер страницы"),
        page_size: int = Query(default=10, ge=1, le=100, title="Размер страницы")
    ) -> List[UserSchema]:
        """Получение списка пользователей с пагинацией.
        
        Args:
            user_repo: Репозиторий пользователей.
            page: Номер страницы.
            page_size: Количество записей на странице.
            
        Returns:
            List[UserSchema]: Список пользователей.
            
        Raises:
            HTTPException: При ошибке получения списка пользователей.
        """
        try:
            offset = (page - 1) * page_size
            users = await user_repo.list(limit=page_size, offset=offset)
            return [user_to_schema(user) for user in users]
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Ошибка при получении списка пользователей: {str(e)}"
            )

    @get("/{user_id:int}")
    async def get_user(
        self,
        user_repo: UserRepository,
        user_id: int = Parameter(title="ID пользователя"),
    ) -> UserSchema:
        """Получение данных одного пользователя.
        
        Args:
            user_repo: Репозиторий пользователей.
            user_id: Идентификатор пользователя.
            
        Returns:
            UserSchema: Данные пользователя.
            
        Raises:
            HTTPException: При отсутствии пользователя или ошибке получения данных.
        """
        try:
            user = await user_repo.get(user_id)
            if not user:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Пользователь с ID {user_id} не найден"
                )
            return user_to_schema(user)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Ошибка при получении пользователя: {str(e)}"
            )

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_repo: UserRepository,
        data: UserUpdateSchema,
        user_id: int = Parameter(title="ID пользователя"),
    ) -> UserSchema:
        """Обновление данных пользователя.
        
        Args:
            user_repo: Репозиторий пользователей.
            data: Данные для обновления.
            user_id: Идентификатор пользователя.
            
        Returns:
            UserSchema: Обновленные данные пользователя.
            
        Raises:
            HTTPException: При отсутствии пользователя или ошибке обновления данных.
        """
        try:
            user = await user_repo.get(user_id)
            if not user:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Пользователь с ID {user_id} не найден"
                )

            if data.name is not None:
                user.name = data.name
            if data.surname is not None:
                user.surname = data.surname
            if data.password is not None:
                user.password = bcrypt.hash(data.password)  # Хеширование при обновлении
                
            async with user_repo.session.begin():
                await user_repo.update(user)
                
            return user_to_schema(user)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Ошибка при обновлении пользователя: {str(e)}"
            )

    @delete("/{user_id:int}", status_code=HTTP_204_NO_CONTENT)
    async def delete_user(
        self,
        user_repo: UserRepository,
        user_id: int = Parameter(title="ID пользователя"),
    ) -> None:
        """Удаление пользователя.
        
        Args:
            user_repo: Репозиторий пользователей.
            user_id: Идентиф��катор пользователя.
            
        Raises:
            HTTPException: При ошибке удаления пользователя.
        """
        try:
            user = await user_repo.get(user_id)
            if not user:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Пользователь с ID {user_id} не найден"
                )
                
            async with user_repo.session.begin():
                await user_repo.delete(user_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Ошибка при удалении пользователя: {str(e)}"
            )
