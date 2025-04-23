from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.db.models import User


class UserRepository(SQLAlchemyAsyncRepository[User]):
    """Репозиторий для работы с пользователями на основе Advanced-SQLAlchemy."""

    model_type = User
