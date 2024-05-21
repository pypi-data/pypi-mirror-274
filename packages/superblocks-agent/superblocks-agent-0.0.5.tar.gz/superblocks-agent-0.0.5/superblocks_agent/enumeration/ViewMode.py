from __future__ import annotations

from superblocks_types.api.v1.service_pb2 import ViewMode as ViewModeProto

from superblocks_agent.enumeration.BaseEnum import BaseEnum


class ViewMode(BaseEnum):
    DEPLOYED = "deployed"
    EDITOR = "editor"
    PREVIEW = "preview"

    @classmethod
    def items(cls) -> list[tuple[ViewMode, str]]:
        return [(member, name) for name, member in cls.__members__.items()]

    @classmethod
    def from_str(cls, s: str) -> ViewMode:
        s_upper = s.upper()
        for member in cls:
            if member.name == s_upper:
                return member
        raise ValueError(f"'{s}' is not a valid {cls.__name__}")

    def to_proto_view_mode(self) -> ViewModeProto:
        match self:
            case ViewMode.DEPLOYED:
                return ViewModeProto.VIEW_MODE_DEPLOYED
            case ViewMode.EDITOR:
                return ViewModeProto.VIEW_MODE_EDIT
            case ViewMode.PREVIEW:
                return ViewModeProto.VIEW_MODE_PREVIEW
        return ViewModeProto.VIEW_MODE_UNSPECIFIED
