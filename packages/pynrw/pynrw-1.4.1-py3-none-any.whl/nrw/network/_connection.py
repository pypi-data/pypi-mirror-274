"""Klasse `Connection`."""

from __future__ import annotations

__all__: Final[list[str]] = ["Connection"]

import socket
from contextlib import suppress
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from io import TextIOWrapper


class Connection:
    """Objekte der Klasse `Connection` ermöglichen eine Netzwerkverbindung zu einem
    Server mittels TCP/IP-Protokoll. Nach Verbindungsaufbau können Zeichenketten
    (`Strings`) zum Server gesendet und von diesem empfangen werden. Zur
    Vereinfachung geschieht dies zeilenweise, d. h., beim Senden einer
    Zeichenkette wird ein Zeilentrenner ergänzt und beim Empfang wird dieser
    entfernt. Es findet nur eine rudimentäre Fehlerbehandlung statt, so dass z.B.
    der Zugriff auf unterbrochene oder bereits getrennte Verbindungen nicht zu
    einem Programmabbruch führt. Eine einmal getrennte Verbindung kann nicht
    reaktiviert werden.
    """

    __slots__: Final[tuple[str, str, str]] = ("_socket", "_to_server", "_from_server")

    def __init__(self, server_ip: str, server_port: int) -> None:
        """Ein Objekt vom Typ `Connection` wird erstellt. Dadurch wird eine Verbindung
        zum durch `server_ip` und `server_port` spezifizierten Server aufgebaut,
        so dass Daten (Zeichenketten) gesendet und empfangen werden können.
        Kann die Verbindung nicht hergestellt werden, kann die Instanz von Connection
        nicht mehr verwendet werden.
        """
        try:
            self._socket: socket.socket | None = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )
            self._socket.connect((server_ip, server_port))
            self._to_server: TextIOWrapper | None = self._socket.makefile(
                mode="w",
                encoding="utf-8",
            )
            self._from_server: TextIOWrapper | None = self._socket.makefile(
                mode="r",
                encoding="utf-8",
            )
        except OSError:
            self._socket = None
            self._to_server = None
            self._from_server = None

    def receive(self) -> str | None:
        """Es wird beliebig lange auf eine eingehende Nachricht vom Server gewartet und
        diese Nachricht anschließend zurückgegeben. Der vom Server angehängte
        Zeilentrenner wird zuvor entfernt. Während des Wartens ist der ausführende
        Prozess blockiert. Wurde die Verbindung unterbrochen oder durch den Server
        unvermittelt geschlossen, wird `None` zurückgegeben.
        """
        if self._from_server is not None:
            with suppress(OSError, ValueError):
                received_line: str = self._from_server.readline().strip()
                return received_line if received_line else None
        return None

    def send(self, message: str) -> None:
        """Die Nachricht `message` wird - um einen Zeilentrenner ergänzt - an den Server
        gesendet. Schlägt der Versand fehl, geschieht nichts.
        """
        if self._to_server is not None:
            with suppress(OSError, ValueError):
                self._to_server.write(f"{message}\n")
                self._to_server.flush()

    def close(self) -> None:
        """Die Verbindung zum Server wird getrennt und kann nicht mehr verwendet werden.
        War die Verbindung bereits getrennt, geschieht nichts.
        """
        if self._socket is not None:
            with suppress(OSError):
                self._to_server.close()
                self._from_server.close()
                self._socket.shutdown(socket.SHUT_RDWR)
                self._socket.close()
