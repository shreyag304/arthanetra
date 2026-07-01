# Backend API Routes Documentation

This document lists and details all API routes defined in the [`Backend/routes`](file:///home/abhijay/python/arthanetra/Backend/routes) directory and included in the main application ([`main.py`](file:///home/abhijay/python/arthanetra/Backend/main.py)).

---

## Summary Overview

| Router Prefix | Method | Endpoint | Description | Source File |
| :--- | :--- | :--- | :--- | :--- |
| `/auth` | `POST` | `/auth/login` | Authenticate user with mobile and password | [`auth.py`](file:///home/abhijay/python/arthanetra/Backend/routes/auth.py#L45-L56) |
| `/auth` | `GET` | `/auth/register` | Check registration availability of a mobile number | [`auth.py`](file:///home/abhijay/python/arthanetra/Backend/routes/auth.py#L60-L79) |
| `/auth` | `POST` | `/auth/register` | Register a new user account | [`auth.py`](file:///home/abhijay/python/arthanetra/Backend/routes/auth.py#L82-L106) |
| `/chat` | `POST` | `/chat` | Process AI chat conversation & return user context | [`chat.py`](file:///home/abhijay/python/arthanetra/Backend/routes/chat.py#L24-L47) |

---

## Detailed Route Specifications

### 1. Authentication Routes (`/auth`)

Defined in [`Backend/routes/auth.py`](file:///home/abhijay/python/arthanetra/Backend/routes/auth.py).

#### `POST /auth/login`
Authenticates a user using their 10-digit mobile number and password.

- **Request Body (`LoginRequest`):**
  ```json
  {
    "mobile": "9876543210",
    "password": "secretpassword"
  }
  ```
  - `mobile` (*string*, required): Exactly 10 characters.
  - `password` (*string*, required): User password.

- **Success Response (`200 OK` - `LoginResponse`):**
  ```json
  {
    "message": "Login successful",
    "user_id": 1,
    "name": "John Doe",
    "mobile": "9876543210"
  }
  ```

- **Error Responses:**
  - `404 Not Found`: `{ "detail": "User not found" }`
  - `401 Unauthorized`: `{ "detail": "Invalid credentials" }`
  - `422 Unprocessable Entity`: Request body validation failure.

---

#### `GET /auth/register`
Checks whether a 10-digit mobile number is already registered or available for sign-up.

- **Query Parameters:**
  - `mobile` (*string*, required): 10-digit mobile number to check. Example: `?mobile=9876543210`

- **Success Response (`200 OK` - `CheckRegistrationResponse`):**
  - **When available:**
    ```json
    {
      "mobile": "9876543210",
      "is_registered": false,
      "available": true,
      "message": "Mobile number is available for registration"
    }
    ```
  - **When already registered:**
    ```json
    {
      "mobile": "9876543210",
      "is_registered": true,
      "available": false,
      "message": "Mobile number is already registered"
    }
    ```

- **Error Responses:**
  - `422 Unprocessable Entity`: Missing or invalid mobile parameter format.

---

#### `POST /auth/register`
Registers a new user account and saves it to the database with rollback protection on error.

- **Request Body (`RegisterRequest`):**
  ```json
  {
    "mobile": "9876543210",
    "password": "securepassword",
    "name": "John Doe",
    "email": "john@example.com"
  }
  ```
  - `mobile` (*string*, required): Exactly 10 characters.
  - `password` (*string*, required): Minimum length 1.
  - `name` (*string*, optional): Defaults to `"User"`.
  - `email` (*string*, optional): Defaults to `null`.

- **Success Response (`200 OK` - `RegisterResponse`):**
  ```json
  {
    "message": "Registration successful",
    "user_id": 1,
    "name": "John Doe",
    "mobile": "9876543210"
  }
  ```

- **Error Responses:**
  - `400 Bad Request`: `{ "detail": "Mobile number already registered" }`
  - `500 Internal Server Error`: `{ "detail": "Failed to register user" }`
  - `422 Unprocessable Entity`: Request body validation failure.

---

### 2. Chat Routes (`/chat`)

Defined in [`Backend/routes/chat.py`](file:///home/abhijay/python/arthanetra/Backend/routes/chat.py).

#### `POST /chat`
Handles user interactions with ArthaNetra AI, providing localized replies and contextual financial metadata.

- **Request Body (`ChatRequest`):**
  ```json
  {
    "message": "How can I optimize my budget?",
    "user_id": 1,
    "conversation_id": "conv-12345",
    "language": "English"
  }
  ```
  - `message` (*string*, required): The chat message input by the user.
  - `user_id` (*integer*, optional): ID of the user sending the message.
  - `conversation_id` (*string*, optional): Unique session or conversation identifier.
  - `language` (*string*, optional): Defaults to `"English"`.

- **Success Response (`200 OK` - `ChatResponse`):**
  ```json
  {
    "message": "Chat processed successfully",
    "reply": "ArthaNetra AI (English): I received your message 'How can I optimize my budget?'. Assisting User ID #1.",
    "user_id": 1,
    "conversation_id": "conv-12345",
    "language": "English",
    "context": {
      "financial_health_score": 75,
      "persona": "Standard User",
      "income_type": "Variable",
      "language": "English",
      "goal": "Budget Optimization",
      "eligible_schemes": [
        "PM Jan Dhan Yojana",
        "Atal Pension Yojana"
      ]
    }
  }
  ```

- **Error Responses:**
  - `422 Unprocessable Entity`: Request body validation failure.
