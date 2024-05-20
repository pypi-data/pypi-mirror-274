from typing import List, Optional
from lptp.exceptions import RequestError
from lptp.server.file_generator import generate_proc_file
from lptp.types import AuthPacket, ExitPacket, ProcedurePacket, ServerPacket, AuthType, StatusCode
from lptp.types.pds.field import SingleDataField
from .manager import Manager
from .log import logger
import asyncio, traceback


class LPTPServer:
    hostname: str
    port: int
    connection_wait: int
    auth_type: AuthType
    key: Optional[bytes | str]
    ips: List[str]
    manager: Manager

    def __init__(
            self,
            hostname: str = "127.0.0.1",
            port: int = 740,
            auth_type: AuthType = AuthType.Key,
            key: Optional[bytes] = None,
            ips: List[str] = [],
            connection_wait: int = 30
        ) -> None:
        if not isinstance(hostname, str):
            raise TypeError("hostname should be instance of str")
        if not isinstance(port, int):
            raise TypeError("ip should be instance of int")
        if not isinstance(connection_wait, int):
            raise TypeError("connection_wait should be instance of int")
        if auth_type is AuthType.Key:
            if not key:
                raise TypeError("key is required with Key Auth")
            if not isinstance(key, bytes):
                if isinstance(key, str):
                    key = key.encode()
                else:
                    raise TypeError("key should be instance of bytes")
        if auth_type is AuthType.Ip:
            if not isinstance(ips, list):
                raise TypeError("ips should be instance of list")
        
        self.hostname = hostname
        self.port = port
        self.connection_wait = connection_wait
        self.auth_type = auth_type
        self.key = key
        self.ips = ips[:]
        self.manager = Manager()

    def add_manager(self, *args: List[Manager]) -> None:
        for manager in args:
            if not isinstance(manager, Manager):
                raise TypeError("manager children should be instance of Manager")
            self.manager.extend(manager)

    async def _run_forever(self) -> None:
        loop = asyncio.get_running_loop()
        self.server = await loop.create_server(
            lambda: LPTPProtocol(self),
            self.hostname,
            self.port
        )
        async with self.server:
            logger.info(f"Server started on {self.hostname}:{self.port}")
            await self.server.serve_forever()

    def generate_proc_file(self, filename: str = "lptp_procedures.py"):
        if not isinstance(filename, str):
            raise TypeError("filename should be instance of str")
        generate_proc_file(filename, self.manager)

    def run_forever(self) -> None:
        asyncio.run(self._run_forever())

class LPTPProtocol(asyncio.Protocol):
    server: LPTPServer
    transport: asyncio.WriteTransport
    ip: str
    port: int
    authorized: False
    timer: asyncio.Task

    def __init__(self, server: LPTPServer) -> None:
        self.server = server

    def connection_made(self, transport: asyncio.WriteTransport) -> None:
        self.transport = transport
        self.ip, self.port = transport.get_extra_info("peername")
        self.authorized = False
        self.timer = asyncio.ensure_future(self.connection_timer())

    def connection_lost(self, exc) -> None:
        logger.info(f"Closed connection from {self.ip}:{self.port}")

    async def connection_timer(self) -> None:
        await asyncio.sleep(self.server.connection_wait)
        self.transport.close()

    async def auth_handler(self, data: bytes) -> bool:
        packet = AuthPacket.from_bytes(data)
        if packet.hash != self.server.manager.hash:
            raise RequestError(status_code = StatusCode.HashError)
        if packet.type is AuthType.Key and self.server.auth_type is AuthType.Key:
            if packet.key != self.server.key:
                raise RequestError(status_code = StatusCode.AuthError)
        elif packet.type is AuthType.Ip and self.server.auth_type is AuthType.Ip:
            if self.ip not in self.server.ips:
                raise RequestError(status_code = StatusCode.AuthError)
        elif packet.type is not AuthType.Without or self.server.auth_type is not AuthType.Without:
            raise RequestError(status_code = AuthType.Without)
        self.transport.write(ServerPacket(StatusCode.Ok).to_bytes())
        self.authorized = True
        
    async def procedure_handler(self, data: bytes) -> None:
        packet = ProcedurePacket.from_bytes(data)
        procedure = self.server.manager.get(packet.name, packet.subtype)
        if not procedure:
            raise RequestError("Invalid procedure", StatusCode.Undefined)
        field = SingleDataField(await procedure.call(packet.pds))
        self.transport.write(ServerPacket(StatusCode.Ok, field).to_bytes())

    async def receive_handler(self, data: bytes) -> None:
        if data == ExitPacket().to_bytes():
            self.transport.write(ServerPacket(StatusCode.Ok).to_bytes())
            self.transport.close()
            return
        
        try:
            if not self.authorized:
                await self.auth_handler(data)
            else:
                await self.procedure_handler(data)
        except RequestError as exc:
            logger.debug(str(exc))
            self.transport.write(ServerPacket(exc.status_code).to_bytes())

    async def data_received_async(self, data: bytes) -> None:
        logger.info(f"New receive from {self.ip}:{self.port} with {len(data)} bytes")
        
        try:
            await self.receive_handler(data)
        except Exception as err:
            traceback.print_exception(err)
            self.transport.write(ServerPacket(StatusCode.InternalError).to_bytes())

        self.timer.cancel()
        self.timer = asyncio.ensure_future(self.connection_timer())

    def data_received(self, data: bytes):
        asyncio.ensure_future(self.data_received_async(data))