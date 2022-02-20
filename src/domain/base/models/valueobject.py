import typing
from dataclasses import dataclass


def valueobject(cls):
    def __post_init__(self):
        validation_methods = self._get_validation_methods()
        for method in validation_methods:
            method()

    def _get_validation_methods(self) -> list[typing.Callable]:
        methods: list[typing.Callable] = list()
        for method in dir(self):
            if method.split('_')[0] == 'validate':
                methods.append(getattr(self, method))

        return methods

    setattr(cls, '__post_init__', __post_init__)
    setattr(cls, '_get_validation_methods', _get_validation_methods)

    return dataclass(
        cls, init=True, repr=True, order=True, eq=True, unsafe_hash=True
    )
