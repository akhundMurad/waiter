import logging
import uuid

from sqlalchemy.orm import relationship

from adapters import orm
from domain.exceptions import WrongMenuItemForRestaurant, \
    WrongTableForRestaurant
from waiter.src.domain.valueobjects import Price, Table


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


class Entity:
    def __init__(self, id: uuid.UUID = None):
        self.id = id or generate_uuid()

    def __eq__(self, other) -> bool:
        if isinstance(other, Entity):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)


class Restaurant(Entity):
    def __init__(self, name: str, id: uuid.UUID = None):
        super().__init__(id)
        self.name = name
        self.tables = set()
        self.menu_items = set()

    def add_table(self):
        previous_table_index = self.get_previous_table_index()
        table = Table(index=previous_table_index + 1)
        self.tables.add(table)

    def get_previous_table_index(self) -> int:
        try:
            index = min([table.index for table in self.tables])
        except ValueError:
            index = 0
        return index

    def add_menu_item(self, title: str,
                      description: str, price: Price) -> "MenuItem":
        menu_item = MenuItem(title=title, description=description,
                             price=price, restaurant=self)
        self.menu_items.add(menu_item)
        return menu_item


class MenuItem(Entity):
    def __init__(self, title: str, description: str,
                 price: Price, restaurant: Restaurant, id: uuid.UUID = None):
        super().__init__(id)
        self.title = title
        self.description = description
        self.price = price
        self.restaurant = restaurant

    def order_item(self, table: Table) -> "Order":
        if table not in self.restaurant.tables:
            raise WrongTableForRestaurant(
                'Table does not exist in this restaurant.'
            )
        order = Order(table=table, restaurant=self.restaurant)
        order.add_menu_item(self)
        return order


class Order(Entity):
    def __init__(self, table: Table, restaurant: Restaurant,
                 id: uuid.UUID = None):
        super().__init__(id)
        self.table = table
        self.ordered_menu_items = set()
        self.restaurant = restaurant
        self.total_price = Price()

    def add_menu_item(self, menu_item: MenuItem):
        if menu_item not in self.restaurant.menu_items:
            raise WrongMenuItemForRestaurant(
                'Menu item does not exist in this restaurant.'
            )

        self.add_to_total_price(menu_item)

        self.ordered_menu_items.add(menu_item)

    def add_to_total_price(self, menu_item: MenuItem):
        self.total_price = Price(
            value=self.total_price.value + menu_item.price.value
        )


logger = logging.getLogger(__name__)


def start_mappers():
    logger.info('Starting mappers...')

    orm.mapper_registry.map_imperatively(Restaurant, orm.restaurant)
    orm.mapper_registry.map_imperatively(
        Order,
        orm.order,
        properties={
            'ordered_menu_items': relationship(
                MenuItem,
                secondary=orm.order_and_menu_item_association_table,
                back_populates='orders'
            )
        }
    )
    orm.mapper_registry.map_imperatively(
        MenuItem,
        orm.menu_item,
        properties={
            'orders': relationship(
                Order,
                secondary=orm.order_and_menu_item_association_table,
                back_populates='ordered_menu_items'
            )
        }
    )
