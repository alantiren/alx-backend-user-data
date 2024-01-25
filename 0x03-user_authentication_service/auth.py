#!/usr/bin/env python3
"""Auth module for handling user authentication logic.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a UUID.
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new Auth instance with a reference to the database
        (DB) object.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.
        Args:
            email (str): The email of the user.
            password (str): The password of the user.
        Returns:
            User: The registered User object.
        Raises:
            ValueError: If a user already exists with the provided email.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login credentials.
        Args:
            email (str): The email of the user.
            password (str): The password of the user.
        Returns:
            bool: True if the login credentials are valid, False otherwise.
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
        """
        Create a session for the user.
        Args:
            email (str): The email of the user.
        Returns:
            str: The generated session ID.
        Raises:
            NoResultFound: If the user with the provided email is not found.
        """
        user = self._db.find_user_by(email=email)
        session_id = str(uuid.uuid4())
        user.session_id = session_id
        self._db.commit()
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get the user corresponding to the session ID.
        Args:
            session_id (str): The session ID.
        Returns:
            User: The User object corresponding to the session ID,
            or None if not found.
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session for the user.
        Args:
            user_id (int): The ID of the user.
        Raises:
            NoResultFound: If the user with the provided ID is not found.
        """
        user = self._db.find_user_by(id=user_id)
        user.session_id = None
        self._db.commit()

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for the user.
        Args:
            email (str): The email of the user.
        Returns:
            str: The generated reset password token.
        Raises:
            NoResultFound: If the user with the provided email is not found.
        """
        user = self._db.find_user_by(email=email)
        reset_token = str(uuid.uuid4())
        user.reset_token = reset_token
        self._db.commit()
        return reset_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        """
        Update the user's password using a reset token.
        Args:
            reset_token (str): The reset password token.
            new_password (str): The new password.
        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = self._hash_password(new_password)
            user.reset_token = None
            self._db.commit()
        except NoResultFound:
            raise ValueError("Invalid reset token")

    def _hash_password(self, password: str) -> bytes:
        """
        Hash the password using bcrypt.
        Args:
            password (str): The password to hash.
        Returns:
            bytes: The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
