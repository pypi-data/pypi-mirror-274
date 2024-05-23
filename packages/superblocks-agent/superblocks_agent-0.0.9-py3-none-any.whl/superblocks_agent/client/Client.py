import queue

import grpc
from superblocks_types.api.v1.service_pb2 import StreamResponse

from superblocks_agent._type.client import TwoWayStreamResponseHandler
from superblocks_agent.client import Config


class Client:
    def __init__(self, config: Config):
        self.config = config

    async def _run(
        self,
        *,
        with_stub: object,
        stub_func_name: str,
        initial_request: object,
        response_handler: TwoWayStreamResponseHandler,
    ) -> list[StreamResponse]:
        # TODO: (joey) throw clear errors here for auth/connection issues
        stub = with_stub(channel=grpc.insecure_channel(target=self.config.endpoint))
        stub_function = getattr(stub, stub_func_name)

        stream_responses = []
        q = queue.Queue()

        q.put(initial_request)

        def get_requests():
            while True:
                yield q.get()

        try:
            responses = stub_function(get_requests())

            for response in responses:
                next_request, two_way_response = response_handler(response)
                if two_way_response is not None:
                    stream_responses.append(two_way_response.stream)
                if next_request is not None:
                    q.put(next_request)
        except Exception as e:
            print("ERROR WHILE GETTING RESPONSES", e)
            raise e

        return stream_responses
