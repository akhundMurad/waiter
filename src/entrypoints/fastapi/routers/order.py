import uuid

from fastapi.routing import APIRouter
from fastapi import status, Depends
from starlette.responses import JSONResponse

from entrypoints.fastapi import schema
from entrypoints.providers.uow import uow_provider
from servicelayer import handlers
from servicelayer.unitofwork import AbstractUnitOfWork

router = APIRouter(
    # prefix='order',
    tags=['order']
)


@router.post(
    '/restaurant/{restaurant_id}/order/',
    response_model=schema.OrderRead
)
def make_order(
        restaurant_id: uuid.UUID,
        order: schema.OrderWrite,
        uow: AbstractUnitOfWork = Depends(uow_provider)
) -> JSONResponse:
    order = handlers.make_order(
        restaurant_id=restaurant_id,
        order_mapping=[
            order_mapping.dict()
            for order_mapping in order.order_mapping
        ],
        table=order.table,
        uow=uow
    )

    return JSONResponse(
        content=schema.OrderRead(**order).dict(),
        status_code=status.HTTP_201_CREATED
    )

