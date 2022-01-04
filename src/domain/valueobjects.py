import qrcode

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Callable, Any, Optional

from waiter.src.domain.exceptions import PriceValueIsLessThanZero, \
    TableIndexIsLessThanZero


def vo(cls):
    """Value object decorator
    """
    def __post_init__(self):
        validation_methods = self._get_validation_methods()
        for method in validation_methods:
            method()

    def _get_validation_methods(self) -> list[Callable]:
        methods: list[Callable] = list()
        for method in dir(self):
            if method.split('_')[0] == 'validate':
                methods.append(getattr(self, method))

        return methods

    setattr(cls, '__post_init__', __post_init__)
    setattr(cls, '_get_validation_methods', _get_validation_methods)

    return dataclass(cls, init=True, repr=True, order=True)


@vo
class Price:
    value: Decimal = Decimal('0.0')

    def __composite_values__(self):
        return self.value,

    def validate_value(self):
        if self.value < 0:
            raise PriceValueIsLessThanZero('Price cannot be less than zero.')


@vo
class Table:
    index: int
    restaurant: Any

    def validate_index(self):
        if self.index < 0:
            raise TableIndexIsLessThanZero(
                'Table index cannot be less than zero'
            )


@vo
class QRCode:
    table: Table
    restaurant: Any

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
