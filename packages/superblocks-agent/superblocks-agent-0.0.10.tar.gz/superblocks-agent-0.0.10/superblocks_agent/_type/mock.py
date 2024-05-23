from __future__ import annotations

from typing import Callable, Union

from superblocks_agent.testing import Params

JSONValue = Union[str, float, int, bool, None, "JSONObject", "JSONArray"]
JSONObject = dict[str, JSONValue]
JSONArray = list[JSONValue]

# when {these params}
WhenCallable = Callable[[Params], bool]

# when {these params} return {this value}
MockCallable = Callable[[Params], JSONValue]
