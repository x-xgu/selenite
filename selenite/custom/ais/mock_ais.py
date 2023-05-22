from typing import Any, Tuple
from pyais import encode_dict
from selenite.conf.protocol.socket import SocketConfig


class ShipAIS:
    """
    Mock sending AIS messages to a socket.
    """
    mmsi: int = None
    course: float = None
    speed: float = None
    position: Tuple[float, float] = None

    def __init__(
            self,
            config: SocketConfig
    ) -> None:
        """
        Initialize ShipAIS object with a SocketConfig object.

        Args:
            config (SocketConfig): SocketConfig object containing socket information.
        """
        self._socket = config

    def encode_msg(
            self
    ) -> Any:
        """
        Encode AIS message into a byte string.

        Returns:
            Any: Encoded AIS message as a byte string.

        Example:
            >>> ais = ShipAIS(SocketConfig())
            >>> ais.mmsi = 123456789
            >>> ais.course = 90.5
            >>> ais.speed = 10.2
            >>> ais.position = (12.3456, 78.9101)
            >>> ais.encode_msg()
            b'!AIVDM,1,1,,A,13a:GQ0P0Qo=,0*5C'
        """
        lon, lat = self.position
        msg = {
            'mmsi': self.mmsi,
            'type': 1,
            'course': self.course,
            'speed': self.speed,
            'lon': lon,
            'lat': lat
        }
        return encode_dict(
            msg,
            talker_id='AIVDM'
        )[0]

    def send_ais_msg(
            self
    ) -> None:
        """
        Send AIS message to the socket.

        Returns:
            None

        Example:
            >>> ais = ShipAIS(SocketConfig())
            >>> ais.mmsi = 123456789
            >>> ais.course = 90.5
            >>> ais.speed = 10.2
            >>> ais.position = (12.3456, 78.9101)
            >>> ais.send_ais_msg()
        """
        self._socket.send_msg(
            self.encode_msg()
        )
