from fastapi import APIRouter, Depends

from webapp.main.dependencies import get_token_header

router = APIRouter(
    prefix="/something",
    tags=["something"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)