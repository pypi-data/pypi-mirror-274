# TODO: (joey) some of these imports are weird

from dataclasses import dataclass
from typing import Optional

from superblocks_agent.api.ExecutionError import ExecutionError


@dataclass(kw_only=True)
class Result:
    output: Optional[dict] = None
    error: Optional[ExecutionError] = None
