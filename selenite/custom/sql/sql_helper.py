import warnings
from typing import Callable, List, Any

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


class SQLHelper:
    """
    SQL helper
    """

    def __init__(self, engine: Engine) -> None:

        self._engine = engine
        self._session = sessionmaker(bind=self._engine)
        self.session = self._session()

    def __del__(self) -> None:
        """
        Close session
        """
        self.session.close()

    def commit(self) -> None:
        """
        Commit session
        """
        self.session.commit()

    def rollback(self) -> None:
        """
        Rollback session
        """
        self.session.rollback()

    def with_safety_commit(
            self,
            fn: Callable,
            *args,
            **kwargs
    ) -> None:
        """
        Execute function with safety commit
        """
        try:
            fn(*args, **kwargs)
            self.commit()
        except SQLAlchemyError as e:
            self.rollback()
            warnings.warn(f'Error occurs: {e}')
            raise

    def add_data_to_table(
            self,
            data: List[object]
    ) -> None:
        """
        Add data to table
        """
        self.with_safety_commit(
            lambda _:
            self.session.add_all(_),
            data
        )

    def delete_all_data_in_table(
            self,
            table_name: Any
    ) -> None:
        """
        Delete all data in table
        """
        self.with_safety_commit(
            lambda _:
            self.session.query(_).delete(),
            table_name
        )
