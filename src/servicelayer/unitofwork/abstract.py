from abc import ABC, abstractmethod

from domain.base.repository import AbstractRepository


class AbstractUnitOfWork(ABC):
    repository: AbstractRepository

    def __enter__(self) -> 'AbstractUnitOfWork':
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.rollback()

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass
