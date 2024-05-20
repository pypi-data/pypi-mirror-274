from .base import DataType, FieldType, fieldtype


@fieldtype
class IntegerType(FieldType[int]):
    raw_type = 0xA0
    data_type = int

    def to_bytes(self, data: DataType) -> bytes:
        if not isinstance(data, int):
            raise TypeError("data should be instance of int")
        return data.to_bytes((data.bit_length() + 7) // 8, signed=True)
    
    def from_bytes(self, data: bytes) -> DataType:
        if not isinstance(data, bytes):
            raise TypeError("data should be instance of bytes")
        return int.from_bytes(data, signed=True)