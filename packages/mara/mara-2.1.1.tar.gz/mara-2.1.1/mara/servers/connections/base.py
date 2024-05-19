from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Generic, TypeVar

from ...events import Connect, Disconnect, Receive
from ...storage.dict import DictStore

if TYPE_CHECKING:
    from ..base import AbstractServer


ContentType = TypeVar("ContentType")

logger = logging.getLogger("mara.connection")


class AbstractConnection(Generic[ContentType]):
    server: AbstractServer
    connected: bool
    read_task: asyncio.Task
    write_task: asyncio.Task
    write_queue: asyncio.Queue
    session: DictStore

    def __init__(self, server: AbstractServer):
        self.server = server
        self.connected = True
        self.session = DictStore()
        # TODO: Queue(maxsize=?) - configure from server
        self.write_queue = asyncio.Queue()

    def __str__(self):
        return "unknown"

    async def read(self) -> ContentType:
        raise NotImplementedError()

    def write(self, data: ContentType):
        """
        Write to the outbound queue
        """
        self.write_queue.put_nowait(data)

    async def flush(self):
        """
        Wait for all outbound data to be sent
        """
        await self.write_queue.join()

    async def _write(self, data: ContentType):
        """
        Write to the connection
        """
        raise NotImplementedError()

    async def close(self):
        logger.info(f"Connection {self} closed")
        await self.server.disconnected(self)

    def run(self):
        """
        Add the connection read and write tasks to the app's loop
        """
        if not self.server.app:
            raise ValueError("Connection read loop must be part of an active server")
        self.read_task = self.server.app.create_task(self._read_loop())
        self.write_task = self.server.app.create_task(self._write_loop())

    async def _read_loop(self):
        app = self.server.app
        if not app:
            raise ValueError("Connection read loop must be part of an active server")
        await app.events.trigger(Connect(self))
        logger.info(f"Connection {self} connected")
        while self.connected:
            data: ContentType = await self.read()
            if data:
                await app.events.trigger(Receive(self, data))

        logger.info(f"Connection {self} disconnected")
        await app.events.trigger(Disconnect(self))

    async def _write_loop(self):
        while self.connected:
            data: ContentType = await self.write_queue.get()
            await self._write(data)
            self.write_queue.task_done()
