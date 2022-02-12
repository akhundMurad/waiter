from abc import ABC, abstractmethod

from domain import repository


class AbstractUnitOfWork(ABC):
    repository: repository.AbstractRepository

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
