import typing
from uuid import UUID

from domain.base import models


class RepositoryInterface(typing.Protocol):
    def add(self, entity: models.Entity) -> None:
        ...

    def get(self, uuid: UUID) -> models.Entity:
        ...

    def remove(self, uuid: UUID) -> None:
        ...
