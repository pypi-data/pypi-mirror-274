from dataclasses import dataclass
from typing import Optional

from superblocks_agent.model.ExecutionError import ExecutionError


@dataclass(kw_only=True)
class StepResult:
    step_name: str
    output: Optional[dict] = None
    error: Optional[ExecutionError] = None
