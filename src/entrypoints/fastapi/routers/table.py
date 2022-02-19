import uuid

from fastapi import status, Depends
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse

from domain import dto
from entrypoints.providers.uow import uow_provider
from servicelayer import handlers
from servicelayer.unitofwork.abstract import AbstractUnitOfWork

router = APIRouter(
    prefix='/table',
    tags=['table']
)


@router.post(
    '/{restaurant_id}/',
    response_model=dto.TableRead
)
def add_table_to_restaurant(
        restaurant_id: uuid.UUID,
        uow: AbstractUnitOfWork = Depends(uow_provider)
) -> JSONResponse:
    table = handlers.add_table_to_restaurant(
        restaurant_id=restaurant_id, uow=uow
    )

    return JSONResponse(
        content=table.dict(), status_code=status.HTTP_201_CREATED
    )
