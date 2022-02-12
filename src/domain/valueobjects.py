import qrcode

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from . import exceptions
from .base import Entity


@dataclass(init=True, repr=True, order=True, eq=True)
class Price:
    value: Decimal = Decimal('0.0')

    def __composite_values__(self):
        return self.value,

    def validate_value(self):
        if self.value < 0:
            raise exceptions.PriceValueIsLessThanZero(
                'Price cannot be less than zero.'
            )


@dataclass(init=True, repr=True, order=True, eq=True)
class Table:
    index: int
    restaurant: Entity

    def validate_index(self):
        if self.index < 0:
            raise exceptions.TableIndexIsLessThanZero(
                'Table index cannot be less than zero.'
            )


@dataclass(init=True, repr=True, order=True, eq=True)
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
