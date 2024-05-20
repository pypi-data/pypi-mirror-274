from .int import IntegerType
from .base import DataType, fieldtype


@fieldtype
class BooleanType(IntegerType):
    raw_type = 0xA2
    data_type = bool

    def to_bytes(self, data: DataType) -> bytes:
        if not isinstance(data, bool):
            raise TypeError("data should be instance of bool")
        return data.to_bytes()