"""Klasse `Server`."""

from __future__ import annotations

__all__: Final[list[str]] = ["Server"]

import socket
import sys
import threading
import weakref
from abc import ABC, abstractmethod
from contextlib import suppress
from typing import TYPE_CHECKING, Final

from nrw.datastructures import List

if sys.version_info >= (3, 12):  # pragma: >=3.12 cover
    from typing import override
else:  # pragma: <3.12 cover
    from typing_extensions import override

if TYPE_CHECKING:
    from io import TextIOWrapper


class _NewConnectionHandler(threading.Thread):
    __slots__: Final[tuple[str, str, str]] = ("_server", "_active", "_server_socket")

    def __init__(
        self,
        port: int,
        server: Server,
    ) -> None:
        super().__init__()
        self._server: weakref.ProxyType[Server] = weakref.proxy(
            server,
            self._on_server_shutdown,
        )
        try:
            self._server_socket: socket.socket | None = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )
            self._server_socket.bind(("127.0.0.1", port))
            self._server_socket.listen()
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._active: bool = True
            self.start()
        except Exception:  # pylint: disable=W0718
            self._active = False
            self._server_socket = None

    def _on_server_shutdown(
        self,
        server: Server,  # noqa: ARG002 # pylint: disable=W0613
    ) -> None:
        self.close()

    @override
    def run(self) -> None:
        while self._active:
            with suppress(OSError, ReferenceError):
                client_socket, (client_ip, client_port) = self._server_socket.accept()
                self._server._add_new_client_message_handler(client_socket)
                self._server.process_new_connection(client_ip, client_port)

    def close(self) -> None:
        self._active = False
        if self._server_socket is not None:
            with suppress(OSError):
                self._server_socket.close()


class _ClientSocketWrapper:
    __slots__: Final[tuple[str, str, str]] = (
        "_client_socket",
        "_to_client",
        "_from_client",
    )

    def __init__(self, client_socket: socket.socket | None) -> None:
        try:
            self._client_socket: socket.socket | None = client_socket
            self._to_client: TextIOWrapper | None = self._client_socket.makefile(
                mode="w",
                encoding="utf-8",
            )
            self._from_client: TextIOWrapper | None = self._client_socket.makefile(
                mode="r",
                encoding="utf-8",
            )
        except OSError:
            self._client_socket = None
            self._to_client = None
            self._from_client = None

    def receive(self) -> str | None:
        if self._from_client is not None:
            with suppress(OSError, ValueError):
                received_line: str = self._from_client.readline().strip()
                return received_line if received_line else None
        return None

    def send(self, message: str) -> None:
        if self._to_client is not None:
            with suppress(OSError, ValueError):
                self._to_client.write(f"{message}\n")
                self._to_client.flush()

    @property
    def client_ip(self) -> str | None:
        if self._client_socket is None:
            return None
        try:
            return self._client_socket.getpeername()[0]  # type: ignore[no-any-return]
        except OSError:
            return None

    @property
    def client_port(self) -> int:
        if self._client_socket is None:
            return 0
        try:
            return self._client_socket.getpeername()[1]  # type: ignore[no-any-return]
        except OSError:
            return 0

    def close(self) -> None:
        if self._client_socket is not None:
            with suppress(OSError):
                self._to_client.close()
                self._from_client.close()
                self._client_socket.shutdown(socket.SHUT_RDWR)
                self._client_socket.close()


class _ClientMessageHandler(threading.Thread):
    __slots__: Final[tuple[str, str, str]] = ("_server", "_active", "_socket_wrapper")

    def __init__(self, client_socket: socket.socket | None, server: Server) -> None:
        super().__init__()
        self._server: weakref.ProxyType[Server] = weakref.proxy(
            server,
            self._on_server_shutdown,
        )
        self._active: bool = False
        self._socket_wrapper: _ClientSocketWrapper = _ClientSocketWrapper(client_socket)
        if client_socket is not None:
            self._active = True
            self.start()

    def _on_server_shutdown(
        self,
        server: Server,  # noqa: ARG002 # pylint: disable=W0613
    ) -> None:
        self.close()

    @override
    def run(self) -> None:
        message: str | None = None
        while self._active:
            message = self._socket_wrapper.receive()
            client_ip: str | None = self._socket_wrapper.client_ip
            client_port: int = self._socket_wrapper.client_port
            with suppress(ReferenceError):
                if message is not None:
                    self._server.process_message(client_ip, client_port, message)
                else:
                    message_handler: _ClientMessageHandler | None = (
                        self._server._find_client_message_handler(
                            client_ip,
                            client_port,
                        )
                    )
                    if message_handler is not None:
                        message_handler.close()
                        self._server._remove_client_message_handler(message_handler)
                        self._server.process_closing_connection(client_ip, client_port)

    def send(self, message: str) -> None:
        if self._active:
            self._socket_wrapper.send(message)

    def close(self) -> None:
        if self._active:
            self._active = False
            self._socket_wrapper.close()

    @property
    def client_ip(self) -> str | None:
        return self._socket_wrapper.client_ip

    @property
    def client_port(self) -> int:
        return self._socket_wrapper.client_port


