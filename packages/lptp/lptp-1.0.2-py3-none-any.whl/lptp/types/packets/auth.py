from enum import Enum
from typing import Optional, Self
from lptp import exceptions
from .base import Packet


class AuthType(int, Enum):
    Without = 0x0A
    Key = 0x0B
    Ip = 0x0C

class AuthPacket(Packet):
    type: AuthType
    hash: bytes
    key: Optional[bytes]
    auth_required = False

    def __init__(self, type: AuthType, hash: str, key: Optional[bytes] = None) -> None:
        if not isinstance(type, AuthType):
            raise TypeError("type should be instance of AuthType")
        if not isinstance(hash, str):
            raise TypeError("hash should be instance of str")
        if key and not isinstance(key, bytes):
            if isinstance(key, str):
                key = key.encode()
            else:
                raise TypeError("key should be instance of bytes")
        
        self.type = type
        self.hash = hash
        self.key = key

    def to_bytes(self) -> bytes:
        hash = bytes.fromhex(self.hash)
        if len(hash) != 32:
            raise ValueError("hash size should be 32 bytes")
        return self.type.to_bytes() + hash + (self.key if self.key else b'')
    
    def __repr__(self) -> str:
        authtype = self.type
        hash = self.hash
        key = self.key
        return f"<{type(self).__name__} {authtype=} {key=} {hash=}>"

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        if not isinstance(data, bytes):
            raise TypeError("data should be instance of bytes")
        
        if not data:
            raise exceptions.DataException("Cannot convert data")
        
        try:
            type = AuthType(data[0])
            hash = data[1:33]
            if type is AuthType.Key and not data[33:]:
                raise exceptions.DataException("Key is required for this AuthType")
        except ValueError:
            raise exceptions.DataException("Invalid auth_type")
        
        return cls(type, hash.hex(), data[33:])