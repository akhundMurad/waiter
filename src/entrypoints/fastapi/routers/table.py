import uuid

from fastapi import status, Depends
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse

from entrypoints.providers.uow import uow_provider
from servicelayer import handlers
from servicelayer.unitofwork import AbstractUnitOfWork

router = APIRouter(
    # prefix='table',
    tags=['table']
)


@router.post('/restaurant/{restaurant_id}/table/')
def add_table_to_restaurant(
        restaurant_id: uuid.UUID,
        uow: AbstractUnitOfWork = Depends(uow_provider)
) -> JSONResponse:
    index = handlers.add_table_to_restaurant(
        restaurant_id=restaurant_id, uow=uow
    )

    return JSONResponse(
        content={'index': index}, status_code=status.HTTP_201_CREATED
    )
