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

# Database engine options
engine_opt = namedtuple('engine_opt', 'host port username password db_name')

# Database engine factory
factory: Dict[
    DbType,
    Callable[[Optional[engine_opt]], Engine]
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
    Database engine factory.
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
        """
        Initialize DBEngine object with database type and connection information.

        Args:
            db_type (DbType): Database type.
            host (str): Database host.
            port (int): Database port.
            username (str): Database username.
            password (str): Database password.
        """
        self._db_type = db_type
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._db_name: str = ''

    @property
    def _opt(self) -> engine_opt:
        """
        Database engine options.

        Returns:
            engine_opt: Database engine options.

        Example:
            >>> engine = DBEngine(
            ...     db_type='mysql',
            ...     host='localhost',
            ...     port=3306,
            ...     username='root',
            ...     password='password'
            ... )
            >>> engine._opt
            engine_opt(host='localhost', port=3306, username='root', password='password', db_name='')
        """
        return engine_opt(
            host=self._host,
            port=self._port,
            username=self._username,
            password=self._password,
            db_name=self._db_name
        )

    def engine(self, db_name: str) -> Engine:
        """
        Create a database engine.

        Args:
            db_name (str): Database name.

        Returns:
            Engine: Database engine.

        Example:
            >>> engine = DBEngine(
            ...     db_type='mysql',
            ...     host='localhost',
            ...     port=3306,
            ...     username='root',
            ...     password='password'
            ... )
            >>> engine.engine('test')
            Engine(mysql+pymysql://root:password@localhost:3306/test?charset=utf8)
        """
        self._db_name = db_name
        return factory[self._db_type](
            self._opt
        )
