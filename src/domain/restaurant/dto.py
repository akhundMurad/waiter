from domain.base.dto import DTO


class MenuItemWrite(DTO):
    title: str
    description: str
    price: float


class MenuItemRead(DTO):
    id: str
    title: str
    description: str
    price: float


class OrderMapping(DTO):
    menu_item: str
    quantity: int


class OrderWrite(DTO):
    table: int
    order_mapping: list[OrderMapping]
    restaurant_id: str


class OrderRead(DTO):
    id: str
    table: int
    total_price: float


class TableRead(DTO):
    index: int
