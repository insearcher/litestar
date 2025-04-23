from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.di import Provide

from src.core.config import settings
from src.db.session import provide_db_session
from src.domain.users.controllers import UserController

# Инициализация приложения LiteStar
app = Litestar(
    route_handlers=[UserController],
    openapi_config=OpenAPIConfig(
        title=settings.APP_TITLE,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        path="/openapi.json",
        root_schema_site="swagger",  # Использовать Swagger UI по умолчанию
    ),
    debug=settings.DEBUG,
    dependencies={"db_session": Provide(provide_db_session)},
)
