# TODO: (joey) some of these imports are weird

from dataclasses import dataclass
from typing import Optional

from superblocks_agent.api.ViewMode import ViewMode


@dataclass(kw_only=True, eq=False)
class Config:
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
