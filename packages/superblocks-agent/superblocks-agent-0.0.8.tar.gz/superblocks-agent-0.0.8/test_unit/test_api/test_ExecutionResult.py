import unittest

from superblocks_types.api.v1.event_pb2 import BlockStatus, Event, Output
from superblocks_types.api.v1.service_pb2 import StreamResponse
from superblocks_types.common.v1.errors_pb2 import Error

from superblocks_agent._util.convert import to_protobuf_value
from superblocks_agent.api import ExecutionError, ExecutionResult
from superblocks_agent.api import Result as ApiResult
from superblocks_agent.step import Result as StepResult


class TestExecutionResult(unittest.TestCase):
    def test_from_proto_stream_responses__empty_list(self):
        actual = ExecutionResult.from_proto_stream_responses([])
        self.assertEqual(ExecutionResult(step_results=[], api_result=ApiResult()), actual)

        self.assertEqual(ApiResult(), actual.api_result)

    def test_from_proto_stream_responses__with_error(self):
        actual = ExecutionResult.from_proto_stream_responses(
            [
                StreamResponse(
                    event=Event(
                        name="event_name",
                        end=Event.End(
                            error=Error(name="name", message="message", block_path="block_path"),
                            status=BlockStatus.BLOCK_STATUS_ERRORED,
                        ),
                    )
                )
            ]
        )
        expected = ExecutionResult(
            step_results=[
                StepResult(
                    step_name="event_name",
                    error=ExecutionError(name="name", message="message", block_path="block_path"),
                )
            ],
            api_result=ApiResult(
                error=ExecutionError(name="name", message="message", block_path="block_path")
            ),
        )
        self.assertEqual(expected, actual)

    def test_from_proto_stream_responses__without_error(self):
        actual = ExecutionResult.from_proto_stream_responses(
            [
                StreamResponse(
                    event=Event(
                        name="event_name",
                        end=Event.End(
                            output=Output(result=to_protobuf_value({"foo": "bar"})),
                            is_response_block=True,
                        ),
                    )
                )
            ]
        )
        # expected = ExecutionResult(
        #     step_results=[StepResult(step_name="event_name", output={"foo": "bar"})],
        #     api_result=ApiResult(output={"foo": "bar"}),
        # )
        # self.assertEqual(expected, actual)
