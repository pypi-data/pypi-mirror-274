from abc import ABC, abstractmethod
from typing import Optional, Self

from lptp.types.pds.field import SingleDataField
from lptp import exceptions
from .status import StatusCode


class Packet(ABC):

    auth_required: bool = False

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes) -> Self:
        pass

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

class ServerPacket(Packet):
    status_code: StatusCode
    field: Optional[SingleDataField]

    def __init__(self, status_code: int, field: Optional[SingleDataField] = None) -> None:
        if not isinstance(status_code, int):
            raise TypeError("status_code should be instance of int")
        if field and not isinstance(field, SingleDataField):
            raise TypeError("field should be instance of DataField")

        self.status_code = status_code
        self.field = field

    def to_bytes(self) -> bytes:
        return self.status_code.to_bytes() + (self.field.to_bytes() if self.field else b'')
    
    def __repr__(self) -> str:
        status_code = self.status_code
        field = self.field
        return f"<{type(self).__name__} {status_code=} {field=}>"

    @property
    def ok(self) -> bool:
        return self.status_code is StatusCode.Ok

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        if not isinstance(data, bytes):
            raise TypeError("data should be instance of bytes")
        
        if not data:
            raise exceptions.DataException("Cannot convert data")
        
        try:
            status_code = StatusCode(data[0])
        except ValueError:
            raise exceptions.DataException("Invalid status_code")
        if data[1:]:
            field = SingleDataField.from_bytes(data[1:])
        else:
            field = None
        
        return cls(status_code, field)