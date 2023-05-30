from typing import Any, Tuple

from loguru import logger
from pyais import encode_dict

from selenite.conf.protocol.socket import SocketConfig

LOG_TAG = 'MOCK_AIS'


class ShipAIS:
    """
    Mock AIS ship
    """

    def __init__(self, config: SocketConfig) -> None:
        self._socket: SocketConfig = config

        # MMIS: Maritime Mobile Service Identity
        self.mmsi: int = 0
        # Name: Name of the vessel
        self.name: str = ''
        # Course: Course over ground in degrees
        self.course: float = 0
        # Speed: Speed over ground in knots
        self.speed: float = 0
        # Position: Position of the vessel
        self.position: Tuple[float, float] = (0, 0)

    def encode_msg(self) -> Any:
        """
        Encode AIS message
        """
        lon, lat = self.position
        msg = {'mmsi': self.mmsi, 'shipname': self.name, 'type': 1, 'course': self.course, 'speed': self.speed, 'lon': lon, 'lat': lat}
        logger.debug(f'[{LOG_TAG}] Encode AIS message: {msg}')
        return encode_dict(
            msg,
            talker_id='AIVDM'
        )[0]

    def send_ais_msg(self) -> None:
        """
        Send AIS message
        """
        logger.debug(f'[{LOG_TAG}] Send AIS message')
        self._socket.send_msg(self.encode_msg())
