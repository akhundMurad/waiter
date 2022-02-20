from domain.base.exceptions import DomainException


class InvalidRestaurantUUID(DomainException):
    pass


class PriceValueIsLessThanZero(DomainException):
    pass


class TableIndexIsLessThanZero(DomainException):
    pass


class WrongMenuItemForRestaurant(DomainException):
    pass


class WrongTableForRestaurant(DomainException):
    pass
