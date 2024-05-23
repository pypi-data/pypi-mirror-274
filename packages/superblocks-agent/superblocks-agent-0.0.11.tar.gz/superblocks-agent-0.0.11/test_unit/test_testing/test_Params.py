import unittest

from superblocks_types.api.v1.service_pb2 import Mock

from superblocks_agent._util.convert import to_protobuf_value
from superblocks_agent.testing import Params


class TestParams(unittest.TestCase):
    def test_to_proto_params(self):
        self.assertEqual(Mock.Params(), Params().to_proto_params())
        self.assertEqual(
            Mock.Params(
                integration_type="integration_type",
                step_name="step_name",
                inputs=to_protobuf_value({"foo": "bar"}),
            ),
            Params(
                integration_type="integration_type",
                step_name="step_name",
                configuration={"foo": "bar"},
            ).to_proto_params(),
        )
