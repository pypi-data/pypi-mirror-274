"""Klasse `Client`."""

from __future__ import annotations

__all__: Final[list[str]] = ["Client"]

import socket
import threading
from abc import ABC, abstractmethod
from contextlib import suppress
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from io import TextIOWrapper


class _SocketWrapper:
    __slots__: Final[tuple[str, str, str]] = ("_socket", "_to_server", "_from_server")

    def __init__(self, server_ip: str, server_port: int) -> None:
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
        if self._from_server is not None:
            with suppress(OSError, ValueError):
                received_line: str = self._from_server.readline().strip()
                return received_line if received_line else None
        return None

    def send(self, message: str) -> None:
        if self._to_server is not None:
            with suppress(OSError, ValueError):
                self._to_server.write(f"{message}\n")
                self._to_server.flush()

    def close(self) -> None:
        if self._socket is not None:
            with suppress(OSError):
                self._to_server.close()
                self._from_server.close()
                self._socket.shutdown(socket.SHUT_RDWR)
                self._socket.close()


class Client(ABC):
    """Objekte von Unterklassen der abstrakten Klasse `Client` ermöglichen
    Netzwerkverbindungen zu einem Server mittels TCP/IP-Protokoll.
    Nach Verbindungsaufbau können Zeichenketten (`Strings`) zum Server gesendet und von
    diesem empfangen werden, wobei der Nachrichtenempfang nebenläufig geschieht.
    Zur Vereinfachung finden Nachrichtenversand und -empfang zeilenweise statt, d. h.,
    beim Senden einer Zeichenkette wird ein Zeilentrenner ergänzt und
    beim Empfang wird dieser entfernt. Jede empfangene Nachricht wird einer
    Ereignisbehandlungsmethode übergeben, die in Unterklassen implementiert werden muss.
    Es findet nur eine rudimentäre Fehlerbehandlung statt, so dass z. B.
    Verbindungsabbrüche nicht zu einem Programmabbruch führen.
    Eine einmal unterbrochene oder getrennte Verbindung kann nicht reaktiviert werden.
    """

    __slots__: Final[tuple[str, str]] = ("_socket_wrapper", "_active")

    def __init__(self, server_ip: str, server_port: int) -> None:
        """Es wird eine Verbindung zum durch `server_ip` und `server_port`
        spezifizierten Server aufgebaut, so dass Daten (Zeichenketten) gesendet und
        empfangen werden können. Kann die Verbindung nicht hergestellt werden, kann der
        Client nicht zum Datenaustausch verwendet werden.
        """
        self._socket_wrapper: _SocketWrapper = _SocketWrapper(server_ip, server_port)
        if self._socket_wrapper._socket is not None:
            self._active: bool = True
        else:
            self._active = False
        message_handler_thread: threading.Thread = threading.Thread(target=self._run)
        message_handler_thread.start()

    def _run(self) -> None:
        message: str | None = None
        while self._active:
            message = self._socket_wrapper.receive()
            if message is not None:
                self.process_message(message)
            else:
                self.close()

    def send(self, message: str) -> None:
        """Die Nachricht `message` wird - um einen Zeilentrenner ergänzt - an den Server
        gesendet. Schlägt der Versand fehl, geschieht nichts.
        """
        if self._active:
            self._socket_wrapper.send(message)

    def close(self) -> None:
        """Die Verbindung zum Server wird getrennt und der Client kann nicht mehr
        verwendet werden. Ist `Client` bereits vor Aufruf der Methode in diesem Zustand,
        geschieht nichts.
        """
        if self._active:
            self._active = False
            self._socket_wrapper.close()

    @property
    def is_connected(self) -> bool:
        """Die Anfrage liefert den Wert `True`, wenn der Client mit dem Server
        aktuell verbunden ist. Ansonsten liefert sie den Wert `False`.
        """
        return self._active

    @abstractmethod
    def process_message(self, message: str) -> None:
        """Diese Methode wird aufgerufen, wenn der Client die Nachricht `message` vom
        Server empfangen hat. Der vom Server ergänzte Zeilentrenner wurde zuvor
        entfernt. Die Methode ist abstrakt und muss in einer Unterklasse der Klasse
        `Client` überschrieben werden, so dass auf den Empfang der Nachricht reagiert
        wird. Der Aufruf der Methode erfolgt nicht synchronisiert.
        """
