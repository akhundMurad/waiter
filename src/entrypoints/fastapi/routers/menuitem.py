import uuid

from fastapi import status, Depends
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse

from entrypoints.providers.uow import uow_provider
from entrypoints.fastapi import schema
from servicelayer import handlers
from servicelayer.unitofwork import AbstractUnitOfWork

router = APIRouter(
    # prefix='menu-item',
    tags=['menu-item']
)


@router.post(
    '/restaurant/{restaurant_id}/menu-item/',
    response_model=schema.MenuItemRead
)
def create_menu_item_to_restaurant(
        restaurant_id: uuid.UUID,
        menu_item: schema.MenuItemWrite,
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
        content=schema.MenuItemRead(**menu_item).dict(),
        status_code=status.HTTP_201_CREATED
    )
