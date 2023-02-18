from dependency_injector import containers, providers
from fastapi.security import OAuth2PasswordBearer

from webapp.main.infra.persistence.database import Database
from webapp.main.infra.persistence.user_repository import UserRepository
from webapp.main.buiseness.user_service import UserService
from .buiseness.auth_service import AuthService
from .infra import redis
from .buiseness import redis_service
from .infra.utils import jwt


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=config.db.url)

    users_repository = providers.Factory(
        UserRepository,
        create_table=db.provided.create_table,
        session_factory=db.provided.session)

    user_service = providers.Factory(
        UserService,
        users_repository=users_repository)

    auth_service = providers.Factory(
        AuthService,
        users_repository=users_repository)

    redis_pool = providers.Resource(
        redis.init_redis_pool,
        host=config.redis_host,
        password=config.redis_password,
    )

    redis_service = providers.Factory(
        redis_service.Service,
        redis=redis_pool,
    )

    jwt_util = providers.Factory(
        jwt.JwtUtil,
    )

    oauth2_scheme = providers.Factory(
        OAuth2PasswordBearer,
        tokenUrl="/token"
    )
