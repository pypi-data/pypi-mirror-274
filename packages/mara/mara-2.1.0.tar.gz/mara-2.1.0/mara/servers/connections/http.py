from aiohttp import WSMsgType
from aiohttp.web import Request, WebSocketResponse

from .base import AbstractConnection


class WebSocketConnection(AbstractConnection[str]):
    request: Request
    ws: WebSocketResponse

    def __str__(self):
        return str(self.request.remote)

    async def prepare(self, request: Request):
        self.request = request
        self.ws = WebSocketResponse()
        await self.ws.prepare(request)

    async def read(self) -> str:
        msg = await self.ws.receive()
        if msg.type == WSMsgType.TEXT:
            return msg.data
        elif msg.type == WSMsgType.ERROR:
            self.connected = False
            return ""
        # if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
        #    raise StopAsyncIteration
        return ""

    async def _write(self, data: str):
        await self.ws.send_str(data)
