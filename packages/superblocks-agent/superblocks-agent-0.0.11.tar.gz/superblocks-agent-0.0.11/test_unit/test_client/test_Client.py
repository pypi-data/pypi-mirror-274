import asyncio
import unittest

import grpc
from superblocks_types.api.v1.service_pb2_grpc import ExecutorServiceStub

from superblocks_agent.client import Client, Config


class TestClient(unittest.TestCase):
    def test_init(self):
        Client(Config(endpoint="", token=""))

    def test_bad_connection_info(self):
        client = Client(Config(endpoint="", token=""))
        with self.assertRaises(Exception) as context:
            asyncio.run(
                client._run(
                    with_stub=ExecutorServiceStub,
                    stub_func_name="TwoWayStream",
                    initial_request={},
                    response_handler=lambda _: True,
                )
            )
        self.assertIsInstance(context.exception, grpc._channel._MultiThreadedRendezvous)
