# ArthaNetra AI

An intelligent, multi-agent financial guidance and fraud prevention platform tailored for Indian citizens and gig workers. ArthaNetra combines real-time financial health scoring, AI-driven contextual financial coaching, automated government scheme eligibility navigation, and instant scam detection.

---

## 1. Core Tech Stack

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Backend Runtime** | Python | 3.12+ | Asynchronous API runtime environment |
| **Frontend Runtime** | Node.js | 18.0+ / 20.0+ | JavaScript runtime for package resolution and bundling |
| **Backend Framework** | FastAPI | 0.138.1 | High-performance async REST & WebSocket API framework |
| **ASGI Server** | Uvicorn | 0.49.0 | Production ASGI server supporting WebSocket connections |
| **Multi-Agent Orchestration** | LangGraph | 0.2.0+ | State graph orchestration for cooperative specialized agents |
| **LLM Engine** | Google GenAI (Gemini) | 0.1.0+ | Multi-agent reasoning, coaching, and fraud risk analysis |
| **Frontend Framework** | React | 19.2.7 | Modern component-based user interface |
| **Frontend Bundler** | Vite | 8.1.0 | Ultra-fast ESM dev server and production bundler |
| **Database Engine** | SQLite (Default) / PostgreSQL 16 | - | Relational storage for users, chat context, and schemes |
| **ORM / ODM Layer** | SQLModel | 0.0.39 | Modern SQL abstraction combining SQLAlchemy & Pydantic |

---

## 2. Complete Dependency Mapping

### Backend Packages (`requirements.txt`)

#### API & ASGI Core
* `fastapi[standard]==0.138.1`: Core API framework (bundles `starlette`, `pydantic`, `httpx`, and OpenAPI generation).
* `uvicorn[standard]==0.49.0`: ASGI server engine with `websockets` and `uvloop` optimizations.

#### AI & Agentic System
* `langgraph>=0.2.0`: Graph-based state machine for orchestrating specialized agents (Financial Coach, Scam Detector, Scheme Navigator, Profiler).
* `google-genai>=0.1.0`: Google Gemini API client for high-speed, grounded reasoning.
* `pandas>=2.0.0`: Data structures and processing for financial analytics.

#### Database & Persistence
* `sqlmodel==0.0.39`: Declarative ORM providing table models and session lifecycle hooks.
* `psycopg2-binary==2.9.12`: Binary PostgreSQL driver for Python database connectivity (with seamless SQLite fallback).

#### Data Validation & Configuration
* `pydantic==2.13.4`: Schema enforcement for request/payload validation (`chat.py`, `auth.py`).
* `pydantic-settings==2.14.2`: Environment settings management.
* `email-validator==2.3.0`: Email syntax and domain validation for Pydantic field constraints.
* `python-dotenv==1.2.2`: Parses local `.env` variables into `os.environ`.

#### Security & Payload Handling
* `pyjwt==2.13.0`: JSON Web Token encoding/decoding for stateless authentication.
* `bcrypt==5.0.0`: Cryptographic hashing library for user credentials.
* `python-multipart==0.0.32`: Streaming parser for `multipart/form-data` and file uploads.
* `httpx`: Async HTTP client for external integrations and APIs.

---

### Frontend Packages (`package.json`)

#### Runtime Dependencies (`dependencies`)
* `react` (`^19.2.7`) & `react-dom` (`^19.2.7`): Core UI engine and DOM rendering layer.
* `react-router-dom` (`^7.18.0`): Client-side navigation and routing.
* `axios` (`^1.18.1`): HTTP client configured for REST interactions and WebSocket fallback execution.
* `react-icons` (`^5.6.0`): Vector icon system.

#### Build Tooling & Styling (`devDependencies`)
* `vite` (`^8.1.0`) & `@vitejs/plugin-react` (`^6.0.2`): Dev environment and build pipeline.
* `tailwindcss` (`^3.4.19`): Utility-first styling framework.
* `postcss` (`^8.5.15`) & `autoprefixer` (`^10.5.2`): CSS processing pipeline for Tailwind compilation.
* `eslint` (`^10.5.0`) & Plugins: Linting engine (`eslint-plugin-react-hooks`, `eslint-plugin-react-refresh`).

---

## 3. Environment & Infrastructure Requirements

### Network & Port Allocation

| Service | Host Port | Internal Port | Protocol | Description |
| :--- | :--- | :--- | :--- | :--- |
| **FastAPI Backend** | `8000` | `8000` | HTTP / WS | Core API server, docs (`/docs`), and WebSocket hub (`/ws/chat`) |
| **Vite Frontend Dev** | `5173` | `5173` | HTTP | Local application web interface |
| **PostgreSQL DB** (Optional) | `5434` | `5432` | TCP | Containerized DB instance (optional; SQLite fallback works out-of-the-box) |
| **Adminer UI** (Optional) | `8083` | `8080` | HTTP | Visual database administration console |

> [!NOTE]
> **Zero-Config SQLite Support:** If PostgreSQL is not running or credentials are not supplied, the backend automatically falls back to an embedded SQLite database (`Backend/arthanetra.db`) and auto-seeds all default schemes and tables. No external database setup is mandatory to start!

### Required Environment Variables

Create a `.env` file in the `Backend` directory by copying `.env.example`:

```ini
# Database Connection String
# Option 1: SQLite (Default zero-config setup)
DATABASE_URL=sqlite:///./arthanetra.db

# Option 2: PostgreSQL (Docker Compose setup)
# DATABASE_URL=postgresql://chaiaurcode:chaiaurcode@localhost:5434/chaiDB

# Google Gemini API Key (Required for live multi-agent AI features)
GOOGLE_API_KEY=your_gemini_api_key_here

# MeitY Bhashini API Configuration (Optional: for regional language voice & translation)
BHASHINI_USER_ID=your_bhashini_user_id
BHASHINI_ULCA_API_KEY=your_bhashini_ulca_api_key
BHASHINI_PIPELINE_ID=64392f96daac500b55c543cd
```

