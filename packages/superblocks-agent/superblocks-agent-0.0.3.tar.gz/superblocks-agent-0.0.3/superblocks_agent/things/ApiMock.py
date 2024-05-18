from __future__ import annotations

from typing import Optional

from superblocks_types.api.v1.service_pb2 import Mock

from superblocks_agent.model.abstract.BaseMock import BaseMock
from superblocks_agent.model.MockApiFilters import MockApiFilters
from superblocks_agent.type_.mock import FilteredDictCallable, WhenCallable
from superblocks_agent.util.convert import Mock_, to_protobuf_value
from superblocks_agent.util.generate import get_unique_id_for_object


class ApiMock(BaseMock):
    def __init__(
        self,
        filters: Optional[MockApiFilters] = None,
        *,
        when: Optional[WhenCallable] = None,
        # this can be set (more clearly) by calling .return_()
        return_val_or_callable: Optional[dict | FilteredDictCallable] = None,
    ):
        self.on_filters = filters
        # these are public because they are accessed by Api.py
        self.on_callable = when
        self.return_val_or_callable = return_val_or_callable

    def return_(self, value: dict | FilteredDictCallable) -> ApiMock:
        self.return_val_or_callable = value
        return self

    def to_proto_on(self) -> Optional[Mock.On]:
        mock_on = None
        if self.on_filters is not None:
            mock_on = Mock.On() if mock_on is None else mock_on
            mock_on.static.CopyFrom(self.on_filters.to_proto_params())
        if self.on_callable is not None:
            mock_on = Mock.On() if mock_on is None else mock_on
            mock_on.dynamic = get_unique_id_for_object(self.on_callable)
        return mock_on

    def to_proto_return(self) -> Optional[Mock.Return]:
        mock_return = None
        if self.return_val_or_callable is not None:
            mock_return = Mock.Return()
            match self.return_val_or_callable:
                case _ if isinstance(self.return_val_or_callable, dict):
                    mock_return.static.CopyFrom(to_protobuf_value(self.return_val_or_callable))
                # should be type type_.mock.WhenCallable
                case _ if callable(self.return_val_or_callable):
                    mock_return.dynamic = get_unique_id_for_object(self.return_val_or_callable)
        return mock_return

    def to_proto_mock(self) -> Mock:
        return Mock_(on=self.to_proto_on(), return_=self.to_proto_return())


def on(filters: Optional[MockApiFilters] = None, *, when: Optional[WhenCallable] = None) -> ApiMock:
    return ApiMock(filters=filters, when=when)
