from .base import DataType, FieldType, fieldtype


@fieldtype
class StringType(FieldType[str]):
    raw_type = 0xA1
    data_type = str

    def to_bytes(self, data: DataType) -> bytes:
        if not isinstance(data, str):
            raise TypeError("data should be instance of str")
        return data.encode()
    
    def from_bytes(self, data: bytes) -> DataType:
        if not isinstance(data, bytes):
            raise TypeError("data should be instance of bytes")
        return data.decode()