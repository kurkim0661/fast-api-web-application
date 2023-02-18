from fastapi import APIRouter
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from fastapi.openapi.models import Response

from webapp.main.containers import Container
from webapp.main.buiseness.user_service import UserService
from webapp.main.domain.dto.user import UserDTO
from webapp.main.infra.persistence.user_repository import UserRepository

router = APIRouter()


@router.get("/users")
@inject
def root(
        user_service: UserService = Depends(Provide[Container.user_service])
):
    return user_service.get_users()


@router.get("/no_di")
def test():
    return {"data": "test data"}


@router.get("/users/{id}")
@inject
def get_by_id(id: int,
              user_service: UserService =
              Depends(Provide[Container.user_service])):
    return user_service.user_by_id(id)


@router.post("/users/add")
@inject
def add(user: UserDTO, user_service: UserService = Depends(Provide[Container.user_service])):
    user_service.create_user(user.username, user.email, user.hashed_password)
    return Response(status_code=201, description="유저가 추가됐다")


@router.get("/users/remove/{id}")
@inject
def remove(id: int,
           user_repository: UserRepository =
           Depends(Provide[Container.users_repository])):
    return user_repository.delete_by_id(id)
