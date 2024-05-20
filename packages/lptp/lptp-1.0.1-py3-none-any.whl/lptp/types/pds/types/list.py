from typing import List
from lptp import exceptions
from .base import DataType, FieldType, fieldtype


@fieldtype
class ListType(FieldType[list]):
    raw_type = 0xA4
    data_type = list
    data_aliases = (List,)

    def to_bytes(self, data: DataType) -> bytes:
        if not isinstance(data, list):
            raise TypeError("data should be instance of int")
        res = b""
        for el in data:
            el_type = FieldType.by_datatype(type(el))
            if not el_type:
                raise TypeError(f"{type(el).__name__} is invalid FieldType")
            el_data = el_type.to_bytes(el)
            res += el_type.raw_type.to_bytes() + len(el_data).to_bytes(2) + el_data
        return res

    def from_bytes(self, data: bytes) -> DataType:
        if not isinstance(data, bytes):
            raise TypeError("data should be instance of bytes")
        res = []
        while data:
            if len(data) < 3:
                raise exceptions.DataException("Cannot convert data")
            field_type = FieldType.by_rawtype(data[0])
            if not field_type:
                raise exceptions.DataException("Invalid field_type")
            content_length = int.from_bytes(data[1:3])
            if len(data) - 3 < content_length:
                raise exceptions.DataException("Field length exceeds data")
            res.append(field_type.from_bytes(data[3:content_length+3]))
            data = data[content_length+3:]
        return res