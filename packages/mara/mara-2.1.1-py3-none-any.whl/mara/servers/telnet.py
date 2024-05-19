"""
Telnet server

Wrapper around telnetlib3, https://pypi.org/project/telnetlib3/
"""

from __future__ import annotations

from ..constants import DEFAULT_HOST, DEFAULT_PORT
from .base import AbstractAsyncioServer
from .connections.telnet import TelnetConnection

try:
    import telnetlib3
except ImportError:
    raise ValueError("telnetlib3 not found - pip install mara[telnet]")


class TelnetServer(AbstractAsyncioServer):
    connection_class: type[TelnetConnection] = TelnetConnection

    def __init__(
        self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, **telnet_kwargs
    ):
        self.host = host
        self.port = port

        if "shell" in telnet_kwargs:
            raise ValueError("Cannot specify a shell for TelnetServer")
        self.telnet_kwargs = telnet_kwargs
        self.telnet_kwargs["shell"] = self.handle_connect

        super().__init__()

    def __str__(self):
        return f"Telnet {self.host}:{self.port}"

    async def create(self):
        await super().create()
        if not self.app or (loop := self.app.loop) is None:
            raise ValueError("Cannot start TelnetServer without running loop")

        self.server = await loop.create_server(
            protocol_factory=lambda: telnetlib3.TelnetServer(**self.telnet_kwargs),
            host=self.host,
            port=self.port,
        )

    async def handle_connect(
        self, reader: telnetlib3.TelnetReader, writer: telnetlib3.TelnetWriter
    ):
        connection: TelnetConnection = self.connection_class(
            server=self, reader=reader, writer=writer
        )
        await self.connected(connection)
