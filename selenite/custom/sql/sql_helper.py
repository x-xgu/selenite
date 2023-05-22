import warnings
from typing import Callable

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


class SQLHelper:
    """
    Helper class for SQL operations
    """

    def __init__(
            self,
            engine: Engine
    ) -> None:
        """
        Initialize SQLHelper

        Args:
            engine (Engine): SQL engine
        """
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
        Commit changes

        Returns:
            None
        """
        self.session.commit()

    def rollback(self) -> None:
        """
        Rollback changes

        Returns:
            None
        """
        self.session.rollback()

    def with_safety_commit(self, fn: Callable, *args, **kwargs):
        """
        Commit changes with safety

        Args:
            fn (Callable): function to execute
            *args: args for fn
            **kwargs: kwargs for fn

        Returns:
            None

        Examples:
            >>> sql_helper = SQLHelper(engine)
            >>> def fn():
            >>>     sql_helper.session.query(
            >>>         ORMClass
            >>>     ).filter(
            >>>         ORMClass.date == date
            >>>     ).delete()
            >>> sql_helper.with_safety_commit(
            >>>     fn
            >>> )

        Raises:
            SQLAlchemyError: if error occurs, rollback changes
        """
        try:
            fn(*args, **kwargs)
            self.commit()
        except SQLAlchemyError as e:
            self.rollback()
            warnings.warn(f'Error occurs: {e}')
            raise
