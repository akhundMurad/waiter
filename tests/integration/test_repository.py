import pytest

from domain import repository
from adapters.repository import sqlalchemy as sa_repo


@pytest.fixture
def restaurant_repo(session_factory) -> repository.AbstractRepository:
    session = session_factory()
    repo = sa_repo.RestaurantRepository(session)
    return repo


@pytest.fixture
def menu_item_repo(session_factory) -> repository.AbstractRepository:
    session = session_factory()
    repo = sa_repo.MenuItemRepository(session)
    return repo


@pytest.fixture
def order_repo(session_factory) -> repository.AbstractRepository:
    session = session_factory()
    repo = sa_repo.OrderRepository(session)
    return repo


class TestSQLAlchemyRepository:
    def test_add_restaurant(self, restaurant_repo, restaurant):
        restaurant_repo.add(restaurant)

        assert restaurant_repo.get(restaurant.id) == restaurant

    def test_remove_restaurant(self, restaurant_repo, restaurant):
        restaurant_repo.add(restaurant)
        restaurant_repo.remove(restaurant.id)

        assert restaurant_repo.get(restaurant.id) is None

    def test_add_menu_item(self, menu_item_repo, menu_item):
        menu_item_repo.add(menu_item)

        assert menu_item_repo.get(menu_item.id) == menu_item

    def test_remove_menu_item(self, menu_item_repo, menu_item):
        menu_item_repo.add(menu_item)
        menu_item_repo.remove(menu_item.id)

        assert menu_item_repo.get(menu_item.id) is None

    def test_add_order(self, order_repo, empty_order):
        order_repo.add(empty_order)

        assert order_repo.get(empty_order.id) == empty_order

    def test_remove_order(self, order_repo, empty_order):
        order_repo.add(empty_order)
        order_repo.remove(empty_order.id)

        assert order_repo.get(empty_order.id) is None
