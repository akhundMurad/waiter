from abc import ABC, abstractmethod

from domain import repository


class AbstractUnitOfWork(ABC):
    restaurant_repository: repository.AbstractRepository

