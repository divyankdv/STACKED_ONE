"""
============================================================

                    STACKED ONE

                CONNECTION STATE

------------------------------------------------------------

Represents the lifecycle of an exchange connection.

============================================================
"""

from enum import StrEnum


class ConnectionState(StrEnum):

    DISCONNECTED = "disconnected"

    CONNECTING = "connecting"

    CONNECTED = "connected"

    RECONNECTING = "reconnecting"

    STOPPING = "stopping"

    STOPPED = "stopped"

    @property
    def active(self) -> bool:

        return self in (

            ConnectionState.CONNECTING,

            ConnectionState.CONNECTED,

            ConnectionState.RECONNECTING,

        )