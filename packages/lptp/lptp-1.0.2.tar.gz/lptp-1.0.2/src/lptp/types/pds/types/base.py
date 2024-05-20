from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Tuple, TypeVar
from .. import pds

fieldtypes: List[type["FieldType"]] = []
DataType = TypeVar("DataType")


class FieldType(ABC, Generic[DataType]):
    raw_type: int
    data_type: DataType
    data_aliases: Tuple = tuple()
    annotation: bool = False
    real_type: Optional[DataType]

    def __init__(self, real_type: Optional[DataType] = None) -> None:
        self.type = real_type

    @abstractmethod
    def to_bytes(self, data: DataType) -> bytes:
        pass

    @abstractmethod
    def from_bytes(self, data: bytes) -> DataType:
        pass

    @staticmethod
    def by_datatype(data_type: type) -> Optional["FieldType"]:
        t = next(filter(lambda t: t.data_type == data_type or data_type in t.data_aliases, fieldtypes), None)
        return t(data_type) if t else None

    @staticmethod
    def by_rawtype(raw_type: int) -> Optional["FieldType"]:
        t = next(filter(lambda t: t.raw_type == raw_type, fieldtypes), None)
        return t() if t else None
    
    @property
    def name(self) -> str:
        return type(self).__name__
    
    @property
    def type_name(self) -> str:
        return self.data_type.__name__
    
    def validate_field(self, field: "pds.DataField") -> bool:
        return field.type == self

    def __eq__(self, __value: object) -> bool:
        return type(self) == type(__value)

    def __repr__(self) -> str:
        return self.name

def fieldtype(cls):
    fieldtypes.append(cls)
    return cls