from typing import Optional

import grpc
from superblocks_types.api.v1.service_pb2 import StreamResponse

from superblocks_agent.model.ClientConfig import ClientConfig
from superblocks_agent.type_.client import GenericMetadata, TwoWayStreamResponseHandler


class Client:
    def __init__(self, client_config: ClientConfig):
        self.__client_config = client_config

    async def run(
        self,
        *,
        with_stub: object,
        stub_func_name: str,
        initial_requests: list[object],
        response_handler: TwoWayStreamResponseHandler,
    ) -> list[StreamResponse]:
        stub = with_stub(channel=grpc.insecure_channel(target=self.__client_config.agent.endpoint))
        stub_function = getattr(stub, stub_func_name)

        return self.__handle_two_way_stream(
            stub_function=stub_function,
            requests=initial_requests,
            response_handler=response_handler,
        )

    def __handle_two_way_stream(
        self,
        *,
        stub_function: callable,
        requests: list[object],
        response_handler: TwoWayStreamResponseHandler,
        stream_responses: Optional[list[GenericMetadata]] = None,
    ) -> list[StreamResponse]:
        stream_responses = [] if stream_responses is None else stream_responses
        try:
            for response in stub_function(iter(requests)):
                next_request, two_way_response = response_handler(response)
                if two_way_response is not None:
                    stream_responses.append(two_way_response.stream)
                if next_request is not None:
                    # recursively call
                    self.__handle_two_way_stream(
                        stub_function=stub_function,
                        requests=[next_request],
                        response_handler=response_handler,
                        stream_responses=stream_responses,
                    )
        except Exception as e:
            print("Error processing responses:", e)
            raise e

        return stream_responses
