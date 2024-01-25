#!/usr/bin/env python3
"""A module for authentication-related routines.

This module provides functionality for user authentication, including
registering users, validating logins, creating and destroying sessions,
generating password reset tokens, and updating user passwords.

Classes and Functions:
    - _hash_password: Hashes a password using bcrypt.
    - _generate_uuid: Generates a UUID.
    - Auth: Auth class for interacting with the authentication database.

"""

import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.
    Args:
        password (str): The plaintext password.
    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a UUID.
    Returns:
        str: The generated UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    Attributes:
        _db (DB): An instance of the database interface.
    Methods:
        - register_user: Adds a new user to the database.
        - valid_login: Checks if a user's login details are valid.
        - create_session: Creates a new session for a user.
        - get_user_from_session_id: Retrieves a user based on given session ID
        - destroy_session: Destroys a session associated with a given user.
        - get_reset_password_token: Generates a password reset token for a user
        - update_password: Updates user's password given the user's reset token

    """

    def __init__(self):
        """Initializes a new Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a new user to the database.
        Args:
            email (str): The user's email.
            password (str): The user's plaintext password.
        Returns:
            User: The newly registered user.
        Raises:
            ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a user's login details are valid.
        Args:
            email (str): The user's email.
            password (str): The user's plaintext password.
        Returns:
            bool: True if the login details are valid, False otherwise.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Creates a new session for a user.
        Args:
            email (str): The user's email.
        Returns:
            str: The generated session ID.

        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user based on a given session ID.
        Args:
            session_id (str): The session ID.
        Returns:
            Union[User, None]: The user if found, None otherwise.

        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session associated with a given user.
        Args:
            user_id (int): The ID of the user.

        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for a user.
        Args:
            email (str): The user's email.
        Returns:
            str: The generated reset token.
        Raises:
            ValueError: If the user does not exist.

        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password given the user's reset token.
        Args:
            reset_token (str): The user's reset token.
            password (str): The new plaintext password.
        Raises:
            ValueError: If the user does not exist.

        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
