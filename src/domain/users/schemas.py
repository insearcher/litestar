from datetime import datetime
from typing import Optional

import msgspec


class UserSchema(msgspec.Struct):
    """Схема для возврата данных пользователя.

    Attributes:
        id: Идентификатор пользователя.
        name: Имя пользователя.
        surname: Фамилия пользователя.
        created_at: Дата и время создания записи.
        updated_at: Дата и время последнего обновления записи.
    """

    id: int
    name: str
    surname: str
    created_at: datetime
    updated_at: datetime


class UserCreateSchema(msgspec.Struct):
    """Схема для создания пользователя.

    Attributes:
        name: Имя пользователя (от 1 до 100 символов).
        surname: Фамилия пользователя (от 1 до 100 символов).
        password: Пароль пользователя (минимум 8 символов).
    """

    name: str = msgspec.field()
    surname: str = msgspec.field()
    password: str = msgspec.field()


class UserUpdateSchema(msgspec.Struct):
    """Схема для обновления пользователя.

    Attributes:
        name: Имя пользователя (опционально, от 1 до 100 символов).
        surname: Фамилия пользователя (опционально, от 1 до 100 символов).
        password: Пароль пользователя (опционально, минимум 8 символов).
    """

    name: Optional[str] = msgspec.field()
    surname: Optional[str] = msgspec.field()
    password: Optional[str] = msgspec.field()
