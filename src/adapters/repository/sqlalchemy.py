from uuid import UUID

from sqlalchemy.orm import Session

from domain.restaurant import models
from domain.base.repository import AbstractRepository


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
