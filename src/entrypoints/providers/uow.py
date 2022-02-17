from servicelayer.unitofwork.abstract import AbstractUnitOfWork
from servicelayer.unitofwork.sqlalchemy import RestaurantUnitOfWork


def uow_provider() -> AbstractUnitOfWork:
    ...


def get_uow() -> RestaurantUnitOfWork:
    return RestaurantUnitOfWork()
