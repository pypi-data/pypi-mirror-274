from typing import Callable

from .MockFilters import MockFilters

# when {these filters}
WhenCallable = Callable[[MockFilters], bool]

# when {these filters} return {this value}
FilteredDictCallable = Callable[[MockFilters], dict]
