from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from adapters.orm import get_sa_sessionmaker
from domain.models import start_mappers
from entrypoints.fastapi.routers import table, menuitem, order
from entrypoints.providers.uow import uow_provider, get_uow
from entrypoints.providers.settings import get_settings, settings_provider


def get_app(do_mapping: bool = True) -> FastAPI:
    application = FastAPI()

    sa_sessionmaker = get_sa_sessionmaker()

    if do_mapping:
        start_mappers()

    application.include_router(table.router)
    application.include_router(menuitem.router)
    application.include_router(order.router)

    application.dependency_overrides[uow_provider] = get_uow
    application.dependency_overrides[sessionmaker] = sa_sessionmaker
    application.dependency_overrides[settings_provider] = get_settings

    return application


app = get_app()
