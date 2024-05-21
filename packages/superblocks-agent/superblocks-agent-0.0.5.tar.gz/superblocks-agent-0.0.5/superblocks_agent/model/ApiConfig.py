from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from superblocks_agent.enumeration.ViewMode import ViewMode


@dataclass(kw_only=True, eq=False)
class ApiConfig:
    # The application id used to provide a default scope.
    application_id: Optional[str] = None
    # The default branch to use.
    branch_name: Optional[str] = None
    # The id of the commit to use.
    commit_id: Optional[str] = None
    # The default profile to use. If not set, the default for view_mode will be used.
    profile_name: Optional[str] = None
    # The page id used to provide a default scope.
    page_id: Optional[str] = None
    # The default view mode.
    view_mode: Optional[ViewMode] = None
