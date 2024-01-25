#!/usr/bin/env python3
"""The `user` model's module.
This module defines the `User` model,
representing a record from the `users` table.
Attributes:
    Base: A declarative base from SQLAlchemy for the model.
    User (class): Represents a record from the `users` table.

"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """Represents a record from the `users` table.

    Attributes:
        id (int): The primary key of the user record.
        email (str): The email of the user (unique).
        hashed_password (str): The hashed password of the user.
        session_id (str): The session ID associated with the user.
        reset_token (str): The reset token used for password reset.

    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
