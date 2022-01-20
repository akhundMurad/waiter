from pydantic import BaseModel


class MenuItemWrite(BaseModel):
    title: str
    description: str
    price: float


class MenuItemRead(MenuItemWrite):
    id: str


class OrderMapping(BaseModel):
    menu_item: str
    quantity: int


class OrderWrite(BaseModel):
    table: int
    order_mapping: list[OrderMapping]


class OrderRead(BaseModel):
    id: str
    table: int
    total_price: float
