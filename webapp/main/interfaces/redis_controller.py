from fastapi import APIRouter
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from webapp.main.containers import Container
from webapp.main.business.redis_service import RedisService

router = APIRouter()


@router.api_route("/redis")
@inject
async def index(service: RedisService = Depends(Provide[Container.redis_service])):
    value = await service.process()
    return {"result": value}
