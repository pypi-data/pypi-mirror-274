from dataclasses import dataclass
from typing import Optional

from superblocks_agent.model.ExecutionError import ExecutionError


@dataclass(kw_only=True)
class ApiResult:
    output: Optional[dict] = None
    error: Optional[ExecutionError] = None
