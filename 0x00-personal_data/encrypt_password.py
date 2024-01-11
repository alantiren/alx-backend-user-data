#!/usr/bin/env python3
"""A module for encrypting passwords.
This module provides functions for hashing passwords and
validating hashed passwords.

"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using a random salt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted and hashed password.

    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a hashed password matches the given password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to check.

    Returns:
        bool: True if the password is valid, False otherwise.

    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

if __name__ == "__main__":
    pass
