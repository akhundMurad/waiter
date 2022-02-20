import typing
from uuid import UUID

from domain.base.models.entity import Entity


class RepositoryInterface(typing.Protocol):
    def add(self, entity: Entity) -> None:
        ...

    def get(self, uuid: UUID) -> Entity:
        ...

    def remove(self, uuid: UUID) -> None:
        ...
