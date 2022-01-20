import uuid

import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import settings
from servicelayer import unitofwork, handlers
from entrypoints.fastapi import schema


app = FastAPI()


@app.post('/restaurant/{restaurant_id}/table/')
def add_table_to_restaurant(restaurant_id: uuid.UUID) -> JSONResponse:
    index = handlers.add_table_to_restaurant(
        restaurant_id, unitofwork.RestaurantUnitOfWork()
    )

    data = jsonable_encoder({'index': index})

    return JSONResponse(
        content=data, status_code=status.HTTP_201_CREATED
    )


@app.post(
    '/restaurant/{restaurant_id}/menu-item/',
    response_model=schema.MenuItemRead
)
def create_menu_item_to_restaurant(
        restaurant_id: uuid.UUID,
        menu_item: schema.MenuItemWrite
) -> JSONResponse:
    menu_item = handlers.create_menu_item_to_restaurant(
        restaurant_id=restaurant_id,
        title=menu_item.title,
        description=menu_item.description,
        price=menu_item.price,
        uow=unitofwork.RestaurantUnitOfWork()
    )

    data = jsonable_encoder(menu_item)

    return JSONResponse(
        content=schema.MenuItemRead(**data).dict(),
        status_code=status.HTTP_201_CREATED
    )


@app.post(
    '/restaurant/{restaurant_id}/order/',
    response_model=schema.OrderRead
)
def make_order(
        restaurant_id: uuid.UUID,
        order: schema.OrderWrite
) -> JSONResponse:
    order = handlers.make_order(
        restaurant_id=restaurant_id,
        order_mapping=[
            order_mapping.dict()
            for order_mapping in order.order_mapping
        ],
        table=order.table,
        uow=unitofwork.RestaurantUnitOfWork()
    )

    return JSONResponse(
        content=schema.OrderRead(**order).dict(),
        status_code=status.HTTP_201_CREATED
    )


if __name__ == '__main__':
    uvicorn.run(app=app, host=settings.API_HOST, port=settings.API_HOST,
                reload=True, debug=True)
