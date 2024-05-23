from __future__ import annotations

from dataclasses import dataclass

from superblocks_agent._constant import DEFAULT_AGENT_ENDPOINT


@dataclass(kw_only=True)
class Config:
    # The endpoint of the execution engine
    endpoint: str = DEFAULT_AGENT_ENDPOINT
    token: str
