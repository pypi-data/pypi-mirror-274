from dataclasses import dataclass
from typing import Optional

from superblocks_agent.model import ExecutionError


@dataclass(kw_only=True)
class StepResult:
    step_name: str
    output: Optional[dict] = None
    error: Optional[ExecutionError] = None


@dataclass(kw_only=True)
class Foo:
    step_name: str
    output: Optional[dict] = None
    error: Optional[ExecutionError] = None
