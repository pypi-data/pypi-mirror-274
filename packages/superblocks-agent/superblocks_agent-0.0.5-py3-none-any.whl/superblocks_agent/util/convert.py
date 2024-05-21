from typing import Optional

from google.protobuf.struct_pb2 import ListValue, Struct, Value
from superblocks_types.api.v1.service_pb2 import Mock


# NOTE: (joey) theres likely some existing automatic way to do this but for now this works
def to_protobuf_value(data: Optional[bool | int | float | str | dict | list]) -> Value:
    """Returns the protobuf value of the given native Python value."""
    value = Value()
    match data:
        case None:
            value.null_value = 0  # NullValue enum
        case True | False:
            value.bool_value = data
        case _ if isinstance(data, int) | isinstance(data, float):
            value.number_value = data
        case _ if isinstance(data, str):
            value.string_value = data
        case _ if isinstance(data, dict):
            struct_value = Struct()
            for key, item in data.items():
                struct_value.fields[key].CopyFrom(to_protobuf_value(item))
            value.struct_value.CopyFrom(struct_value)
        case _ if isinstance(data, list):
            list_value = ListValue()
            list_value.values.extend(to_protobuf_value(item) for item in data)
            value.list_value.CopyFrom(list_value)
        case _:
            raise TypeError(f"Unsupported type: {type(data)}")
    return value


def from_protobuf_value(proto_value: Value) -> Optional[int | float | str | bool | dict | list]:
    """Extracts native Python value from the given protobuf Value."""
    kind = proto_value.WhichOneof("kind")
    match kind:
        # NOTE: (joey) i think both of these are needed for None
        case "null_value" | None:
            return None
        case "number_value":
            return proto_value.number_value
        case "string_value":
            return proto_value.string_value
        case "bool_value":
            return proto_value.bool_value
        case "struct_value":
            return {k: from_protobuf_value(v) for k, v in proto_value.struct_value.fields.items()}
        case "list_value":
            return [from_protobuf_value(item) for item in proto_value.list_value.values]
        case _:
            raise ValueError(f"Unknown type of value: {kind}")


# some protos use reserved keywords (like 'return')
# to keep the simplicity of using the constructor, we can mimic the constructors here
# NOTE: (joey) there's probably a better pattern for this, something to think about


def Mock_(*, on: Optional[Mock.On] = None, return_: Optional[Mock.Return] = None) -> Mock:
    mock = Mock()
    if on is not None:
        mock.on.CopyFrom(on)
    if return_ is not None:
        # NOTE: return is a reserved keyword, this workaround seems to do the trick
        # source: https://stackoverflow.com/questions/30142750/reserved-keyword-is-used-in-protobuf-in-python
        return_value = getattr(mock, "return")
        return_value.CopyFrom(return_)
    return mock
