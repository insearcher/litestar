from datetime import datetime

from advanced_alchemy.base import BigIntBase
from sqlalchemy import Column, DateTime, String, func, text
from sqlalchemy.orm import Mapped


class User(BigIntBase):
    """Модель пользователя.
    
    Attributes:
        name: Имя пользователя.
        surname: Фамилия пользователя.
        password: Хешированный пароль пользователя.
        created_at: Дата и время создания записи (UTC-0).
        updated_at: Дата и время последнего обновления записи (UTC-0).
    """

    __tablename__ = "user"

    name: Mapped[str] = Column(String, nullable=False)
    surname: Mapped[str] = Column(String, nullable=False)
    password: Mapped[str] = Column(String, nullable=False)
    
    # Сохраняем timezone=False для соответствия требованию UTC-0
    # Используем NOW() AT TIME ZONE 'UTC' для явного указания UTC
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=False), 
        server_default=text("(NOW() AT TIME ZONE 'UTC')"), 
        nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=False),
        server_default=text("(NOW() AT TIME ZONE 'UTC')"),
        onupdate=text("(NOW() AT TIME ZONE 'UTC')"),
        nullable=False,
    )
