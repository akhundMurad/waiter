import uuid

from fastapi import status, Depends
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse

from entrypoints.providers.uow import uow_provider
from domain.restaurant import dto
from servicelayer import handlers
from servicelayer.unitofwork.abstract import AbstractUnitOfWork

router = APIRouter(
    prefix='/menu-item',
    tags=['menu-item']
)


@router.post(
    '/{restaurant_id}/',
    response_model=dto.MenuItemRead
)
def create_menu_item_to_restaurant(
        restaurant_id: uuid.UUID,
        menu_item: dto.MenuItemWrite,
        uow: AbstractUnitOfWork = Depends(uow_provider)
) -> JSONResponse:
    menu_item = handlers.create_menu_item_to_restaurant(
        restaurant_id=restaurant_id,
        title=menu_item.title,
        description=menu_item.description,
        price=menu_item.price,
        uow=uow
    )

    return JSONResponse(
        content=menu_item.dict(),
        status_code=status.HTTP_201_CREATED
    )
