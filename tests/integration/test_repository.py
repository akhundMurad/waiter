class TestSQLAlchemyRepository:
    def test_add_restaurant(self, restaurant_repo, restaurant):
        restaurant_repo.add(restaurant)

        assert restaurant_repo.get(restaurant.id) == restaurant

    def test_remove_restaurant(self, restaurant_repo, restaurant):
        restaurant_repo.add(restaurant)
        restaurant_repo.remove(restaurant.id)

        assert restaurant_repo.get(restaurant.id) is None
