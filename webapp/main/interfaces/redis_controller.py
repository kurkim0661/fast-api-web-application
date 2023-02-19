from fastapi import APIRouter
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from webapp.main.containers import Container
from webapp.main.buiseness.redis_service import Service

router = APIRouter()


@router.api_route("/redis")
@inject
async def index(service: Service = Depends(Provide[Container.redis_service])):
    value = await service.process()
    return {"result": value}
