# User Authentication Service

The User Authentication Service is a simple web service that provides user registration, authentication, and session management capabilities. It is implemented using Flask, SQLAlchemy, and Bcrypt for password hashing.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project aims to provide a foundation for building secure user authentication systems. It handles user registration, login, logout, and password reset functionalities. The service uses Flask, a lightweight web framework, SQLAlchemy for database interactions, and Bcrypt for secure password hashing.

## Features

- **User Registration**: Allow users to create accounts by providing a valid email and password.
- **User Authentication**: Securely authenticate users using hashed passwords and session management.
- **Session Management**: Implement user sessions to keep users logged in across requests.
- **Password Reset**: Enable users to reset their passwords securely through a token-based mechanism.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/alantiren/alx-backend-user-data.git
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask App:**

   ```bash
   python app.py
   ```

## Usage

The User Authentication Service exposes several endpoints for user management. Below are the primary endpoints and their functionalities.

## Endpoints

### 1. Register a New User

- **Endpoint:** `POST /users`
- **Description:** Register a new user by providing a unique email and a secure password.
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password"
  }
  ```
- **Response:**
  ```json
  {
    "email": "user@example.com",
    "message": "user created"
  }
  ```

### 2. Log In and Create a Session

- **Endpoint:** `POST /sessions`
- **Description:** Log in and create a session for the user.
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password"
  }
  ```
- **Response:**
  ```json
  {
    "email": "user@example.com",
    "message": "logged in"
  }
  ```

### 3. Log Out and Destroy the Session

- **Endpoint:** `DELETE /sessions`
- **Description:** Log out and destroy the user's session.
- **Response:**
  ```json
  {
    "message": "logged out"
  }
  ```

### 4. Get User Profile

- **Endpoint:** `GET /profile`
- **Description:** Get the user's profile information.
- **Response:**
  ```json
  {
    "email": "user@example.com"
  }
  ```

### 5. Request Password Reset Token

- **Endpoint:** `POST /reset_password`
- **Description:** Request a password reset token.
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response:**
  ```json
  {
    "email": "user@example.com",
    "reset_token": "a4d19e2f-88f1-4bc4-89f7-7d39b98a3d44"
  }
  ```

### 6. Update Password using Reset Token

- **Endpoint:** `PUT /reset_password`
- **Description:** Update the password using the reset token.
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "reset_token": "a4d19e2f-88f1-4bc4-89f7-7d39b98a3d44",
    "new_password": "new_secure_password"
  }
  ```
- **Response:**
  ```json
  {
    "email": "user@example.com",
    "message": "password updated"
  }
  ```

## Testing

The `tests` directory contains integration tests to verify the functionality of the service. Run the tests using:

```bash
python main.py
```

## Contributing

Feel free to contribute to this project. Fork the repository, make your changes, and submit a pull request.
