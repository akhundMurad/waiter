from uuid import UUID

from domain.exceptions import InvalidRestaurantUUID
from domain.models import MenuItem, Order
from domain.valueobjects import Table, Price
from servicelayer import unitofwork


def add_table_to_restaurant(
        restaurant_id: UUID,
        uow: unitofwork.AbstractUnitOfWork
) -> Table:
    with uow:
        restaurant = uow.repository.get(restaurant_id)
        if restaurant is None:
            raise InvalidRestaurantUUID('Invalid restaurant UUID.')
        table = restaurant.add_table()
        uow.commit()

    return table


def create_menu_item_to_restaurant(
        restaurant_id: UUID,
        title: str,
        description: str,
        price: Price,
        uow: unitofwork.AbstractUnitOfWork
) -> MenuItem:
    with uow:
        restaurant = uow.repository.get(restaurant_id)
        if restaurant is None:
            raise InvalidRestaurantUUID('Invalid restaurant UUID.')
        menu_item = restaurant.create_menu_item(
            title=title, description=description, price=price
        )
        uow.commit()

    return menu_item


def make_order(
        restaurant_id: UUID,
        order_mapping: list[dict],
        quantity: int,
        uow: unitofwork.AbstractUnitOfWork
) -> Order:
    with uow:
        restaurant = uow.repository.get(restaurant_id)
        if restaurant is None:
            raise InvalidRestaurantUUID('Invalid restaurant UUID.')

        order = restaurant.make_order(order_mapping, quantity)
        uow.commit()

    return order
