from decimal import Decimal

import pytest

from domain.models import Restaurant, Order
from domain.valueobjects import Price, Table


@pytest.fixture
def table():
    return Table(index=1)


@pytest.fixture
def price():
    return Price(value=Decimal('2.0'))


@pytest.fixture
def restaurant(table):
    return Restaurant(name='name')


@pytest.fixture
def menu_item(restaurant, price):
    menu_item = restaurant.add_menu_item(
        title='title', description='desc', price=price
    )
    return menu_item


@pytest.fixture
def empty_order(restaurant):
    restaurant.add_table()
    return Order(table=list(restaurant.tables)[0], restaurant=restaurant)
