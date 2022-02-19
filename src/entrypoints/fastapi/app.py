from fastapi import FastAPI

from adapters.orm import get_sa_sessionmaker
from domain.models import start_mappers
from entrypoints.fastapi.routers import table, menuitem, order
from entrypoints.providers.uow import uow_provider, get_uow
from entrypoints.providers.settings import get_settings
from settings import Settings


def get_app(settings: Settings = get_settings()) -> FastAPI:
    application = FastAPI()

    sa_sessionmaker = get_sa_sessionmaker(settings)

    if settings.map_models:
        start_mappers()

    application.include_router(table.router)
    application.include_router(menuitem.router)
    application.include_router(order.router)

    application.state.settings = settings
    application.state.sessionmaker = sa_sessionmaker

    application.dependency_overrides[uow_provider] = get_uow

    return application


app = get_app()
