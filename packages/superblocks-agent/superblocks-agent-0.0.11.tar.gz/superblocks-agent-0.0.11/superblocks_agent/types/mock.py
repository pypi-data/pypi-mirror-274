from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Union

from superblocks_agent.testing import Params

JsonValue = Union[str, float, int, bool, None, "JsonObject", "JsonArray"]
JsonObject = dict[str, JsonValue]
JsonArray = list[JsonValue]

# when {these params}
WhenCallable = Callable[[Params], bool]

# when {these params} return {this value}
MockCallable = Callable[[Params], JsonValue]


class BaseMock(ABC):
    @abstractmethod
    def return_(value: dict | MockCallable) -> BaseMock:
        """
        A helper function that should be implemented by Mock classes.
        This function returns an updated version of the Mock.

        i.e. my_updated_mock = my_mock.return_({"foo": "bar"})
        """
        ...
