import typing

import qrcode

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from . import exceptions
from .base import Entity


def valueobject(cls):
    def __post_init__(self):
        validation_methods = self._get_validation_methods()
        for method in validation_methods:
            method()

    def _get_validation_methods(self) -> list[typing.Callable]:
        methods: list[typing.Callable] = list()
        for method in dir(self):
            if method.split('_')[0] == 'validate':
                methods.append(getattr(self, method))

        return methods

    setattr(cls, '__post_init__', __post_init__)
    setattr(cls, '_get_validation_methods', _get_validation_methods)

    return dataclass(cls, init=True, repr=True, order=True, eq=True)


@valueobject
class Price:
    value: Decimal = Decimal('0.0')

    def __composite_values__(self):
        return self.value,

    def validate_value(self):
        if self.value < 0:
            raise exceptions.PriceValueIsLessThanZero(
                'Price cannot be less than zero.'
            )


@valueobject
class Table:
    index: int
    restaurant: Entity

    def validate_index(self):
        if self.index < 0:
            raise exceptions.TableIndexIsLessThanZero(
                'Table index cannot be less than zero.'
            )


@valueobject
class QRCode:
    table: Table
    restaurant: Entity

    _qrcode_obj: Optional[qrcode.QRCode] = field(default=None, init=False)

    @property
    def qrcode_obj(self) -> qrcode.QRCode:
        if self._qrcode_obj is None:
            self._setup_qrcode_obj()
        return self._qrcode_obj

    def _setup_qrcode_obj(self) -> None:
        qrcode_obj = qrcode.QRCode()

        qrcode_obj.add_data({
            'table': self.table.index,
            'restaurant': self.restaurant.id
        })

        qrcode_obj.make(fit=True)
        self._qrcode_obj = qrcode_obj
