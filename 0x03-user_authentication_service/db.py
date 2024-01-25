#!/usr/bin/env python3
"""
DB module for handling database operations.
"""
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    """
    User class representing the 'users' table.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    hashed_password = Column(String(60), nullable=False)
    session_id = Column(String(36), nullable=True)
    reset_token = Column(String(36), nullable=True)


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
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

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
        user = self._session.query(User).filter_by(**kwargs).one()
        return user

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
        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid argument: {key}")
        self._session.commit()
