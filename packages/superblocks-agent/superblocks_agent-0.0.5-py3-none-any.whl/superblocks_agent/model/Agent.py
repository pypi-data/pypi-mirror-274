from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True, eq=False)
class Agent:
    # The endpoint of the execution engine
    endpoint: str
