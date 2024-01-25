#!/usr/bin/env python3
"""End-to-End (E2E) Integration Test for the Authentication Service.

This module contains functions to perform an E2E test on the authentication
service defined in `app.py`. It covers user registration, login, profile
management, session handling, password reset, and password update.

The test uses the requests module to interact with the web server and assert
expected outcomes.

Requirements:
    - Requests module must be installed. You can install it using:
      `pip install requests`

Usage:
    Run this script by executing `python main.py` in the terminal.

Note:
    Ensure that the authentication service (app.py) is running before running
    this script.

"""

import requests

# Constants for test data
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test user registration.

    Args:
        email (str): Email address for registration.
        password (str): Password for registration.

    """
    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    # Test user registration
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    # Test duplicate registration
    res = requests.post(url, data=body)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test logging in with a wrong password.

    Args:
        email (str): Email address for login.
        password (str): Incorrect password for login.

    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    # Test login with incorrect password
    res = requests.post(url, data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test logging in.

    Args:
        email (str): Email address for login.
        password (str): Password for login.

    Returns:
        str: Session ID obtained after successful login.

    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    # Test successful login
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test retrieving profile information while logged out.

    Raises:
        AssertionError: If the response status code is not 403.

    """
    url = "{}/profile".format(BASE_URL)
    # Test accessing profile while logged out
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test retrieving profile information while logged in.

    Args:
        session_id (str): Session ID obtained after login.

    Raises:
        AssertionError: If the response status code is not 200 or if
        "email" is not present in the response JSON.

    """
    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    # Test accessing profile while logged in
    res = requests.get(url, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """Test logging out of a session.

    Args:
        session_id (str): Session ID obtained after login.

    Raises:
        AssertionError: If the response status code is not 200 or if the
        "message" in the response JSON is not "Bienvenue".

    """
    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    # Test logging out
    res = requests.delete(url, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test requesting a password reset.

    Args:
        email (str): Email address for password reset.

    Returns:
        str: Reset token obtained after a successful reset request.

    Raises:
        AssertionError: If the response status code is not 200, if "email" is
        not present in the response JSON, or if "reset_token" is not present
        in the response JSON.

    """
    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    # Test password reset request
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating a user's password.

    Args:
        email (str): Email address for updating the password.
        reset_token (str): Reset token obtained after a successful reset request.
        new_password (str): New password for the user.

    Raises:
        AssertionError: If the response status code is not 200 or if the
        "message" in the response JSON is not "Password updated".

    """
    url = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    # Test updating password
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    # Run the complete E2E test
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
