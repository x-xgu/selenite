import warnings
from typing import Callable

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


class SQLHelper:

    def __init__(self, engine: Engine) -> None:

        self._engine = engine
        self._session = sessionmaker(bind=self._engine)
        self.session = self._session()

    def __del__(self) -> None:
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def with_safety_commit(
            self,
            fn: Callable,
            *args,
            **kwargs
    ) -> None:
        try:
            fn(*args, **kwargs)
            self.commit()
        except SQLAlchemyError as e:
            self.rollback()
            warnings.warn(f'Error occurs: {e}')
            raise