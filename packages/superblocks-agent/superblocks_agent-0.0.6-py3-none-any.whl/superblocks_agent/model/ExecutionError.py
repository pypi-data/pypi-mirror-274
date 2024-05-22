from __future__ import annotations

from dataclasses import dataclass

from superblocks_types.common.v1.errors_pb2 import Error


@dataclass(kw_only=True)
class ExecutionError:
    name: str
    message: str
    block_path: str

    @staticmethod
    def from_proto_error(error: Error) -> ExecutionError:
        return ExecutionError(name=error.name, message=error.message, block_path=error.block_path)
