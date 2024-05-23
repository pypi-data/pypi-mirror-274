from dataclasses import dataclass
from typing import Optional

from superblocks_agent.api import ExecutionError


@dataclass(kw_only=True)
class Result:
    step_name: str
    output: Optional[dict] = None
    error: Optional[ExecutionError.ExecutionError] = None
