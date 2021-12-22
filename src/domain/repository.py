from abc import ABC, abstractmethod
from uuid import UUID

from domain import models


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def get(self, uuid: UUID) -> models.Entity:
        pass

    @abstractmethod
    def remove(self, uuid: UUID) -> None:
        pass
