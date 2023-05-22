import socket


class SocketConfig:
    def __init__(self, *, ip: str, port: int) -> None:
        self.addr = (ip, port)
        self.socket = None

    def open_socket(self) -> None:
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

    def close_socket(self) -> None:
        self.socket.close()

    def send_msg(self, msg: str) -> None:
        with socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM
        ) as s:
            s.sendto(
                msg.encode(),
                self.addr
            )
