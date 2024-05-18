import unittest

from superblocks_types.api.v1.service_pb2 import Mock

from superblocks_agent.model.MockApiFilters import MockApiFilters
from superblocks_agent.things.ApiMock import ApiMock, on
from superblocks_agent.util.convert import Mock_, to_protobuf_value
from superblocks_agent.util.generate import get_unique_id_for_object


class TestApiMock(unittest.TestCase):
    def test_return_(self):
        # overwrites existing return val
        api_mock = ApiMock(return_val_or_callable="old")
        self.assertEqual("old", api_mock.return_val_or_callable)
        api_mock = api_mock.return_("new")
        self.assertEqual("new", api_mock.return_val_or_callable)

    def test_on__no_params(self):
        api_mock = on()
        self.assertIsNone(api_mock.on_callable)
        self.assertIsNone(api_mock.on_filters)
        self.assertIsNone(api_mock.return_val_or_callable)

    def test_on__only_filters_given(self):
        filters = MockApiFilters(
            integration_type="integration_type", step_name="step_name", inputs={"foo": "bar"}
        )
        api_mock = on(filters=filters)
        self.assertEqual(filters, api_mock.on_filters)
        self.assertIsNone(api_mock.on_callable)
        self.assertIsNone(api_mock.return_val_or_callable)

    def test_on__only_when_given(self):
        func = lambda _: True
        api_mock = on(when=func)
        self.assertEqual(func, api_mock.on_callable)
        self.assertIsNone(api_mock.on_filters)
        self.assertIsNone(api_mock.return_val_or_callable)

    def test_on__filters_and_when_given(self):
        func = lambda _: True
        filters = MockApiFilters(
            integration_type="integration_type", step_name="step_name", inputs={"foo": "bar"}
        )
        api_mock = on(when=func, filters=filters)
        self.assertEqual(func, api_mock.on_callable)
        self.assertEqual(filters, api_mock.on_filters)
        self.assertIsNone(api_mock.return_val_or_callable)

    def test_to_proto_on(self):
        self.assertIsNone(ApiMock().to_proto_on())

        func = lambda _: True
        api_mock = ApiMock(
            filters=MockApiFilters(
                integration_type="integration_type", step_name="step_name", inputs={"foo": "bar"}
            ),
            when=func,
        )
        self.assertEqual(
            Mock.On(
                static=Mock.Params(
                    integration_type="integration_type",
                    step_name="step_name",
                    inputs=to_protobuf_value({"foo": "bar"}),
                ),
                dynamic=get_unique_id_for_object(func),
            ),
            api_mock.to_proto_on(),
        )

    def test_to_proto_return(self):
        # None
        self.assertIsNone(ApiMock().to_proto_return())

        # static
        api_mock = ApiMock(return_val_or_callable={"foo": "bar"})
        self.assertEqual(
            Mock.Return(static=to_protobuf_value({"foo": "bar"})), api_mock.to_proto_return()
        )

        # dynamic
        func = lambda _: True
        api_mock = ApiMock(return_val_or_callable=func)
        self.assertEqual(
            Mock.Return(dynamic=get_unique_id_for_object(func)), api_mock.to_proto_return()
        )

    def test_to_proto_mock(self):
        when_func = lambda _: True
        return_func = lambda _: True
        api_mock = ApiMock(
            filters=MockApiFilters(
                integration_type="integration_type", step_name="step_name", inputs={"foo": "bar"}
            ),
            when=when_func,
            return_val_or_callable=return_func,
        )

        self.assertEqual(
            Mock_(
                on=Mock.On(
                    static=Mock.Params(
                        integration_type="integration_type",
                        step_name="step_name",
                        inputs=to_protobuf_value({"foo": "bar"}),
                    ),
                    dynamic=get_unique_id_for_object(when_func),
                ),
                return_=Mock.Return(dynamic=get_unique_id_for_object(return_func)),
            ),
            api_mock.to_proto_mock(),
        )
