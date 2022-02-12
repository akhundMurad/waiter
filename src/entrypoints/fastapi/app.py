from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from adapters.orm import get_sa_sessionmaker
from domain.models import start_mappers
from entrypoints.fastapi.routers import table, menuitem, order
from entrypoints.providers.uow import uow_provider, get_uow


def get_app(do_mapping: bool = True) -> FastAPI:
    app = FastAPI()

    sa_sessionmaker = get_sa_sessionmaker()

    if do_mapping:
        start_mappers()

    app.include_router(table.router)
    app.include_router(menuitem.router)
    app.include_router(order.router)

    app.dependency_overrides[uow_provider] = get_uow
    app.dependency_overrides[sessionmaker] = sa_sessionmaker

    return app


app = get_app()
