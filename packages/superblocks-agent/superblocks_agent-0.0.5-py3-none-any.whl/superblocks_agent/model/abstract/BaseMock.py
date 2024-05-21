from __future__ import annotations

from abc import ABC, abstractmethod

from superblocks_agent.type_.mock import FilteredDictCallable


class BaseMock(ABC):
    @abstractmethod
    def return_(value: dict | FilteredDictCallable) -> BaseMock:
        """
        A helper function that should be implemented by Mock classes.
        This function returns an updated version of the Mock.

        i.e. my_updated_mock = my_mock.return_({"foo": "bar"})
        """
        ...
