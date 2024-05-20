from typing import Self
from .base import Packet


class ExitPacket(Packet):
    auth_required = False

    def to_bytes(self) -> bytes:
        return 0x00.to_bytes()
    
    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        return cls()