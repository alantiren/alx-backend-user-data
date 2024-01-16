# alx-backend-user-data

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Authentication Classes](#authentication-classes)
  - [Auth Class](#auth-class)
  - [BasicAuth Class](#basicauth-class)
- [Advanced Features](#advanced-features)
- [Endpoints](#endpoints)
- [Error Handlers](#error-handlers)
- [Contributors](#contributors)
- [License](#license)

## Introduction
The `alx-backend-user-data` project is a Flask API designed for managing user data with authentication capabilities. The API includes features such as error handling, authentication classes, and supports Basic Authentication.

## Features
- **Error Handlers:**
  - Unauthorized (HTTP 401)
  - Forbidden (HTTP 403)

- **Authentication Classes:**
  - Auth (base class)
  - BasicAuth (inherits from Auth)

- **Endpoints:**
  - `/api/v1/unauthorized` (Simulates 401 error)
  - `/api/v1/forbidden` (Simulates 403 error)

## Getting Started
Follow these instructions to set up and run the project locally.

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Pip (Python package installer)

### Installation
1. Clone the repository:

2. Navigate to the project directory:
   ```bash
   cd alx-backend-user-data
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. Start the server:
   ```bash
   API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
   ```

2. Test the API status:
   ```bash
   curl "http://0.0.0.0:5000/api/v1/status"
   ```

## Authentication Classes
### Auth Class
The base authentication class with methods for handling authentication.
- **Methods:**
  - `require_auth(path: str, excluded_paths: List[str]) -> bool`
  - `authorization_header(request=None) -> str`
  - `current_user(request=None) -> TypeVar('User')`

### BasicAuth Class (Inherits from Auth)
An authentication class that supports Basic Authentication.
- **Additional Methods:**
  - `extract_base64_authorization_header(authorization_header: str) -> str`
  - `decode_base64_authorization_header(base64_authorization_header: str) -> str`
  - `extract_user_credentials(decoded_base64_authorization_header) -> (str, str)`
  - `user_object_from_credentials(user_email: str, user_pwd: str) -> TypeVar('User')`
  - `current_user(request=None) -> TypeVar('User')`

## Advanced Features
- **Password with ":" Support:** BasicAuth now allows passwords containing ":".

- **Wildcard Paths:** `require_auth` now supports "*" at the end of excluded paths for flexible path matching.

## Endpoints
- `/api/v1/unauthorized`: Simulates a 401 error.
- `/api/v1/forbidden`: Simulates a 403 error.

## Error Handlers
- **Unauthorized (401):** JSON response: `{"error": "Unauthorized"}`
- **Forbidden (403):** JSON response: `{"error": "Forbidden"}`
