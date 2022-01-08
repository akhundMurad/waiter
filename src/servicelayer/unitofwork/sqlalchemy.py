from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

import settings
from . import AbstractUnitOfWork
from adapters.repository import sqlalchemy


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        settings.get_postgres_uri(),
        isolation_level='REPEATABLE READ'
    )
)


class RestaurantUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
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