---

## 4. How to Run the Project (Step-by-Step)

### Prerequisites

Ensure you have the following installed on your machine:
* **Python**: Version 3.10 or higher (`python --version`)
* **Node.js**: Version 18.0 or higher (`node -v`)
* **Git**: (`git --version`)
* **Docker & Docker Compose** (Optional, only if using PostgreSQL instead of SQLite)

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/shreyag304/arthanetra.git
cd arthanetra
```

---

### Step 2: Setup and Run the Backend

1. **Navigate to the Backend directory:**
   ```bash
   cd Backend
   ```

2. **Create and activate a Python virtual environment:**

   * **On Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

   * **On Windows (CMD):**
     ```cmd
     python -m venv venv
     .\venv\Scripts\activate.bat
     ```

   * **On macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the `Backend` directory:
   ```bash
   # Windows (PowerShell)
   Copy-Item .env.example .env

   # Linux / macOS
   cp .env.example .env
   ```
   Open `.env` and add your Google Gemini API key:
   ```ini
   GOOGLE_API_KEY="your_api_key_here"
   ```
   *(Note: If left empty, ArthaNetra uses high-quality offline rule engines and heuristics so the system will never crash).*

5. **Start the FastAPI Backend Server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The backend will start and display:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Application startup complete.
   ```
   * Open your browser and visit:
     * **API Root:** [http://localhost:8000/](http://localhost:8000/)
     * **Interactive Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Step 3: Setup and Run the Frontend

Open a **new terminal window** and run the following commands:

1. **Navigate to the frontend directory:**
   ```bash
   cd arthanetra/frontend
   ```

2. **Install frontend dependencies:**
   ```bash
   npm install
   ```

3. **Start the Vite development server:**
   ```bash
   npm run dev
   ```

4. **Access the Application:**
   Open your browser and navigate to:
   * **Frontend App:** [http://localhost:5173](http://localhost:5173)

---

### Step 4 (Optional): Run with Docker Compose (PostgreSQL & Adminer)

If you prefer to run PostgreSQL in Docker rather than using the default SQLite mode:

1. In the directory containing `docker-compose.yaml`:
   ```bash
   docker compose up -d
   ```
2. Verify services:
   * **PostgreSQL:** Running on `localhost:5434`
   * **Adminer Web GUI:** Running on [http://localhost:8083](http://localhost:8083)
3. Set `DATABASE_URL` in `Backend/.env` to:
   ```ini
   DATABASE_URL=postgresql://chaiaurcode:chaiaurcode@localhost:5434/chaiDB
   ```

---

## 5. Multi-Agent System Architecture

ArthaNetra uses a stateful multi-agent system powered by **LangGraph** and **Gemini**:

```mermaid
flowchart TD
    UserQuery["User Input (Chat / Voice)"] --> Supervisor["LangGraph Supervisor / Router"]
    
    Supervisor -->|Fraud Risk / Loan App / Suspicious Offer| ScamAgent["Scam Detector Agent\n• Risk Score (0-100%)\n• Red Flags & RBI Regulations\n• Actionable Checklist"]
    Supervisor -->|Schemes / Subsidies / Eligibility| SchemeAgent["Gov Scheme Navigator\n• Database Lookup\n• Dynamic Eligibility Matching\n• Application Roadmap"]
    Supervisor -->|Budget / Savings / Debt / Score| CoachAgent["Financial Coach Agent\n• 50/30/20 & Emergency Fund\n• Step-by-Step Practical Advice\n• Proactive Financial Nudges"]
    
    ScamAgent --> ContextMemory["Profile & Context Memory\n(Financial Health Score & History)"]
    SchemeAgent --> ContextMemory
    CoachAgent --> ContextMemory
    
    ContextMemory --> Synthesis["Response Synthesis Engine\n(Friendly, Grounded, Formatted Markdown)"]
    Synthesis --> Output["User Output (WebSocket / REST)"]
```

* **Supervisor Router**: Classifies incoming user intent into `scam_detection`, `gov_schemes`, `financial_coach`, or `general_guidance`.
* **Scam Detector Agent**: Assesses suspicious SMS, fraudulent APK loan apps, lottery scams, and returns calculated risk levels (Safe, Caution, High Risk, Critical).
* **Government Scheme Navigator**: Matches user income, occupation, and demographics with pre-seeded central and state schemes (e.g., PM-SVANidhi, PM-KISAN, PMSYM, PMMY).
* **Financial Coach Agent**: Provides contextual budgeting, emergency buffer planning, and debt repayment prioritization.
* **Financial Health Score (FHS) Engine**: Computes comprehensive 0-100 scores across 4 pillars (Savings buffer, Debt-to-income, Credit score, Expense stability).

---

## 6. Key API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API status and service discovery |
| `POST` | `/auth/register` | Register a new user account |
| `POST` | `/auth/login` | Authenticate and obtain user session |
| `POST` | `/chat` | Multi-agent AI chat REST interface |
| `WS` | `/ws/chat` | Real-time bidirectional streaming AI chat |
| `POST` | `/api/fhs/calculate` | Calculate Financial Health Score (FHS) from raw profile metrics |
| `GET` | `/api/fhs/score/{user_id}` | Retrieve the latest FHS and pillar breakdown |
| `GET` | `/api/fhs/history/{user_id}` | Retrieve historical FHS scores and trend analysis |
| `GET` | `/api/profile/{user_id}` | Fetch persistent user financial context and last routing state |
| `PUT` | `/api/profile/{user_id}` | Update user financial profile |
