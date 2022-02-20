from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from adapters.orm import get_connection_string, mapper_registry
from domain.restaurant import models
from domain.base import repository
from adapters.repository import sqlalchemy as sa_repo
from settings import Settings


@pytest.fixture
def restaurant() -> models.Restaurant:
    return models.Restaurant(name='name')


@pytest.fixture
def table(restaurant) -> models.Table:
    return models.Table(index=1, restaurant=restaurant)


@pytest.fixture
def price() -> models.Price:
    return models.Price(value=Decimal(2.0))


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
        table=restaurant.tables.pop(),
        restaurant=restaurant
    )


@pytest.fixture
def settings() -> Settings:
    return Settings(
        postgres_host='localhost',
        postgres_port=5432,
        postgres_password='waiter',
        postgres_name='waiter',
        postgres_user='waiter',
        map_models=False
    )


@pytest.fixture
def pg_db(settings):
    engine = create_engine(get_connection_string(settings))
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(pg_db):
    clear_mappers()
    models.start_mappers()
    yield sessionmaker(pg_db)
    clear_mappers()


@pytest.fixture
def restaurant_repo(session_factory) -> repository.AbstractRepository:
    session = session_factory()
    repo = sa_repo.RestaurantRepository(session)
    return repo
