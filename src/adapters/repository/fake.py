from uuid import UUID

from domain import models
from domain.repository import AbstractRepository


class RestaurantRepository(AbstractRepository):
    restaurants: set[models.Restaurant] = set()

    def add(self, restaurant: models.Restaurant):
        self.restaurants.add(restaurant)

    def get(self, uuid: UUID) -> models.Restaurant:
        restaurant = list(filter(
            lambda x: x.id == uuid,
            self.restaurants
        ))[0]
        return restaurant

    def remove(self, restaurant: models.Restaurant):
        self.restaurants.remove(restaurant)


class OrderRepository(AbstractRepository):
    orders: set[models.Order] = set()

    def add(self, order: models.Order):
        self.orders.add(order)

    def get(self, uuid: UUID) -> models.Order:
        order = list(filter(
            lambda x: x.id == uuid,
            self.orders
        ))[0]
        return order

    def remove(self, order: models.Order):
        self.orders.remove(order)


class MenuItemRepository(AbstractRepository):
    menu_items: set[models.MenuItem] = set()

    def add(self, menu_item: models.MenuItem):
        self.menu_items.add(menu_item)

    def get(self, uuid: UUID) -> models.MenuItem:
        menu_item = list(filter(
            lambda x: x.id == uuid,
            self.menu_items
        ))[0]
        return menu_item

    def remove(self, menu_item: models.MenuItem):
        self.menu_items.remove(menu_item)
