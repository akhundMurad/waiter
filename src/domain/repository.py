from abc import ABC, abstractmethod
from uuid import UUID

from domain import models


class AbstractRepository(ABC):
    @abstractmethod
    def add_restaurant(self, restaurant: models.Restaurant):
        pass

    @abstractmethod
    def get_restaurant(self, restaurant_id: UUID) -> models.Restaurant:
        pass

    @abstractmethod
    def remove_restaurant(self, restaurant_id: UUID):
        pass

    @abstractmethod
    def add_menu_item(self, menu_item: models.MenuItem):
        pass

    @abstractmethod
    def get_menu_item(self, menu_item_id: UUID) -> models.MenuItem:
        pass

    @abstractmethod
    def remove_menu_item(self, menu_item_id: UUID):
        pass

    @abstractmethod
    def add_order(self, order: models.Order):
        pass

    @abstractmethod
    def get_order(self, order_id: UUID) -> models.Order:
        pass

    @abstractmethod
    def remove_order(self, order_id: UUID):
        pass