from .base import DataType, FieldType, fieldtype
from lptp import exceptions
from .. import pds
from typing import Any, Optional, Union


class AnnotationType(FieldType[DataType]):
    raw_type = -1
    annotation = True

    def to_bytes(self, data: Any) -> bytes:
        raise NotImplementedError
    
    def from_bytes(self, data: bytes) -> Any:
        return NotImplementedError
    
    @property
    def type_name(self) -> str:
        return self.name

@fieldtype
class AnyType(AnnotationType[Any]):
    data_type = Any
    data_aliases = (type(Any),)
    
    def __eq__(self, __value: Any) -> bool:
        return True

    @property
    def name(self) -> str:
        return "Any"
    
# @fieldtype
# class UnionType(AnnotationType[Union]):
#     data_type = Union
#     data_aliases = (type(Union[Any]),)
#     args: list[FieldType]

#     def __init__(self, real_type: Union[Any]) -> None:
#         super().__init__(real_type)
#         self.args = []
#         for arg in real_type.__args__:
#             field_type = FieldType.by_datatype(type(arg))
#             if not field_type:
#                 raise TypeError(f"{field_type} is invalid FieldType")
#             self.args.append(field_type)

#     def validate_field(self, field: "pds.DataField") -> bool:
#         for arg in self.args:
#             if field.type == arg:
#                 return True
#         return False

#     @property
#     def name(self) -> str:
#         return f"Union[{', '.join([arg.type_name for arg in self.args])}]"

# @fieldtype
# class OptionalType(FieldType):
#     raw_type = 0xA3
#     data_type = Optional
#     data_aliases = (type(Optional),)
#     annonation = True

#     def to_bytes(self, data: Any) -> bytes:
#         raise NotImplementedError
    
#     def from_bytes(self, data: bytes) -> Any:
#         return NotImplementedError
    
#     def __eq__(self, __value: Any) -> bool:
#         return self

#     @property
#     def name(self) -> str:
#         return "Any"
    
#     @property
#     def type_name(self) -> str:
#         return self.name
    
@fieldtype
class NullType(FieldType[None]):
    raw_type = 0xA3
    data_type = None
    data_aliases = (type(None),)

    def to_bytes(self, data: DataType) -> bytes:
        return 0x00.to_bytes()
    
    def from_bytes(self, data: bytes) -> DataType:
        if not isinstance(data, bytes):
            raise TypeError("data should be instance of bytes")
        if data != 0x00.to_bytes():
            raise exceptions.DataException("Invalid null byte")
        return None

    def __eq__(self, __value: object) -> bool:
        return __value is None
    
    @property
    def name(self) -> str:
        return "None"
    
    @property
    def type_name(self) -> str:
        return self.name