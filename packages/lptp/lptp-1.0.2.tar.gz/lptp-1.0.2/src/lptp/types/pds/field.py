from typing import Any, Self
from lptp import exceptions
from .types import FieldType


class DataField:
    name: int
    type: FieldType
    data: Any

    def __init__(self, name: int, data: Any) -> None:
        if not isinstance(name, int):
            raise TypeError("name should be instance of int")
        if name > 0xFF or name < 0:
            raise ValueError("name should be within 0xFF")
        
        data_type = FieldType.by_datatype(type(data))
        if not data_type:
            raise TypeError(f"{type(data).__name__} is invalid FieldType")
        
        self.name = name
        self.type = data_type
        self.data = data

    def to_bytes(self) -> bytes:
        name = self.name.to_bytes()
        data = self.type.to_bytes(self.data)
        field_type = self.type.raw_type.to_bytes()
        field_length = len(data).to_bytes(2)
        return name + field_type + field_length + data
    
    def __repr__(self) -> str:
        name = self.name
        data = self.data
        date_type = self.type
        return f"<{type(self).__name__} {name=} {data=} {date_type=}>"

    @classmethod
    def from_bytes(cls, name: int, data: bytes, field_type: FieldType) -> Self:
        if not isinstance(field_type, FieldType):
            raise ValueError(f"field_type should be instance of FieldType")
        return cls(name, field_type.from_bytes(data))
    

class SingleDataField(DataField):

    def __init__(self, data: Any) -> None:
        super().__init__(0, data)

    def to_bytes(self) -> bytes:
        data = self.type.to_bytes(self.data)
        field_type = self.type.raw_type.to_bytes()
        return field_type + data
    
    def __repr__(self) -> str:
        data = self.data
        return f"<{type(self).__name__} {data=}>"
    
    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        if not isinstance(data, bytes):
            raise ValueError(f"data should be instance of bytes")
        if len(data) < 2:
            raise exceptions.DataException("Cannot convert data")
        
        field_type = FieldType.by_rawtype(data[0])
        if not field_type:
            raise exceptions.DataException("Invalid field_type")
        return cls(field_type.from_bytes(data[1:]))