from fastapi import Request

from servicelayer.unitofwork.abstract import AbstractUnitOfWork
from servicelayer.unitofwork.sqlalchemy import RestaurantUnitOfWork


def uow_provider(request: Request) -> AbstractUnitOfWork:
    ...


def get_uow(request: Request) -> RestaurantUnitOfWork:
    return RestaurantUnitOfWork(request.state.db_session)
