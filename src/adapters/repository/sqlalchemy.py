from uuid import UUID

from sqlalchemy.orm import Session

from domain import models
from domain.repository import AbstractRepository


class RestaurantRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, restaurant: models.Restaurant):
        self.session.add(restaurant)

    def get(self, uuid: UUID) -> models.Restaurant:
        return self.session.query(models.Restaurant).filter_by(
            id=uuid
        ).first()

    def remove(self, uuid: UUID):
        self.session.query(models.Restaurant).filter_by(
            id=uuid
        ).delete()


class MenuItemRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, menu_item: models.MenuItem):
        self.session.add(menu_item)

    def get(self, uuid: UUID) -> models.MenuItem:
        return self.session.query(models.MenuItem).filter_by(
            id=uuid
        ).first()

    def remove(self, uuid: UUID):
        self.session.query(models.MenuItem).filter_by(
            id=uuid
        ).delete()


class OrderRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, order: models.Order):
        self.session.add(order)

    def get(self, uuid: UUID) -> models.Order:
        return self.session.query(models.Order).filter_by(
            id=uuid
        ).first()

    def remove(self, uuid: UUID):
        self.session.query(models.Order).filter_by(
            id=uuid
        ).delete()
