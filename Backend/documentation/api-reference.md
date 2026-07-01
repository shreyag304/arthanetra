# API Reference

This document provides a centralized reference for all API routes across the backend and frontend codebases, mapped and reconciled according to the `api-mapper` specification.

## Mapped Routes

| Method | Endpoint | Source (FE/BE/Both) | Payload/Params | Response | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `POST` | `/auth/login` | Both | **Body (`LoginRequest`):**<br>• `mobile` (string, 10 chars)<br>• `password` (string) | **`LoginResponse` (200 OK):**<br>• `message` (string)<br>• `user_id` (int)<br>• `name` (string)<br>• `mobile` (string)<br><br>**Errors:**<br>• `404 Not Found`<br>• `401 Unauthorized` | Authenticates a user using their 10-digit mobile number and password. Integrated with frontend client (`auth.js`). |
| `GET` | `/auth/register` | Both | **Query Params:**<br>• `mobile` (string, 10 chars) | **`CheckRegistrationResponse` (200 OK):**<br>• `mobile` (string)<br>• `is_registered` (bool)<br>• `available` (bool)<br>• `message` (string)<br><br>**Errors:**<br>• `422 Validation Error` | Checks whether a mobile number is already registered or available for signup. Integrated with frontend client (`checkRegistration` in `auth.js`). |
| `POST` | `/auth/register` | Both | **Body (`RegisterRequest`):**<br>• `mobile` (string, 10 chars)<br>• `password` (string)<br>• `name` (string, default "User")<br>• `email` (string, optional) | **`RegisterResponse` (200 OK):**<br>• `message` (string)<br>• `user_id` (int)<br>• `name` (string)<br>• `mobile` (string)<br><br>**Errors:**<br>• `400 Bad Request`<br>• `500 Internal Server Error` | Registers a new user with rollback support on error. Integrated with frontend client (`register` in `auth.js`). |
| `POST` | `/chat` | Both | **Body (`ChatRequest`):**<br>• `message` (string, required)<br>• `user_id` (int, optional)<br>• `conversation_id` (string, optional)<br>• `language` (string, optional) | **`ChatResponse` (200 OK):**<br>• `message` (string)<br>• `reply` (string)<br>• `user_id` (int, optional)<br>• `context` (object, optional)<br><br>**Errors:**<br>• `422 Validation Error` | Processes financial assistant chat messages and returns AI response along with conversational context. Integrated with frontend client (`sendMessage` in `chat.js`). |
| `GET` | `/profile` | Both | **Query / Path:**<br>• `user_id` (int, optional)<br>• `Authorization: Bearer <id>` | **`ProfileResponse` (200 OK):**<br>• `user_id` (int)<br>• `name` (string)<br>• `mobile` (string)<br>• `financial_health_score` (int)<br><br>**Errors:**<br>• `404 Not Found` | Retrieves user profile metadata and financial context. Integrated with frontend (`getProfile` in `profile.js`). |
| `PUT` | `/profile` | Both | **Body (`ProfileUpdateRequest`):**<br>• `name` (string, optional)<br>• `mobile` (string, optional)<br>• `goal` (string, optional) | **`ProfileResponse` (200 OK):**<br>Returns updated user profile.<br><br>**Errors:**<br>• `400 Bad Request`<br>• `404 Not Found` | Updates user profile and preferences with transaction rollback support. Integrated with frontend (`updateProfile` in `profile.js`). |

---

## Reconcile & Integration Status

1. **`/auth/login` (Reconciled - Fully Integrated)**
   - **Backend Definition:** [routes/auth.py](file:///home/abhijay/python/arthanetra/Backend/routes/auth.py#L43-L54) defines `POST /auth/login` accepting `LoginRequest` (`mobile`, `password`).
   - **Frontend Interaction:** [frontend/src/api/auth.js](file:///home/abhijay/python/arthanetra/frontend/src/api/auth.js#L3-L16) calls `client.post("/auth/login", { mobile, password })`.
   - **Status:** Payloads match exactly.

2. **`/auth/register` (Reconciled - Fully Integrated)**
   - **Backend Definition:** [routes/auth.py](file:///home/abhijay/python/arthanetra/Backend/routes/auth.py#L57-L99) defines `GET /auth/register` (status check) and `POST /auth/register` (user registration).
   - **Frontend Interaction:** [frontend/src/api/auth.js](file:///home/abhijay/python/arthanetra/frontend/src/api/auth.js#L18-L58) exports `checkRegistration(mobile)` calling `GET /auth/register?mobile=...` and `register(mobile, password, name, email)` calling `POST /auth/register`.
   - **Status:** Payloads and models reconciled against `models.User` (`mobile`, `password`, `name`). DB error handling wrapped in `try/except` with explicit `db.rollback()`.

3. **`/chat` (Reconciled - Fully Integrated)**
   - **Backend Definition:** [routes/chat.py](file:///home/abhijay/python/arthanetra/Backend/routes/chat.py#L22-L44) defines `POST /chat` accepting `ChatRequest` (`message`, `user_id`, `conversation_id`, `language`).
   - **Frontend Interaction:** [frontend/src/api/chat.js](file:///home/abhijay/python/arthanetra/frontend/src/api/chat.js#L3-L24) calls `client.post("/chat", requestData)`.
   - **Status:** Payloads and models reconciled. Route path updated from `/chat/chats` (`@router.post("/chats")`) to `POST /chat` (`@router.post("")`).

4. **`/profile` (Reconciled - Fully Integrated)**
   - **Backend Definition:** [routes/profile.py](file:///home/abhijay/python/arthanetra/Backend/routes/profile.py) defines `GET /profile`, `GET /profile/{user_id}`, `PUT /profile`, and `PUT /profile/{user_id}`.
   - **Frontend Interaction:** [frontend/src/api/profile.js](file:///home/abhijay/python/arthanetra/frontend/src/api/profile.js) exports `getProfile({ forceRefresh, userId })` calling `GET /profile` or `GET /profile/{userId}`, and `updateProfile(profileData)` calling `PUT /profile`.
   - **Status:** Models (`ProfileResponse`) output both `id` and `user_id` along with conversational context (`financial_health_score`, `persona`, `goal`) matching expectations in `AuthContext.jsx` and `Workspace.jsx`. DB update operations wrapped in `try/except` with explicit `db.rollback()`.



