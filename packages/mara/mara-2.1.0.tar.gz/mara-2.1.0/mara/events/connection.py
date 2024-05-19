"""
Connection events
"""

from __future__ import annotations

from .base import Event

__all__ = ["Connection", "Connect", "Receive", "Disconnect"]


class Connection(Event):
    "Connection event"

    def __init__(self, connection):
        super(Connection, self).__init__()
        self.connection = connection
        self.server = getattr(connection, "server", None)

    def __str__(self):
        msg = super(Connection, self).__str__().strip()
        return f"{msg} ({self.connection})"


class Connect(Connection):
    "Connection connected"


class Disconnect(Connection):
    "Connection disconnected"


class Receive(Connection):
    "Data received"

    def __init__(self, connection, data):
        super(Receive, self).__init__(connection)
        self.data = data

    def __str__(self):
        msg = super(Receive, self).__str__().strip()
        return f"{msg}: {self.data}"
