import typing

from sqlalchemy.orm.session import Session

from domain.base.interface.unitofwork import UnitOfWorkInterface
from adapters.repository import sqlalchemy


class RestaurantUnitOfWork(UnitOfWorkInterface):
    def __init__(self, session_factory: typing.Callable):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.repository = sqlalchemy.RestaurantRepository(self.session)
        return self

    def __exit__(self, *args, **kwargs):
        self.session.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
