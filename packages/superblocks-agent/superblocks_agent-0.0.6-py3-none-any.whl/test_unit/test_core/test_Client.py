import asyncio
import unittest

import grpc
from superblocks_types.api.v1.service_pb2_grpc import ExecutorServiceStub

from superblocks_agent.core import Client
from superblocks_agent.model import Agent, Auth, ClientConfig


class TestClient(unittest.TestCase):
    def test_init(self):
        Client(ClientConfig(agent=Agent(endpoint=""), auth=Auth(token="")))

    def test_bad_connection_info(self):
        client = Client(ClientConfig(agent=Agent(endpoint=""), auth=Auth(token="")))
        with self.assertRaises(Exception) as context:
            asyncio.run(
                client.run(
                    with_stub=ExecutorServiceStub,
                    stub_func_name="TwoWayStream",
                    initial_request={},
                    response_handler=lambda _: True,
                )
            )
        self.assertIsInstance(context.exception, grpc._channel._MultiThreadedRendezvous)
