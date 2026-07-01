# ArthaNetra Project Context

## Project Overview
ArthaNetra is a full-stack web application consisting of a FastAPI backend and a React (Vite) frontend. The platform focuses on providing financial assistance, budgeting optimization, and checking eligibility for government financial schemes (like PM Jan Dhan Yojana, PM-KISAN, etc.) through an AI chat interface.

## Backend Context (`/Backend`)
- **Framework:** FastAPI with Uvicorn server.
- **Database:** SQLModel (ORM), using PostgreSQL (`psycopg2-binary`).
- **Dependencies:** `fastapi`, `uvicorn`, `sqlmodel`, `pydantic`, `pyjwt`, `bcrypt`, `python-dotenv`.
- **Key Modules & Structure:**
  - `main.py`: Entry point for the FastAPI application. Sets up CORS for frontend integration and includes routers. Automatically initializes database tables on startup.
  - `routes/auth.py`: Handles user authentication.
    - `POST /auth/login`: Accepts 10-digit mobile number and password. Returns user ID, name, and mobile.
    - `POST /auth/register`: Creates a new user with mobile, password, optional name/email.
    - `GET /auth/register`: Checks if a given mobile number is already registered.
  - `routes/chat.py`: Handles the AI chatbot interactions.
    - `POST /chat`: REST endpoint for chat messages.
    - `WS /ws` & `WS /ws/chat`: WebSocket endpoints for real-time chat.
    - Current AI is mock-based, responding to keywords like "loan", "scam", "budget", "save", "scheme", "health score". It returns a mock financial context (health score, income type, eligible schemes).
  - `dbmodel/`: Contains `Database.py` (connection and setup) and `models.py` (SQLModel schemas, e.g., `User`).

## Frontend Context (`/frontend`)
- **Framework:** React 19 built with Vite.
- **Styling:** Tailwind CSS and PostCSS.
- **Routing:** `react-router-dom` for navigation.
- **Dependencies:** `axios` (API calls), `react-icons`, `@vitejs/plugin-react`.
- **Key Structure:**
  - `src/App.jsx` & `src/main.jsx`: Main entry points and layout.
  - `src/pages/`: Contains primary views like `Login.jsx` and `Workspace.jsx` (which likely hosts the chat interface).
  - `src/components/`: Modular components structured into `auth`, `chat`, `context`, and `shared`.
  - `src/api/`: Likely contains Axios configurations and API calling functions.
  - `src/index.css`: Global styles including Tailwind directives.

## Running the Project
**Backend:**
```bash
cd Backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```
