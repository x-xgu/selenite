from typing import Any, Tuple

from pyais import encode_dict

from selenite.conf.protocol.socket import SocketConfig


class ShipAIS:
    def __init__(self, config: SocketConfig) -> None:
        self._socket = config
        self.mmsi: int = 0
        self.course: float = 0
        self.speed: float = 0
        self.position: Tuple[float, float] = (0, 0)

    def encode_msg(self) -> Any:
        lon, lat = self.position
        msg = {'mmsi': self.mmsi, 'type': 1, 'course': self.course, 'speed': self.speed, 'lon': lon, 'lat': lat}
        return encode_dict(msg, talker_id='AIVDM')[0]

    def send_ais_msg(self) -> None:
        self._socket.send_msg(self.encode_msg())
