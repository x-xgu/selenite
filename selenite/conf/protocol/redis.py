from typing import Union

import redis


class RedisConfig:
    """
    Redis Config
    """
    host: str = ''
    port: int = None
    db: int = None
    password: str = ''

    def send_redis_msg(
            self, name: str,
            msg: Union[str, int]
    ) -> None:
        """
        Send Redis Message
        """
        r = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password
        )
        r.set(name, msg)
