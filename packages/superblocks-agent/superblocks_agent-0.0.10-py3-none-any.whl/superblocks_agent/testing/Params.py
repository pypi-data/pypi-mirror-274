from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from superblocks_types.api.v1.service_pb2 import Mock

from superblocks_agent._util.convert import to_protobuf_value


@dataclass(kw_only=True)
class Params:
    # Filter on integrations with this type
    integration_type: Optional[str] = None
    # Filter on steps with this name
    # NOTE: steps are unique on name
    step_name: Optional[str] = None
    # Filter on these inputs
    configuration: Optional[dict] = None

    def to_proto_params(self) -> Mock.Params:
        params = Mock.Params()
        if self.integration_type is not None:
            params.integration_type = self.integration_type
        if self.step_name is not None:
            params.step_name = self.step_name
        if self.configuration is not None:
            params.inputs.CopyFrom(to_protobuf_value(self.configuration))
        return params
