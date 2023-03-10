from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from webapp.main.containers import Container
from webapp.main.business.user_service import UserService
from . import router


@router.get("/exchange-flows")
@inject
def root(user_service: UserService = Depends(Provide[Container.user_service])):
    return user_service.get_users()
