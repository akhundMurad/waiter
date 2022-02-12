from servicelayer.unitofwork import AbstractUnitOfWork, RestaurantUnitOfWork


def uow_provider() -> AbstractUnitOfWork:
    ...


def get_uow() -> RestaurantUnitOfWork:
    return RestaurantUnitOfWork()
