import socket


class SocketConfig:
    """
    SocketConfig is a class that contains the configuration for the socket
    """
    def __init__(
            self,
            *,
            ip: str,
            port: int
    ) -> None:
        self.addr = (ip, port)
        self.socket = None

    def open_socket(self) -> None:
        """
        Open Socket
        """
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

    def close_socket(self) -> None:
        """
        Close Socket
        """
        self.socket.close()

    def send_msg(self, msg: str) -> None:
        """
        Send Message
        """
        with socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM
        ) as s:
            s.sendto(
                msg.encode(),
                self.addr
            )
