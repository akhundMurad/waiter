import importlib
from settings import UNIT_OF_WORK_TYPE
from .abstract import AbstractUnitOfWork  # noqa: F401


uow = importlib.import_module(
    f'servicelayer.unitofwork.{UNIT_OF_WORK_TYPE}'
)


RestaurantUnitOfWork = uow.RestaurantUnitOfWork
