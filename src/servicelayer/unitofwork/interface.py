import typing

from domain.base.interface.repository import RepositoryInterface


TUnitOfWorkInterface = typing.TypeVar(
    'TUnitOfWorkInterface', bound='UnitOfWorkInterface'
)


class UnitOfWorkInterface(typing.Protocol):
    repository: RepositoryInterface

    def __enter__(self) -> TUnitOfWorkInterface:
        ...

    def __exit__(self, *args, **kwargs) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...
