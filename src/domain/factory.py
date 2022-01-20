import typing
import uuid

from domain.base import Entity


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


class EntityFactory:
    @classmethod
    def build(cls, *, entity_cls: typing.Type[Entity], **data) -> Entity:
        return entity_cls(
            id=generate_uuid(),
            **data
        )


class ValueObjectFactory:
    @classmethod
    def build(cls, *, vo_cls: typing.Any, **data) -> typing.Any:
        return vo_cls(**data)
