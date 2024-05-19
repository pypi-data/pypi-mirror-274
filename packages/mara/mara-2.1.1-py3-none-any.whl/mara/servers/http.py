"""
HTTP server

Wrapper around aiohttp, https://pypi.org/project/aiohttp/
"""

from __future__ import annotations

from asyncio import sleep
from typing import TYPE_CHECKING

from aiohttp import web

from ..constants import DEFAULT_HOST, DEFAULT_PORT
from ..status import Status
from .base import AbstractAsyncioServer, AbstractServer
from .connections.http import WebSocketConnection

if TYPE_CHECKING:
    from ..app import App


class WebSocketServer(AbstractServer):
    """
    A websocket server is a sub-server of an HttpServer.

    To create a websocket server, call HttpServer.create_websocket(..)
    """

    connection_class = WebSocketConnection

    def __init__(self, http_server: HttpServer):
        self.http_server = http_server
        super().__init__()

    async def listen_loop(self):
        # Keep the server active
        while self.http_server.status != Status.STOPPED:
            await sleep(0.1)

    async def handle_connect(self, request):
        connection: WebSocketConnection = self.connection_class(server=self)
        await connection.prepare(request)
        await self.connected(connection)

        # Keep the connection open
        while connection.connected:
            await sleep(0.1)


class HttpServer(AbstractAsyncioServer):
    #: Host
    host: str

    #: Port
    port: int

    #: aiohttp web.Application instance
    web_app: web.Application

    #: websocket servers provided by this server
    websockets: list[WebSocketServer]

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        web_app: web.Application | None = None,
        **handler_kwargs,
    ):
        self.host = host
        self.port = port
        if web_app:
            self.web_app = web_app
        else:
            self.web_app = web.Application()
        self.handler_kwargs = handler_kwargs

        self.websockets: list[WebSocketServer] = []
        super().__init__()

    def __str__(self):
        return f"HTTP {self.host}:{self.port}"

    async def run(self, app: App):
        for ws in self.websockets:
            app.add_server(ws)
        await super().run(app)

    async def create(self):
        await super().create()

        loop = self.app.loop if self.app else None
        if loop is None:
            raise ValueError("Cannot start HttpServer without running loop")

        self.server = await loop.create_server(
            protocol_factory=self.web_app.make_handler(**self.handler_kwargs),
            host=self.host,
            port=self.port,
        )

    def add_route(self, method: str, path: str, *, name=None, expect_handler=None):
        def decorator(handler):
            self.web_app.router.add_route(
                method, path, handler, name=name, expect_handler=expect_handler
            )
            return handler

        return decorator

    def add_get(self, path: str, **kwargs):
        return self.add_route("GET", path, **kwargs)

    def add_post(self, path: str, **kwargs):
        return self.add_route("POST", path, **kwargs)

    def add_head(self, path: str, **kwargs):
        return self.add_route("HEAD", path, **kwargs)

    def add_put(self, path: str, **kwargs):
        return self.add_route("PUT", path, **kwargs)

    def add_patch(self, path: str, **kwargs):
        return self.add_route("PATCH", path, **kwargs)

    def add_delete(self, path: str, **kwargs):
        return self.add_route("DELETE", path, **kwargs)

    def add_view(self, path: str, **kwargs):
        return self.add_route("*", path, **kwargs)

    def create_websocket(self, path: str):
        ws = WebSocketServer(self)
        self.add_get(path)(ws.handle_connect)
        self.websockets.append(ws)
        if self.app:
            self.app.add_server(ws)
        return ws
