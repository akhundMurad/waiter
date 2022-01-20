import logging
import uuid
from typing import Optional

from domain.exceptions import WrongMenuItemForRestaurant, \
    WrongTableForRestaurant
from waiter.src.domain.valueobjects import Price, Table, QRCode
from .base import Entity
from .factory import ValueObjectFactory, EntityFactory

logger = logging.getLogger(__name__)


class Restaurant(Entity):
    def __init__(self, name: str, id: uuid.UUID = None,
                 tables=None, menu_items=None):
        super().__init__(id)
        self.name = name
        self.tables = tables or list()
        self.menu_items = menu_items or list()

    def generate_qrcode(self, table: Table) -> QRCode:
        if table not in self.tables:
            raise WrongTableForRestaurant(
                'Table does not exist in this restaurant.'
            )

        return QRCode(table=table, restaurant=self)

    def add_table(self) -> 'Table':
        previous_table_index = self.get_previous_table_index()
        table = ValueObjectFactory.build(
            vo_cls=Table, index=previous_table_index + 1, restaurant=self
        )
        self.tables.append(table)

        return table

    def get_table_by_index(self, index: int) -> Optional['Table']:
        table = list(filter(
            lambda x: x.index == index,
            self.tables
        ))

        if not table:
            return None
        return table[0]

    def get_previous_table_index(self) -> int:
        try:
            index = min([table.index for table in self.tables])
        except ValueError:
            index = 0
        return index

    def create_menu_item(self, title: str,
                         description: str,
                         price: Price) -> "MenuItem":
        menu_item = EntityFactory.build(
            entity_cls=MenuItem,
            title=title,
            description=description,
            price=price,
            restaurant=self
        )
        self.menu_items.append(menu_item)
        return menu_item

    def make_order(self, order_mapping: list[dict],
                   table: Table) -> 'Order':
        if table not in self.tables:
            raise WrongTableForRestaurant(
                'Table does not exist in this restaurant.'
            )
        order = EntityFactory.build(
            entity_cls=Order,
            table=table,
            restaurant=self
        )
        for order_map in order_mapping:
            menu_item = self._get_menu_item_by_id(order_map['menu_item'])
            order.add_menu_item(menu_item, order_map['quantity'])
        return order

    def _get_menu_item_by_id(self, menu_item_id: uuid.UUID) -> 'MenuItem':
        menu_item = list(
            filter(
                lambda x: x.id == menu_item_id,
                self.menu_items
            )
        )

        if not menu_item:
            raise WrongMenuItemForRestaurant(
                'Menu item does not exist in this restaurant.'
            )

        return menu_item[0]


class MenuItem(Entity):
    def __init__(self, title: str, description: str,
                 price: Price, restaurant: Restaurant, id: uuid.UUID = None):
        super().__init__(id)
        self.title = title
        self.description = description
        self.price = price
        self.restaurant = restaurant


class Order(Entity):
    def __init__(self, table: Table, restaurant: Restaurant,
                 order_items: list = None, id: uuid.UUID = None):
        super().__init__(id)
        self.table = table
        self.order_items = order_items or list()
        self.restaurant = restaurant
        self.total_price = Price()

    def add_menu_item(self, menu_item: MenuItem, quantity: int):
        if menu_item not in self.restaurant.menu_items:
            raise WrongMenuItemForRestaurant(
                'Menu item does not exist in this restaurant.'
            )

        self.add_to_total_price(menu_item, quantity)

        self.order_items.append(
            OrderItem(menu_item=menu_item, quantity=quantity)
        )

    def add_to_total_price(self, menu_item: MenuItem, quantity: int):
        self.total_price = Price(
            value=self.total_price.value + menu_item.price.value * quantity
        )


class OrderItem(Entity):
    def __init__(self, menu_item: MenuItem, quantity: int,
                 id: uuid.UUID = None):
        super().__init__(id)
        self.menu_item = menu_item
        self.quantity = quantity


def start_mappers():
    from sqlalchemy.orm import relationship, composite
    from adapters import orm

    logger.info('Starting mappers...')

    orm.mapper_registry.map_imperatively(
        Restaurant,
        orm.restaurant,
        properties={
            'orders': relationship(
                Order,
                back_populates='restaurant'
            ),
            'menu_items': relationship(
                MenuItem,
                back_populates='restaurant'
            ),
            'tables': relationship(
                Table,
                back_populates='restaurant'
            )
        }
    )
    orm.mapper_registry.map_imperatively(
        Table,
        orm.restaurant_table,
        properties={
            'restaurant': relationship(Restaurant),
        }
    )
    orm.mapper_registry.map_imperatively(
        OrderItem,
        orm.order_item,
        properties={
            'menu_item': relationship(MenuItem),
            'order': relationship(Order, back_populates='order_items')
        }
    )
    orm.mapper_registry.map_imperatively(
        Order,
        orm.order,
        properties={
            'restaurant': relationship(Restaurant),
            'total_price': composite(
                Price,
                orm.order.c.total_price_value
            ),
            'table': relationship(Table),
            'order_items': relationship(OrderItem, back_populates='order')
        }
    )
    orm.mapper_registry.map_imperatively(
        MenuItem,
        orm.menu_item,
        properties={
            'restaurant': relationship(Restaurant),
            'price': composite(
                Price,
                orm.menu_item.c.price_value
            )
        }
    )
