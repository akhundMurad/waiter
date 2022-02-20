import uuid

from fastapi.routing import APIRouter
from fastapi import status, Depends
from starlette.responses import JSONResponse

from domain.base.interface.unitofwork import UnitOfWorkInterface
from domain.restaurant import dto
from entrypoints.providers.uow import uow_provider
from servicelayer import services

router = APIRouter(
    prefix='/order',
    tags=['order']
)


@router.post(
    '/',
    response_model=dto.OrderRead
)
def make_order(
        order: dto.OrderWrite,
        uow: UnitOfWorkInterface = Depends(uow_provider)
) -> JSONResponse:
    order = services.make_order(
        restaurant_id=uuid.UUID(order.restaurant_id),
        order_mapping=[
            order_mapping.dict()
            for order_mapping in order.order_mapping
        ],
        table=order.table,
        uow=uow
    )

    return JSONResponse(
        content=order.dict(),
        status_code=status.HTTP_201_CREATED
    )
