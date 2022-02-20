from uuid import UUID

from sqlalchemy.orm import Session

from domain.restaurant import models
from domain.base.interface.repository import RepositoryInterface


class RestaurantRepository(RepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: models.Restaurant) -> None:
        self.session.add(entity)

    def get(self, uuid: UUID) -> models.Restaurant:
        return self.session.query(models.Restaurant).filter_by(
            id=uuid
        ).first()

    def remove(self, uuid: UUID):
        self.session.query(models.Restaurant).filter_by(
            id=uuid
        ).delete()
