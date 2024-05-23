from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class Config:
    # The endpoint of the execution engine
    endpoint: str
    token: str
