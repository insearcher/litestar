from datetime import datetime
from typing import Optional

from advanced_alchemy.base import BigIntBase
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import Mapped

class User(BigIntBase):
    """Модель пользователя."""
    
    __tablename__ = "user"
    
    name: Mapped[str] = Column(String, nullable=False)
    surname: Mapped[str] = Column(String, nullable=False)
    password: Mapped[str] = Column(String, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
