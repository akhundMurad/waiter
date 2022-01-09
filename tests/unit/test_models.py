from decimal import Decimal
from qrcode import QRCode as QRCodeObj

import pytest

from domain.exceptions import WrongTableForRestaurant, \
    WrongMenuItemForRestaurant
from domain.models import Restaurant, MenuItem
from domain.valueobjects import Price, QRCode


class TestRestaurant:
    def test_add_table(self, restaurant):
        restaurant.add_table()
        restaurant.add_table()

        assert len(restaurant.tables) == 2
        assert 1 in [table.index for table in restaurant.tables]
        assert 2 in [table.index for table in restaurant.tables]

    def test_add_menu_item(self, restaurant):
        restaurant.add_menu_item(title='title', description='desc',
                                 price=Price(value=Decimal('2.0')))

        assert len(restaurant.menu_items) == 1

    def test_generate_qrcode(self, restaurant):
        restaurant.add_table()
        table = restaurant.tables[0]

        qrcode = restaurant.generate_qrcode(table)

        assert qrcode.restaurant == restaurant
        assert qrcode.table == table
        assert isinstance(qrcode.qrcode_obj,  QRCodeObj)

    def test_order_item_raise_exception(self, menu_item, table):
        with pytest.raises(WrongTableForRestaurant):
            menu_item.restaurant.make_order([
                {'menu_item': menu_item, 'quantity': 1}
            ], table)

    def test_order_item_added(self, menu_item):
        menu_item.restaurant.add_table()
        table = list(menu_item.restaurant.tables)[0]
        order = menu_item.restaurant.make_order([
            {'menu_item': menu_item, 'quantity': 1}
        ], table)

        assert order.restaurant.id == menu_item.restaurant.id
        assert len(order.order_items) > 0
        assert menu_item == order.order_items[0].menu_item
        assert table == order.table


class TestOrder:
    def test_add_menu_item_raises_exception(self, empty_order, price):
        restaurant = Restaurant(name='n')
        menu_item = MenuItem(
            title='title', description='desc',
            price=price, restaurant=restaurant
        )

        with pytest.raises(WrongMenuItemForRestaurant):
            empty_order.add_menu_item(menu_item, 1)

    def test_add_menu_item(self, empty_order, menu_item):
        empty_order.add_menu_item(menu_item, 1)

        assert len(empty_order.order_items) > 0
        assert menu_item == empty_order.order_items[0].menu_item
        assert empty_order.total_price.value == menu_item.price.value
