import uuid

from fastapi import status, Depends
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse

from domain.base.interface.unitofwork import UnitOfWorkInterface
from domain.restaurant import dto
from entrypoints.providers.uow import uow_provider
from servicelayer import services

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
        uow: UnitOfWorkInterface = Depends(uow_provider)
) -> JSONResponse:
    table = services.add_table_to_restaurant(
        restaurant_id=restaurant_id, uow=uow
    )

    return JSONResponse(
        content=table.dict(), status_code=status.HTTP_201_CREATED
    )
