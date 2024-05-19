from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from ssl import Purpose, SSLContext, create_default_context

from ..constants import DEFAULT_HOST, DEFAULT_PORT
from .base import AbstractAsyncioServer
from .connections.socket import SocketConnection, SocketMixin, TextConnection

logger = logging.getLogger("mara.server")


class AbstractSocketServer(AbstractAsyncioServer):
    connection_class: type[SocketMixin]
    _host: str
    _port: int
    _ssl_context: SSLContext | None = None

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        ssl: SSLContext | None = None,
        ssl_cert: str | Path | None = None,
        ssl_key: str | Path | None = None,
    ):
        self.host = host
        self.port = port
        if ssl or ssl_cert:
            if ssl and ssl_cert:
                raise ValueError("Cannot provide both an SSL context and certificate")

            if ssl_cert:
                ssl = create_default_context(Purpose.CLIENT_AUTH)
                ssl.check_hostname = False
                ssl.load_cert_chain(certfile=ssl_cert, keyfile=ssl_key)

            if not isinstance(ssl, SSLContext):
                raise ValueError("ssl must be an ssl.SSLContext")

            self._ssl_context = ssl

        super().__init__()

    def __str__(self):
        return f"{'SSL 'if self._ssl_context else ''}Socket {self.host}:{self.port}"

    async def create(self):
        await super().create()

        self.server = await asyncio.start_server(
            client_connected_cb=self.handle_connect,
            host=self.host,
            port=self.port,
            ssl=self._ssl_context,
        )

    async def handle_connect(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        connection: SocketMixin = self.connection_class(
            server=self, reader=reader, writer=writer
        )
        await self.connected(connection)


class SocketServer(AbstractSocketServer):
    connection_class: type[SocketConnection] = SocketConnection


class TextServer(AbstractSocketServer):
    connection_class: type[TextConnection] = TextConnection
