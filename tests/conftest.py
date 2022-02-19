from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from adapters.orm import get_connection_string
from domain.models import start_mappers
from domain.valueobjects import Price, Table
from domain import models
from domain import repository
from adapters.repository import sqlalchemy as sa_repo
from settings import Settings


@pytest.fixture
def restaurant() -> models.Restaurant:
    return models.Restaurant(name='name')


@pytest.fixture
def table(restaurant) -> Table:
    return Table(index=1, restaurant=restaurant)


@pytest.fixture
def price() -> Price:
    return Price(value=Decimal(2.0))


@pytest.fixture
def menu_item(restaurant, price) -> models.MenuItem:
    menu_item = restaurant.create_menu_item(
        title='title', description='desc', price=price
    )
    return menu_item


@pytest.fixture
def empty_order(restaurant) -> models.Order:
    restaurant.add_table()
    return models.Order(
        table=restaurant.tables[0],
        restaurant=restaurant
    )


@pytest.fixture
def settings() -> Settings:
    return Settings(
        postgres_host='localhost',
        postgres_port=5432,
        postgres_password='waiter',
        postgres_name='waiter',
        postgres_user='waiter'
    )


@pytest.fixture(scope='session')
def pg_db(settings):
    engine = create_engine(get_connection_string(settings))
    return engine


@pytest.fixture
def session_factory(pg_db):
    clear_mappers()
    start_mappers()
    yield sessionmaker(pg_db)
    clear_mappers()


@pytest.fixture
def restaurant_repo(session_factory) -> repository.AbstractRepository:
    session = session_factory()
    repo = sa_repo.RestaurantRepository(session)
    return repo
