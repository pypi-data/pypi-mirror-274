"""Die Netzklassen nach den Vorgaben des Landes NRW."""

from __future__ import annotations

__all__: Final[list[str]] = ["Connection", "Client", "Server"]

from typing import Final

from nrw.network._client import Client
from nrw.network._connection import Connection
from nrw.network._server import Server
