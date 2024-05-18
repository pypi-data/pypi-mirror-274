from __future__ import annotations

from dataclasses import dataclass, field

from superblocks_types.api.v1.event_pb2 import BlockStatus
from superblocks_types.api.v1.service_pb2 import StreamResponse

from superblocks_agent.model.ApiResult import ApiResult
from superblocks_agent.model.ExecutionError import ExecutionError
from superblocks_agent.model.StepResult import StepResult
from superblocks_agent.util.convert import from_protobuf_value


@dataclass(kw_only=True)
class ExecutionResult:
    step_results: list[StepResult] = field(default_factory=list)
    api_result: ApiResult = field(default_factory=ApiResult)

    @staticmethod
    def from_proto_stream_responses(stream_responses: list[StreamResponse]) -> ExecutionResult:
        step_results = []
        api_output = None
        api_error = None
        for stream_response in stream_responses:
            # check if this is an "end" event
            # "end" events are step results
            if stream_response.event.HasField("end"):
                step_output = from_protobuf_value(stream_response.event.end.output.result)
                step_error = None
                if stream_response.event.end.is_response_block:
                    api_output = from_protobuf_value(stream_response.event.end.output.result)
                if stream_response.event.end.status == BlockStatus.BLOCK_STATUS_ERRORED:
                    api_error = step_error = ExecutionError.from_proto_error(
                        stream_response.event.end.error
                    )
                step_results.append(
                    StepResult(
                        step_name=stream_response.event.name, output=step_output, error=step_error
                    )
                )
        api_result = ApiResult(output=api_output, error=api_error)
        return ExecutionResult(step_results=step_results, api_result=api_result)
