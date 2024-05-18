import unittest

from superblocks_types.api.v1.event_pb2 import Event
from superblocks_types.api.v1.service_pb2 import (
    ExecuteRequest,
    Function,
    Mock,
    StreamResponse,
    TwoWayRequest,
    TwoWayResponse,
)
from superblocks_types.common.v1.common_pb2 import Profile
from superblocks_types.common.v1.errors_pb2 import Error

from superblocks_agent.enumeration.ViewMode import ViewMode
from superblocks_agent.model.ApiConfig import ApiConfig
from superblocks_agent.model.MockApiFilters import MockApiFilters
from superblocks_agent.things.Api import Api
from superblocks_agent.things.ApiMock import ApiMock
from superblocks_agent.util.convert import Mock_, to_protobuf_value
from superblocks_agent.util.generate import get_unique_id_for_object


class TestApi(unittest.TestCase):
    def test_build_execute_request(self):
        api = Api(
            "api_id",
            config=ApiConfig(
                application_id="app_id",
                branch_name="branch_name",
                commit_id="commit_id",
                profile_name="profile_name",
                page_id="page_id",
                view_mode=ViewMode.DEPLOYED,
            ),
        )
        api_mock = ApiMock(
            filters=MockApiFilters(
                integration_type="integration_type", step_name="step_name", inputs={"foo": "bar"}
            ),
            when=lambda _: True,
            return_val_or_callable={"some": "return"},
        )
        actual = api.build_execute_request(
            inputs={
                "str_var": "foo",
                "int_var": 1,
                "bool_var": True,
                "list_var": ["foo", 1, True, {}, []],
                "dict_var": {"foo": "bar"},
                "null_var": None,
            },
            mocks=[api_mock],
        )

        expected = ExecuteRequest(
            inputs={
                "str_var": to_protobuf_value("foo"),
                "int_var": to_protobuf_value(1),
                "bool_var": to_protobuf_value(True),
                "list_var": to_protobuf_value(["foo", 1, True, {}, []]),
                "dict_var": to_protobuf_value({"foo": "bar"}),
                "null_var": to_protobuf_value(None),
            },
            options=ExecuteRequest.Options(
                mocks=[
                    Mock_(
                        on=Mock.On(
                            static=Mock.Params(
                                integration_type="integration_type",
                                step_name="step_name",
                                inputs=to_protobuf_value({"foo": "bar"}),
                            ),
                            dynamic=get_unique_id_for_object(api_mock.on_callable),
                        ),
                        return_=Mock.Return(static=to_protobuf_value({"some": "return"})),
                    )
                ],
                include_event_outputs=True,
            ),
            fetch=ExecuteRequest.Fetch(
                id="api_id",
                profile=Profile(name="profile_name"),
                view_mode=ViewMode.DEPLOYED.to_proto_view_mode(),
                commit_id="commit_id",
                branch_name="branch_name",
            ),
        )

        self.assertEqual(expected, actual)

    def test_handle_two_way_response_invalid_type(self):
        api = Api("api_id")
        func = api.get_handle_two_way_response_func()

        with self.assertRaises(Exception) as context:
            func(TwoWayResponse())
        self.assertEqual(
            "got unexpected type: <class 'api.v1.service_pb2.TwoWayResponse'>",
            str(context.exception),
        )

    def test_handle_two_way_response_stream_type(self):
        api = Api("api_id")
        func = api.get_handle_two_way_response_func()

        stream_response = TwoWayResponse(
            stream=StreamResponse(
                execution="execution",
                event=Event(data=Event.Data(value=to_protobuf_value("some data"))),
            )
        )
        actual = func(stream_response)
        self.assertEqual(2, len(actual))
        self.assertIsNone(actual[0])
        self.assertEqual(stream_response, actual[1])

    def test_handle_two_way_response_function_type_function_call_succeeds(self):
        api = Api("api_id")
        func = api.get_handle_two_way_response_func()

        # have to set up function map first
        def return_func(filters: MockApiFilters) -> dict:
            return {"given_params": filters}

        api_mock = ApiMock(return_val_or_callable=return_func)

        api.hydrate_mock_func_lookup([api_mock])

        function_response = TwoWayResponse(
            function=Function.Request(
                name=get_unique_id_for_object(api_mock.return_val_or_callable),
                parameters=[to_protobuf_value({"foo": "bar"})],
                id="some_id",
            )
        )
        actual = func(function_response)
        self.assertEqual(2, len(actual))
        self.assertIsNone(actual[1])
        self.assertEqual(
            TwoWayRequest(
                function=Function.Response(
                    value=to_protobuf_value({"given_params": {"foo": "bar"}}), id="some_id"
                )
            ),
            actual[0],
        )

    def test_handle_two_way_response_function_type_function_call_fails(self):
        api = Api("api_id")
        func = api.get_handle_two_way_response_func()

        # have to set up function map first
        def return_func(_: MockApiFilters) -> dict:
            raise Exception("expected test error")

        api_mock = ApiMock(return_val_or_callable=return_func)

        api.hydrate_mock_func_lookup([api_mock])

        function_response = TwoWayResponse(
            function=Function.Request(
                name=get_unique_id_for_object(api_mock.return_val_or_callable),
                parameters=[to_protobuf_value({"foo": "bar"})],
                id="some_id",
            )
        )
        actual = func(function_response)
        self.assertEqual(2, len(actual))
        self.assertIsNone(actual[1])
        self.assertEqual(
            TwoWayRequest(
                function=Function.Response(error=Error(message="expected test error"), id="some_id")
            ),
            actual[0],
        )

    def test_hydrate_mock_func_lookup_no_mocks_given(self):
        api = Api("api_id")
        api.hydrate_mock_func_lookup([])
        self.assertEqual({}, api.mock_func_lookup)

    def test_hydrate_mock_func_lookup_only_mocks_with_dict_value_given(self):
        api = Api("api_id")
        mock_1 = ApiMock(return_val_or_callable={"foo": "bar"})
        api.hydrate_mock_func_lookup([mock_1])
        self.assertEqual({}, api.mock_func_lookup)

    def test_hydrate_mock_func_lookup_only_mocks_with_func_value_given(self):
        api = Api("api_id")
        mock_1_func = lambda x: x
        mock_1 = ApiMock(return_val_or_callable=mock_1_func)
        api.hydrate_mock_func_lookup([mock_1])
        self.assertEqual(
            {get_unique_id_for_object(mock_1.return_val_or_callable): mock_1_func},
            api.mock_func_lookup,
        )

    def test_hydrate_mock_func_lookup_mocks_with_func_value_and_mocks_with_dict_value_given(self):
        api = Api("api_id")
        mock_1_func = lambda x: x
        mock_1 = ApiMock(return_val_or_callable=mock_1_func)
        mock_2 = ApiMock(return_val_or_callable={"foo": "bar"})
        api.hydrate_mock_func_lookup([mock_1, mock_2])
        self.assertEqual(
            {get_unique_id_for_object(mock_1.return_val_or_callable): mock_1_func},
            api.mock_func_lookup,
        )

    def test_handle_two_way_response__function_to_execute_not_found(self):
        api = Api("api_id")

        func = api.get_handle_two_way_response_func()

        with self.assertRaises(Exception) as context:
            func(
                TwoWayResponse(
                    function=Function.Request(id="some_id", name="im_not_found", parameters=[])
                )
            )
        self.assertEqual("FOUND NO FUNCTION TO EXECUTE!", str(context.exception))
