from typing import List, Self
from lptp import exceptions
from .field import DataField
from .types import FieldType


class ProcedureDataStructure:
    fields: List[DataField]

    def __init__(self, fields: List[DataField] = []) -> None:
        if not isinstance(fields, list):
            raise TypeError("fields should be list of DataField")
        for field in fields:
            if not isinstance(field, DataField):
                raise TypeError("fields children should be instance of DataField")
            if field.type.annotation:
                raise TypeError(f"{field.name} is only annotation")

        self.fields = fields[:]

    def add_field(self, field: DataField) -> None:
        if not isinstance(field, DataField):
            raise TypeError("data should be instance of DataField")
        
        self.fields.append(field)

    def get_params(self) -> list:
        return [field.data for field in sorted(self.fields, key=lambda f: f.name)]

    def to_bytes(self) -> bytes:
        data = b"".join([field.to_bytes() for field in self.fields])
        return data
    
    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        if not isinstance(data, bytes):
            raise TypeError("data should be instance of bytes")

        fields = []
        while data:
            if len(data) < 4:
                raise exceptions.DataException("Cannot convert data")
            name = data[0]
            field_type = FieldType.by_rawtype(data[1])
            if not field_type:
                raise exceptions.DataException("Invalid field_type")
            field_length = int.from_bytes(data[2:4])
            if len(data) - 4 < field_length:
                raise exceptions.DataException("Field length exceeds data")
            fields.append(DataField.from_bytes(name, data[4:field_length+4], field_type))
            data = data[4 + field_length:]
        return cls(fields)