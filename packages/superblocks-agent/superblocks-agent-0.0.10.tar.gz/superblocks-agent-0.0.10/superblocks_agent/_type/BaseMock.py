from __future__ import annotations

from abc import ABC, abstractmethod

from .mock import MockCallable


class BaseMock(ABC):
    @abstractmethod
    def return_(value: dict | MockCallable) -> BaseMock:
        """
        A helper function that should be implemented by Mock classes.
        This function returns an updated version of the Mock.

        i.e. my_updated_mock = my_mock.return_({"foo": "bar"})
        """
        ...
