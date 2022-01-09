from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from adapters.orm import mapper_registry
from domain.models import start_mappers
from domain.valueobjects import Price, Table
from domain import models
import settings


@pytest.fixture
def restaurant():
    return models.Restaurant(name='name')


@pytest.fixture
def table(restaurant):
    return Table(index=1, restaurant=restaurant)


@pytest.fixture
def price():
    return Price(value=Decimal('2.0'))


@pytest.fixture
def menu_item(restaurant, price):
    menu_item = restaurant.add_menu_item(
        title='title', description='desc', price=price
    )
    return menu_item


@pytest.fixture
def empty_order(restaurant):
    restaurant.add_table()
    return models.Order(table=list(restaurant.tables)[0],
                        restaurant=restaurant)


@pytest.fixture(scope='session')
def pg_db():
    engine = create_engine(settings.get_postgres_uri())
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(pg_db):
    clear_mappers()
    start_mappers()
    yield sessionmaker(pg_db)
    clear_mappers()
