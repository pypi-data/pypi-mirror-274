from dataclasses import dataclass
from typing import Optional

from superblocks_agent.model import ExecutionError


@dataclass(kw_only=True)
class ApiResult:
    output: Optional[dict] = None
    # TODO: (joey) figure out why its making me do "." here
    error: Optional[ExecutionError.ExecutionError] = None
