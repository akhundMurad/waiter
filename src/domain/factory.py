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
        vo_obj = vo_cls(**data)

        validate_vo(vo_obj)

        return vo_obj


def validate_vo(vo_obj: typing.Any) -> None:
    for method in _get_validation_methods(vo_obj):
        method()


def _get_validation_methods(vo_obj: typing.Any) -> typing.Generator:
    for method in dir(vo_obj):
        if method.split('_')[0] == 'validate':
            yield getattr(vo_obj, method)
