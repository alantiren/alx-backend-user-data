#!/usr/bin/env python3
"""
Main application module for the user authentication service.
"""
from flask import Flask, request, jsonify, abort, make_response
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def welcome():
    """
    Welcome route.

    Returns:
        jsonify: JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """
    Endpoint to register a new user.

    Returns:
        jsonify: JSON response with user details if registration is successful.
    """
    try:
        email = request.form['email']
        password = request.form['password']
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError as err:
        return jsonify({"message": str(err)}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    Endpoint to log in a user.

    Returns:
        jsonify: JSON response with user details and session ID if login is successful.
    """
    try:
        email = request.form['email']
        password = request.form['password']
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            return jsonify({"email": email, "message": "logged in"}), 200, {'Set-Cookie': f'session_id={session_id}'}
        else:
            abort(401)
    except (NoResultFound, InvalidRequestError):
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Endpoint to log out a user.

    Returns:
        jsonify: JSON response with a logout message.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return jsonify({"message": "logged out"}), 200
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def get_profile():
    """
    Endpoint to get the user profile.

    Returns:
        jsonify: JSON response with user's email if the session is valid.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def request_reset_password():
    """
    Endpoint to request a reset password token.

    Returns:
        jsonify: JSON response with user's email and reset token if the email is valid.
    """
    try:
        email = request.form['email']
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except (NoResultFound, InvalidRequestError):
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Endpoint to update the user password using a reset token.

    Returns:
        jsonify: JSON response with user's email and a password update message if successful.
    """
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
