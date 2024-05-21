from __future__ import annotations

from dataclasses import dataclass

from superblocks_agent.model.Agent import Agent
from superblocks_agent.model.Auth import Auth


@dataclass(kw_only=True)
class ClientConfig:
    agent: Agent
    # The authentication configuration.
    auth: Auth
