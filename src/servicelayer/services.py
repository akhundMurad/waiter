import decimal
import uuid
from uuid import UUID

from domain.restaurant import dto
from domain.restaurant.exceptions import InvalidRestaurantUUID, \
    WrongTableForRestaurant
from domain.restaurant.models import Price
from servicelayer.unitofwork.interface import UnitOfWorkInterface


def add_table_to_restaurant(
        restaurant_id: UUID,
        uow: UnitOfWorkInterface
) -> dto.TableRead:
    with uow:
        restaurant = uow.repository.get(restaurant_id)
        if restaurant is None:
            raise InvalidRestaurantUUID('Invalid restaurant UUID.')
        table = restaurant.add_table()
        table = dto.TableRead(
            index=table.index
        )
        uow.commit()

    return table


def create_menu_item_to_restaurant(
        restaurant_id: UUID,
        title: str,
        description: str,
        price: float,
        uow: UnitOfWorkInterface
) -> dto.MenuItemRead:
    with uow:
        restaurant = uow.repository.get(restaurant_id)
        if restaurant is None:
            raise InvalidRestaurantUUID('Invalid restaurant UUID.')
        price_as_vo = Price(value=decimal.Decimal(price))
        menu_item = restaurant.create_menu_item(
            title=title, description=description, price=price_as_vo
        )
        menu_item = dto.MenuItemRead(
            id=str(menu_item.id),
            title=menu_item.title,
            description=menu_item.description,
            price=float(menu_item.price.value)
        )
        uow.commit()

    return menu_item


def make_order(
        restaurant_id: UUID,
        order_mapping: list[dict],
        table: int,
        uow: UnitOfWorkInterface
) -> dto.OrderRead:
    with uow:
        restaurant = uow.repository.get(restaurant_id)
        if restaurant is None:
            raise InvalidRestaurantUUID('Invalid restaurant UUID.')

        table = restaurant.get_table_by_index(table)
        if table is None:
            raise WrongTableForRestaurant('Invalid table for restaurant.')

        new_order_mapping = list()
        for order_mapping in order_mapping:
            new_order_mapping.append({
                'menu_item': uuid.UUID(order_mapping['menu_item']),
                'quantity': order_mapping['quantity']
            })

        order = restaurant.make_order(
            order_mapping=new_order_mapping,
            table=table,
        )
        order = dto.OrderRead(
            id=str(order.id),
            table=order.table.index,
            total_price=float(order.total_price.value)
        )
        uow.commit()

    return order
