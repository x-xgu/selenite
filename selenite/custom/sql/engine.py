from collections import namedtuple
from typing import Dict, Literal, Final, Callable, Optional

from sqlalchemy import create_engine, Engine

# Database types
DbType = Literal['mysql', 'oracle', 'postgresql', 'sqlite', 'db2']

mysql: Final[DbType] = 'mysql'
oracle: Final[DbType] = 'oracle'
postgresql: Final[DbType] = 'postgresql'
sqlite: Final[DbType] = 'sqlite'
db2: Final[DbType] = 'db2'

# Database engine config
DBConfig = namedtuple('DBConfig', 'host port username password db_name')

# Database engine factory
factory: Dict[
    DbType,
    Callable[[Optional[DBConfig]], Engine]
] = {
    mysql:
        lambda opts: create_engine(
            f'mysql+pymysql://{opts.username}:{opts.password}@{opts.host}:{opts.port}/{opts.db_name}?charset=utf8'
        ),
    oracle:
        lambda opts: create_engine(
            f'oracle+cx_oracle://{opts.username}:{opts.password}@{opts.host}:{opts.port}/{opts.db_name}'
        ),
    postgresql:
        lambda opts: create_engine(
            f'postgresql+psycopg2://{opts.username}:{opts.password}@{opts.host}:{opts.port}/{opts.db_name}'
        ),
    sqlite:
        lambda opts: create_engine(
            f'sqlite:///{opts.db_name}'
        ),
    db2:
        lambda opts: create_engine(
            f'db2+ibm_db://{opts.username}:{opts.password}@{opts.host}:{opts.port}/{opts.db_name}'
        )
}


class DBEngine:
    """
    Database engine
    """
    def __init__(
            self,
            *,
            db_type: DbType,
            host: str = None,
            port: int = None,
            username: str = None,
            password: str = None
    ) -> None:
        self._db_type = db_type
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    def engine(
            self,
            db_name: str
    ) -> Engine:
        """
        Create database engine
        """
        return factory[self._db_type](
            DBConfig(
                self._host,
                self._port,
                self._username,
                self._password,
                db_name
            )
        )
