from fastapi import FastAPI

from domain.models import start_mappers
from entrypoints.fastapi.routers import table, menuitem, order
from entrypoints.providers.uow import uow_provider, get_uow


def get_app(do_mapping: bool = False) -> FastAPI:
    app = FastAPI()

    if do_mapping:
        start_mappers()

    app.include_router(table.router)
    app.include_router(menuitem.router)
    app.include_router(order.router)

    app.dependency_overrides[uow_provider] = get_uow

    return app
