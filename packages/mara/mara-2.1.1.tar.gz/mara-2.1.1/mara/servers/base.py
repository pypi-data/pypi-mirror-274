from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from ..app import event_manager
from ..events import Event, ListenStart, ListenStop
from ..status import Status

if TYPE_CHECKING:
    from ..app import App
    from .connections import AbstractConnection

logger = logging.getLogger("mara.server")

DeferredEventType = tuple[
    type[Event], event_manager.HandlerType, event_manager.FilterType
]


class AbstractServer:
    app: App | None = None
    connections: list[AbstractConnection]
    _status: Status = Status.IDLE
    _events: list[DeferredEventType]

    def __init__(self):
        self.connections = []
        self._events: list[DeferredEventType] = []

    def __str__(self):
        return self.__class__.__name__

    async def run(self, app: App):
        """
        Create the server
        """
        self.app = app

        # Register deferred events
        for event_class, handler, filters in self._events:
            self.app.on(event_class=event_class, handler=handler, **filters)

        # Initialise server and listen
        await self.create()
        await self.listen()

    async def create(self):
        logger.debug(f"Server starting: {self}")
        self._status = Status.STARTING

    async def listen(self):
        """
        Main listening loop
        """
        logger.debug(f"Server running: {self}")
        self._status = Status.RUNNING

        # Raise the event
        await self.app.events.trigger(ListenStart(self))

        # Start the server
        await self.listen_loop()

        # Look has exited, likely due to a call to self.stop()
        logger.debug(f"Server stopping: {self}")
        await self.app.events.trigger(ListenStop(self))
        logger.info(f"Server stopped: {self}")
        self._status = Status.STOPPED

    async def listen_loop(self):
        """
        Placeholder for subclasses to implement their listen loop
        """
        pass

    async def connected(self, connection: AbstractConnection):
        """
        Register a new client connection and start the lifecycle
        """
        logger.info(f"[{self}] Connection from {connection}")
        self.connections.append(connection)
        connection.run()

    async def disconnected(self, connection: AbstractConnection):
        """
        Unregister a connection that has disconnected
        """
        self.connections.remove(connection)

    def stop(self):
        """
        Shut down the server
        """
        self._status = Status.STOPPING
        logger.info(f"Server closing: {self}")

    @property
    def status(self) -> Status:
        return self._status

    def on(
        self,
        event_class: type[Event],
        handler: event_manager.HandlerType | None = None,
        **filters: event_manager.FilterType,
    ):
        filters["server"] = self

        if self.app is not None:
            return self.app.on(event_class=event_class, handler=handler, **filters)

        def defer(handler):
            self._events.append((event_class, handler, filters))
            return handler

        if handler is not None:
            defer(handler)
            return handler

        return defer


class AbstractAsyncioServer(AbstractServer):
    """
    Base class for servers based on asyncio.Server
    """

    server: asyncio.base_events.Server

    async def listen_loop(self):
        async with self.server:
            await self.server.serve_forever()

    def stop(self):
        """
        Shut down the server
        """
        super().stop()
        self.server.close()

    @property
    def status(self) -> Status:
        status = super().status

        if status == Status.RUNNING and not self.server.is_serving():
            return Status.STARTING

        return status
