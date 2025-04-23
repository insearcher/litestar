from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.params import Parameter
from litestar.status_codes import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from src.db.models import User
from src.db.repositories import UserRepository
from src.domain.users.schemas import (UserCreateSchema, UserSchema,
                                      UserUpdateSchema)


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    """Провайдер репозитория пользователей."""
    return UserRepository(session=db_session)


class UserController(Controller):
    """Контроллер для управления пользователями."""

    path = "/users"
    dependencies = {"user_repo": Provide(provide_user_repo)}

    @post(status_code=HTTP_201_CREATED)
    async def create_user(
        self, user_repo: UserRepository, data: UserCreateSchema
    ) -> UserSchema:
        """Создание нового пользователя."""
        user = User(
            name=data.name,
            surname=data.surname,
            password=data.password,
        )
        await user_repo.add(user)

        result = UserSchema(
            id=user.id,
            name=user.name,
            surname=user.surname,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        await user_repo.session.commit()
        return result

    @get()
    async def list_users(self, user_repo: UserRepository) -> List[UserSchema]:
        """Получение списка пользователей."""
        users = await user_repo.list()
        return [
            UserSchema(
                id=user.id,
                name=user.name,
                surname=user.surname,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ]

    @get("/{user_id:int}")
    async def get_user(
        self,
        user_repo: UserRepository,
        user_id: int = Parameter(title="ID пользователя"),
    ) -> UserSchema:
        """Получение данных одного пользователя."""
        user = await user_repo.get(user_id)
        return UserSchema(
            id=user.id,
            name=user.name,
            surname=user.surname,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_repo: UserRepository,
        data: UserUpdateSchema,
        user_id: int = Parameter(title="ID пользователя"),
    ) -> UserSchema:
        """Обновление данных пользователя."""
        user = await user_repo.get(user_id)

        if data.name is not None:
            user.name = data.name
        if data.surname is not None:
            user.surname = data.surname
        if data.password is not None:
            user.password = data.password
        await user_repo.update(user)

        result = UserSchema(
            id=user.id,
            name=user.name,
            surname=user.surname,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        await user_repo.session.commit()

        return result

    @delete("/{user_id:int}", status_code=HTTP_204_NO_CONTENT)
    async def delete_user(
        self,
        user_repo: UserRepository,
        user_id: int = Parameter(title="ID пользователя"),
    ) -> None:
        """Удаление пользователя."""
        await user_repo.delete(user_id)
        await user_repo.session.commit()
