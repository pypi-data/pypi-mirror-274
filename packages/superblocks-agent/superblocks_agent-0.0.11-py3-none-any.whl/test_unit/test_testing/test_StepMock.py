import unittest

from superblocks_types.api.v1.service_pb2 import Mock

from superblocks_agent._util.convert import Mock_, to_protobuf_value
from superblocks_agent._util.generate import get_unique_id_for_object
from superblocks_agent.testing import Params
from superblocks_agent.testing._StepMock import StepMock, on


class TestStepMock(unittest.TestCase):
    def test_return_(self):
        # overwrites existing return val
        api_mock = StepMock().return_({"old": "value"})
        self.assertEqual({"old": "value"}, api_mock.get_return_value())
        api_mock = api_mock.return_({"new": "value"})
        self.assertEqual({"new": "value"}, api_mock.get_return_value())

    def test_return__invalid_type_given(self):
        with self.assertRaises(ValueError) as context:
            StepMock().return_("im invalid")
        self.assertEqual("invalid type for return: '<class 'str'>'", str(context.exception))

    def test_on__no_params(self):
        api_mock = on()
        self.assertIsNone(api_mock.get_when_callable())
        self.assertIsNone(api_mock.get_return_value())

    def test_on__only_params_given(self):
        params = Params(
            integration_type="integration_type", step_name="step_name", configuration={"foo": "bar"}
        )
        api_mock = on(params=params)
        self.assertIsNone(api_mock.get_when_callable())
        self.assertIsNone(api_mock.get_return_value())

    def test_on__only_when_given(self):
        func = lambda _: True
        api_mock = on(when=func)
        self.assertEqual(func, api_mock.get_when_callable())
        self.assertIsNone(api_mock.get_return_value())

    def test_on__params_and_when_given(self):
        func = lambda _: True
        params = Params(
            integration_type="integration_type", step_name="step_name", configuration={"foo": "bar"}
        )
        api_mock = on(when=func, params=params)
        self.assertEqual(func, api_mock.get_when_callable())
        self.assertIsNone(api_mock.get_return_value())

    def test_to_proto_on(self):
        self.assertIsNone(StepMock().to_proto_on())

        func = lambda _: True
        api_mock = StepMock(
            params=Params(
                integration_type="integration_type",
                step_name="step_name",
                configuration={"foo": "bar"},
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
        self.assertIsNone(StepMock().to_proto_return())

        # static
        api_mock = StepMock().return_({"foo": "bar"})
        self.assertEqual(
            Mock.Return(static=to_protobuf_value({"foo": "bar"})), api_mock.to_proto_return()
        )

        # dynamic
        func = lambda _: True
        api_mock = StepMock().return_(func)
        self.assertEqual(
            Mock.Return(dynamic=get_unique_id_for_object(func)), api_mock.to_proto_return()
        )

    def test_to_proto_mock(self):
        when_func = lambda _: True
        return_func = lambda _: True
        api_mock = StepMock(
            params=Params(
                integration_type="integration_type",
                step_name="step_name",
                configuration={"foo": "bar"},
            ),
            when=when_func,
        ).return_(return_func)

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
