import logging
from uuid import UUID

from sqlalchemy.orm import Session, relationship

from domain import models
from domain.repository import AbstractRepository


class FakeRepository(AbstractRepository):
    restaurants: set[models.Restaurant] = set()
    menu_items: set[models.MenuItem] = set()
    orders: set[models.Order] = set()

    def add_restaurant(self, restaurant: models.Restaurant):
        self.restaurants.add(restaurant)

    def get_restaurant(self, restaurant_id: UUID) -> models.Restaurant:
        restaurant = list(filter(
            lambda x: x.id == restaurant_id,
            self.restaurants
        ))[0]
        return restaurant

    def remove_restaurant(self, restaurant: models.Restaurant):
        self.restaurants.remove(restaurant)

    def add_order(self, order: models.Order):
        self.orders.add(order)

    def get_order(self, order_id: UUID) -> models.Order:
        order = list(filter(
            lambda x: x.id == order_id,
            self.orders
        ))[0]
        return order

    def remove_order(self, order: models.Order):
        self.orders.remove(order)

    def add_menu_item(self, menu_item: models.MenuItem):
        self.menu_items.add(menu_item)

    def get_menu_item(self, menu_item_id: UUID) -> models.MenuItem:
        menu_item = list(filter(
            lambda x: x.id == menu_item_id,
            self.menu_items
        ))[0]
        return menu_item

    def remove_menu_item(self, menu_item: models.MenuItem):
        self.menu_items.remove(menu_item)


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_restaurant(self, restaurant: models.Restaurant):
        self.session.add(restaurant)

    def get_restaurant(self, restaurant_id: UUID) -> models.Restaurant:
        return self.session.query(models.Restaurant).filter_by(
            id=restaurant_id
        ).first()

    def remove_restaurant(self, restaurant_id: UUID):
        self.session.query(models.Restaurant).filter_by(
            id=restaurant_id
        ).delete()

    def add_menu_item(self, menu_item: models.MenuItem):
        self.session.add(menu_item)

    def get_menu_item(self, menu_item_id: UUID) -> models.MenuItem:
        return self.session.query(models.MenuItem).filter_by(
            id=menu_item_id
        ).first()

    def remove_menu_item(self, menu_item_id: UUID):
        self.session.query(models.MenuItem).filter_by(
            id=menu_item_id
        ).delete()

    def add_order(self, order: models.Order):
        self.session.add(order)

    def get_order(self, order_id: UUID) -> models.Order:
        return self.session.query(models.Order).filter_by(
            id=order_id
        ).first()

    def remove_order(self, order_id: UUID):
        self.session.query(models.Order).filter_by(
            id=order_id
        ).delete()
