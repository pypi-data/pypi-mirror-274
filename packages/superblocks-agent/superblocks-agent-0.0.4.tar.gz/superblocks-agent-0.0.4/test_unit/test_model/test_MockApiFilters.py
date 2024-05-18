import unittest

from superblocks_types.api.v1.service_pb2 import Mock

from superblocks_agent.model.MockApiFilters import MockApiFilters
from superblocks_agent.util.convert import to_protobuf_value


class TestMockApiFilters(unittest.TestCase):
    def test_to_proto_params(self):
        self.assertEqual(Mock.Params(), MockApiFilters().to_proto_params())
        self.assertEqual(
            Mock.Params(
                integration_type="integration_type",
                step_name="step_name",
                inputs=to_protobuf_value({"foo": "bar"}),
            ),
            MockApiFilters(
                integration_type="integration_type", step_name="step_name", inputs={"foo": "bar"}
            ).to_proto_params(),
        )
