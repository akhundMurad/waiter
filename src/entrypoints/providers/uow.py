from fastapi import Request

from domain.base.interface.unitofwork import UnitOfWorkInterface
from servicelayer.unitofwork.sqlalchemy import RestaurantUnitOfWork


def uow_provider(request: Request) -> UnitOfWorkInterface:
    ...


def get_uow(request: Request) -> RestaurantUnitOfWork:
    return RestaurantUnitOfWork(request.app.state.sessionmaker)
