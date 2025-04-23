from datetime import datetime
from typing import Optional

import msgspec

class UserSchema(msgspec.Struct):
    """Схема для возврата данных пользователя."""
    
    id: int
    name: str
    surname: str
    created_at: datetime
    updated_at: datetime

class UserCreateSchema(msgspec.Struct):
    """Схема для создания пользователя."""
    
    name: str
    surname: str
    password: str

class UserUpdateSchema(msgspec.Struct):
    """Схема для обновления пользователя."""
    
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None
