import pytest

from domain import repository
from adapters.repository import sqlalchemy as sa_repo


@pytest.fixture
def restaurant_repo(session_factory) -> repository.AbstractRepository:
    session = session_factory()
    repo = sa_repo.RestaurantRepository(session)
    return repo


class TestSQLAlchemyRepository:
    def test_add_restaurant(self, restaurant_repo, restaurant):
        restaurant_repo.add(restaurant)

        assert restaurant_repo.get(restaurant.id) == restaurant

    def test_remove_restaurant(self, restaurant_repo, restaurant):
        restaurant_repo.add(restaurant)
        restaurant_repo.remove(restaurant.id)

        assert restaurant_repo.get(restaurant.id) is None
