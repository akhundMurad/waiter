import pytest

from adapters import repository


@pytest.fixture
def sa_repo(session_factory) -> repository.AbstractRepository:
    session = session_factory()
    repo = repository.SQLAlchemyRepository(session)
    return repo


class TestSQLAlchemyRepository:
    def test_add_restaurant(self, sa_repo, restaurant):
        sa_repo.add_restaurant(restaurant)

        assert sa_repo.get_restaurant(restaurant.id) == restaurant