class Server(ABC):
    """Objekte von Unterklassen der abstrakten Klasse `Server` ermöglichen das Anbieten
    von Serverdiensten, so dass Clients Verbindungen zum Server mittels TCP/IP-Protokoll
    aufbauen können. Zur Vereinfachung finden Nachrichtenversand und -empfang
    zeilenweise statt, d. h., beim Senden einer Zeichenkette wird ein Zeilentrenner
    ergänzt und beim Empfang wird dieser entfernt. Verbindungsannahme,
    Nachrichtenempfang und Verbindungsende geschehen nebenläufig. Auf diese Ereignisse
    muss durch Überschreiben der entsprechenden Ereignisbehandlungsmethoden reagiert
    werden. Es findet nur eine rudimentäre Fehlerbehandlung statt, so dass z. B.
    Verbindungsabbrüche nicht zu einem Programmabbruch führen. Einmal unterbrochene oder
    getrennte Verbindungen können nicht reaktiviert werden.
    """

    __slots__: Final[tuple[str, str, str, str]] = (
        "__weakref__",
        "_lock",
        "_message_handlers",
        "_connection_handler",
    )

    def __init__(self, port: int) -> None:
        """Ein Objekt vom Typ `Server` wird erstellt, das über die angegebene Portnummer
        einen Dienst anbietet an. Clients können sich mit dem Server verbinden, so dass
        Daten (Zeichenketten) zu diesen gesendet und von diesen empfangen werden können.
        Kann der Server unter der angegebenen Portnummer keinen Dienst anbieten (z. B.
        weil die Portnummer bereits belegt ist), ist keine Verbindungsaufnahme zum
        Server und kein Datenaustausch möglich.
        """
        self._lock: threading.Lock = threading.Lock()
        self._message_handlers: List[_ClientMessageHandler] = List()
        self._connection_handler: _NewConnectionHandler = _NewConnectionHandler(
            port,
            self,
        )

    def _add_new_client_message_handler(self, client_socket: socket.socket) -> None:
        with self._lock:
            self._message_handlers.append(_ClientMessageHandler(client_socket, self))

    def _remove_client_message_handler(
        self,
        client_message_handler: _ClientMessageHandler,
    ) -> None:
        with self._lock:
            self._message_handlers.to_first()
            while self._message_handlers.has_access:
                if client_message_handler is self._message_handlers.content:
                    self._message_handlers.remove()
                    return
                self._message_handlers.next()

    def _find_client_message_handler(
        self,
        client_ip: str | None,
        client_port: int,
    ) -> _ClientMessageHandler | None:
        with self._lock:
            self._message_handlers.to_first()
            while self._message_handlers.has_access:
                current_message_handler: _ClientMessageHandler | None = (
                    self._message_handlers.content
                )
                assert current_message_handler is not None
                if (
                    current_message_handler.client_ip == client_ip
                    and current_message_handler.client_port == client_port
                ):
                    return current_message_handler
                self._message_handlers.next()
            return None

    @property
    def is_open(self) -> bool:
        """Die Anfrage liefert den Wert `True`, wenn der `Server` auf Port `port` einen
        Dienst anbietet. Ansonsten liefert die Methode den Wert `False`.
        """
        return self._connection_handler._active

    def is_connected_to(self, client_ip: str, client_port: int) -> bool:
        """Die Anfrage liefert den Wert `True`, wenn der Server mit dem durch
        `client_ip` und `client_port` spezifizierten Client aktuell verbunden ist.
        Ansonsten liefert die Methode den Wert `False`.
        """
        message_handler: _ClientMessageHandler | None = (
            self._find_client_message_handler(client_ip, client_port)
        )
        return message_handler is not None and message_handler._active

    def send(self, client_ip: str, client_port: int, message: str) -> None:
        """Die Nachricht `message` wird - um einen Zeilentrenner erweitert - an den
        durch `client_ip` und `client_port` spezifizierten Client gesendet. Schlägt der
        Versand fehl, geschieht nichts.
        """
        message_handler: _ClientMessageHandler | None = (
            self._find_client_message_handler(client_ip, client_port)
        )
        if message_handler is not None:
            message_handler.send(message)

    def send_to_all(self, message: str) -> None:
        """Die Nachricht `message` wird - um einen Zeilentrenner erweitert - an alle mit
        dem Server verbundenen Clients gesendet. Schlägt der Versand an einen Client
        fehl, wird dieser Client übersprungen.
        """
        with self._lock:
            self._message_handlers.to_first()
            while self._message_handlers.has_access:
                self._message_handlers.content.send(message)
                self._message_handlers.next()

    def close_connection(self, client_ip: str, client_port: int) -> None:
        """Die Verbindung des Servers zu dem durch `client_ip` und `client_port`
        spezifizierten Client wird getrennt. Zuvor wird die Methode
        `process_closing_connection` mit IP-Adresse und Port des jeweiligen Clients
        aufgerufen. Ist der Server nicht mit dem in der Parameterliste spezifizierten
        Client verbunden, geschieht nichts.
        """
        message_handler: _ClientMessageHandler | None = (
            self._find_client_message_handler(client_ip, client_port)
        )
        if message_handler is not None:
            self.process_closing_connection(client_ip, client_port)
            message_handler.close()
            self._remove_client_message_handler(message_handler)

    def close(self) -> None:
        """Alle bestehenden Verbindungen zu Clients werden getrennt und der Server kann
        nicht mehr verwendet werden. Ist der Server bereits vor Aufruf der Methode in
        diesem Zustand, geschieht nichts.
        """
        self._connection_handler.close()
        with self._lock:
            self._message_handlers.to_first()
            while self._message_handlers.has_access:
                message_handler: _ClientMessageHandler | None = (
                    self._message_handlers.content
                )
                assert message_handler is not None
                self.process_closing_connection(
                    message_handler.client_ip,
                    message_handler.client_port,
                )
                message_handler.close()
                self._message_handlers.remove()

    @abstractmethod
    def process_new_connection(
        self,
        client_ip: str,
        client_port: int,
    ) -> None:
        """Diese Ereignisbehandlungsmethode wird aufgerufen, wenn sich ein Client mit
        IP-Adresse `client_ip` und Portnummer `client_port` mit dem Server verbunden
        hat. Die Methode ist abstrakt und muss in einer Unterklasse der Klasse `Server`
        überschrieben werden, so dass auf den Neuaufbau der Verbindung reagiert wird.
        Der Aufruf der Methode erfolgt nicht synchronisiert.
        """

    @abstractmethod
    def process_message(
        self,
        client_ip: str | None,
        client_port: int,
        message: str,
    ) -> None:
        """Diese Ereignisbehandlungsmethode wird aufgerufen, wenn der Server die
        Nachricht `message` von dem durch `client_ip` und `client_port` spezifizierten
        Client empfangen hat. Der vom Client hinzugefügte Zeilentrenner wurde zuvor
        entfernt. Die Methode ist abstrakt und muss in einer Unterklasse der Klasse
        `Server` überschrieben werden, so dass auf den Empfang der Nachricht reagiert
        wird. Der Aufruf der Methode erfolgt nicht synchronisiert.
        """

    @abstractmethod
    def process_closing_connection(
        self,
        client_ip: str | None,
        client_port: int,
    ) -> None:
        """Sofern der Server die Verbindung zu dem durch `client_ip` und `client_port`
        spezifizierten Client trennt, wird diese Ereignisbehandlungsmethode aufgerufen,
        unmittelbar bevor die Verbindungstrennung tatsächlich erfolgt.
        Wird die Verbindung unvermittelt unterbrochen oder hat der in der Parameterliste
        spezifizierte Client die Verbindung zum Server unvermittelt getrennt, erfolgt
        der Methodenaufruf nach der Unterbrechung / Trennung der Verbindung.
        Die Methode ist abstrakt und muss in einer Unterklasse der Klasse Server
        überschrieben werden, so dass auf das Ende der Verbindung zum angegebenen Client
        reagiert wird. Der Aufruf der Methode erfolgt nicht synchronisiert.
        """
