from typing import Self
from lptp.types.pds import ProcedureDataStructure
from lptp import exceptions
from .base import Packet


class ProcedurePacket(Packet):
    name: int
    subtype: int
    pds: ProcedureDataStructure
    auth_required = True

    def __init__(self, name: int, subtype: int, pds: ProcedureDataStructure) -> None:
        if not isinstance(name, int):
            raise TypeError("name should be instance of int")
        if not isinstance(subtype, int):
            raise TypeError("subtype should be instance of int")
        if not isinstance(pds, ProcedureDataStructure):
            raise TypeError("PDS should be instance of ProcedureDataStructure")
            
        self.name = name
        self.subtype = subtype
        self.pds = pds

    def to_bytes(self) -> bytes:
        return self.name.to_bytes() + self.subtype.to_bytes() + self.pds.to_bytes()

    def __repr__(self) -> str:
        name = self.name
        subtype = self.subtype
        pds = self.pds
        return f"<{type(self).__name__} {name=} {subtype=} {pds=}>"

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        if not isinstance(data, bytes):
            raise TypeError("data should be instance of bytes")
    
        if len(data) < 2:
            raise exceptions.DataException("Cannot convert data")

        name = data[0]
        subtype = data[1]
        if data[2:]:
            pds = ProcedureDataStructure.from_bytes(data[2:])
        else:
            pds = ProcedureDataStructure()
        return cls(name, subtype, pds)