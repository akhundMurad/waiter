import logging
import uuid

from domain.exceptions import WrongMenuItemForRestaurant, \
    WrongTableForRestaurant
from waiter.src.domain.valueobjects import Price, Table, QRCode

logger = logging.getLogger(__name__)


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

    def add_table(self):
        previous_table_index = self.get_previous_table_index()
        table = Table(index=previous_table_index + 1, restaurant=self)
        self.tables.append(table)

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
        self.menu_items.append(menu_item)
        return menu_item

    def order_menu_item(self, menu_item: 'MenuItem', table: Table) -> 'Order':
        if table not in self.tables:
            raise WrongTableForRestaurant(
                'Table does not exist in this restaurant.'
            )
        order = Order(table=table, restaurant=self)
        order.add_menu_item(menu_item)
        return order


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
                 id: uuid.UUID = None):
        super().__init__(id)
        self.table = table
        self.ordered_menu_items = list()
        self.restaurant = restaurant
        self.total_price = Price()

    def add_menu_item(self, menu_item: MenuItem):
        if menu_item not in self.restaurant.menu_items:
            raise WrongMenuItemForRestaurant(
                'Menu item does not exist in this restaurant.'
            )

        self.add_to_total_price(menu_item)

        self.ordered_menu_items.append(menu_item)

    def add_to_total_price(self, menu_item: MenuItem):
        self.total_price = Price(
            value=self.total_price.value + menu_item.price.value
        )


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
        Order,
        orm.order,
        properties={
            'restaurant': relationship(Restaurant),
            'ordered_menu_items': relationship(
                MenuItem,
                secondary=orm.order_and_menu_item_association_table,
                back_populates='orders'
            ),
            'total_price': composite(
                Price,
                orm.order.c.total_price_value
            ),
            'table': relationship(Table)
        }
    )
    orm.mapper_registry.map_imperatively(
        MenuItem,
        orm.menu_item,
        properties={
            'restaurant': relationship(Restaurant),
            'orders': relationship(
                Order,
                secondary=orm.order_and_menu_item_association_table,
                back_populates='ordered_menu_items'
            ),
            'price': composite(
                Price,
                orm.menu_item.c.price_value
            )
        }
    )
