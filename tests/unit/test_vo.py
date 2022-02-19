from decimal import Decimal

import pytest

from waiter.src.domain.exceptions import PriceValueIsLessThanZero, \
    TableIndexIsLessThanZero
from waiter.src.domain.valueobjects import Price, Table


def test_raise_price_value_is_less_than_zero():
    with pytest.raises(
        PriceValueIsLessThanZero,
        match='Price cannot be less than zero.'
    ):
        Price(value=Decimal(-0.2))


def test_raise_table_index_is_less_than_zero(restaurant):
    with pytest.raises(
        TableIndexIsLessThanZero,
        match='Table index cannot be less than zero.'
    ):
        Table(index=-1, restaurant=restaurant)
