from sqlalchemy.orm.session import Session

from .abstract import AbstractUnitOfWork
from adapters.repository import sqlalchemy


class RestaurantUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.repository = sqlalchemy.RestaurantRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args, **kwargs):
        super().__exit__(*args, **kwargs)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
