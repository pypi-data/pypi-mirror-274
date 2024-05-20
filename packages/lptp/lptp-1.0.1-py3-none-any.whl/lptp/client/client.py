from typing import Optional, Self
import asyncio

from lptp.types.packets import Packet, ServerPacket
from lptp.exceptions import UnopenedConnection, ClosedConnecton, AuthException
from lptp.types.packets import AuthPacket, AuthType, StatusCode, ExitPacket
from lptp.types.packets.procedure import ProcedurePacket
from lptp.types.pds.pds import ProcedureDataStructure


class LPTPClient:

    hostname: str
    port: int
    auth_type: AuthType
    key: Optional[bytes]
    hash: str
    authorized: bool
    reader: Optional[asyncio.StreamReader]
    writer: Optional[asyncio.StreamWriter]
    lock: asyncio.Lock

    def __init__(self, hostname: str = "127.0.0.1", port: int = 740, auth_type: AuthType = AuthType.Key, key: Optional[bytes | str] = None, hash: str = "") -> None:
        if not isinstance(hostname, str):
            raise TypeError("hostname should be instance of str")
        if not isinstance(port, int):
            raise TypeError("ip should be instance of int")
        if not isinstance(auth_type, AuthType):
            raise TypeError("auth_type should be instance of AuthType")
        if not isinstance(hash, str):
            raise TypeError("hash should be instance of str")
        if auth_type is AuthType.Key:
            if not key:
                raise TypeError("key is required with Key Auth")
            if not isinstance(key, bytes):
                if isinstance(key, str):
                    key = key.encode()
                else:
                    raise TypeError("key should be instance of bytes")
        
        self.hostname = hostname
        self.port = port
        self.auth_type = auth_type
        self.key = key
        self.hash = hash
        self.reader = None
        self.writer = None
        self.lock = asyncio.Lock()
        self.authorized = False

    async def auth(self) -> StatusCode:
        if self.authorized:
            raise AuthException("Already authorized")
        
        res = await self._send_packet(AuthPacket(self.auth_type, self.hash, self.key))
        if not res.ok:
            await self.close()
            if res.status_code == StatusCode.HashError:
                raise AuthException("Invalid procedure hash")
            raise AuthException(f"Authorization error with type {self.auth_type.name} ({res.status_code})")
        else:
            self.authorized = True
        return res.status_code

    async def send_procedure(self, name: int, subtype: int, pds: ProcedureDataStructure) -> ServerPacket:
        packet = ProcedurePacket(name, subtype, pds)
        return await self._send_packet(packet)

    async def _send_packet(self, packet: Packet) -> Optional[ServerPacket]:
        if not self.reader or not self.writer:
            raise UnopenedConnection
        if self.writer.is_closing():
            raise ClosedConnecton
        if packet.auth_required and not self.authorized:
            raise AuthException("Auth required before send this packet")
        
        async with self.lock:
            self.writer.write(packet.to_bytes())
            data = await self.reader.read(65535)
            if not data:
                raise ClosedConnecton("Server closed the connection")
            return ServerPacket.from_bytes(data)

    async def close(self) -> None:
        if not self.reader or not self.writer:
            raise UnopenedConnection
        
        await self._send_packet(ExitPacket())
        self.writer.close()
        await self.writer.wait_closed()

    async def connect(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(self.hostname, self.port)
        self.authorized = False

    async def __aenter__(self) -> Self:
        await self.connect()
        await self.auth()

        return self
    
    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()