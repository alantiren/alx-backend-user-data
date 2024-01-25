#!/usr/bin/env python3
"""
DB module for handling database operations.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """
    DB class for handling database operations.
    """

    def __init__(self):
        """
        Initialize a new DB instance with a connection to the database.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self._engine)
        self._session = None

    @property
    def _session(self):
        """
        Memoized session object.
        """
        if self._session_instance is None:
            DBSession = sessionmaker(bind=self._engine)
            self._session_instance = DBSession()
        return self._session_instance

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The added User object.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided query arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            User: The found User object.

        Raises:
            NoResultFound: If no user is found.
        """
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user in the database based on the user ID.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments for updating user attributes.

        Raises:
            NoResultFound: If no user is found with the provided ID.
            ValueError: If an invalid argument is provided.
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update_source = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                update_source[getattr(User, key)] = value
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            update_source,
            synchronize_session=False,
        )
        self._session.commit()
