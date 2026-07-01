# ArthaNetra AI 

---

## 1. Core Tech Stack

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Backend Runtime** | Python | 3.12+ | Asynchronous API runtime environment |
| **Frontend Runtime** | Node.js | 18.0+ / 20.0+ | JavaScript runtime for package resolution and bundling |
| **Backend Framework** | FastAPI | 0.138.1 | High-performance async REST & WebSocket API framework |
| **ASGI Server** | Uvicorn | 0.49.0 | Production ASGI server supporting WebSocket connections |
| **Frontend Framework** | React | 19.2.7 | Component-based user interface library |
| **Frontend Bundler** | Vite | 8.1.0 | Ultra-fast ESM dev server and production bundler |
| **Database Engine** | PostgreSQL | 16 | Containerized relational database engine |
| **ORM / ODM Layer** | SQLModel | 0.0.39 | Modern SQL abstraction layer combining SQLAlchemy & Pydantic |
| **Database Driver** | Psycopg2 | 2.9.12 | Synchronous PostgreSQL DBAPI adapter for Python |

---

## 2. Complete Dependency Mapping

### Backend Packages (`requirements.txt`)

#### API & ASGI Core
* `fastapi[standard]==0.138.1`: Core API framework (bundles `starlette`, `pydantic`, `httpx`, and OpenAPI generation).
* `uvicorn[standard]==0.49.0`: ASGI server engine with `websockets` and `uvloop` optimizations.

#### Database & Persistence
* `sqlmodel==0.0.39`: Declarative ORM providing table models (`models.py`) and session lifecycle hooks.
* `psycopg2-binary==2.9.12`: Binary PostgreSQL driver for Python database connectivity.

#### Data Validation & Configuration
* `pydantic==2.13.4`: Schema enforcement for request/payload validation (`chat.py`, `auth.py`).
* `pydantic-settings==2.14.2`: Environment settings management.
* `email-validator==2.3.0`: Email syntax and domain validation for Pydantic field constraints.
* `python-dotenv==1.2.2`: Parses local `.env` variables into `os.environ`.

#### Security & Payload Handling
* `pyjwt==2.13.0`: JSON Web Token encoding/decoding for stateless authentication.
* `bcrypt==5.0.0`: Cryptographic hashing library for user credentials.
* `python-multipart==0.0.32`: Streaming parser for `multipart/form-data` and file uploads.
* `httpx` (included via fastapi standard): Async HTTP client used by `Bhashini_Service.py` to interact with external MeitY AI language pipelines.

---

### Frontend Packages (`package.json`)

#### Runtime Dependencies (`dependencies`)
* `react` (`^19.2.7`) & `react-dom` (`^19.2.7`): Core UI engine and DOM rendering layer.
* `react-router-dom` (`^7.18.0`): Client-side navigation and routing.
* `axios` (`^1.18.1`): HTTP client configured in `client.js` for REST interactions and WebSocket fallback execution.
* `react-icons` (`^5.6.0`): Vector icon system.

#### Build Tooling & Styling (`devDependencies`)
* `vite` (`^8.1.0`) & `@vitejs/plugin-react` (`^6.0.2`): Dev environment and build pipeline.
* `tailwindcss` (`^3.4.19`): Utility-first styling framework.
* `postcss` (`^8.5.15`) & `autoprefixer` (`^10.5.2`): CSS processing pipeline for Tailwind compilation.
* `eslint` (`^10.5.0`) & Plugins: Linting engine (`eslint-plugin-react-hooks`, `eslint-plugin-react-refresh`).
* `@types/react` (`^19.2.17`) & `@types/react-dom` (`^19.2.3`): Type declarations for editor intellisense.

---

## 3. Environment & Infrastructure Requirements

### Network & Port Allocation

| Service | Host Port | Internal Port | Protocol | Description |
| :--- | :--- | :--- | :--- | :--- |
| **FastAPI Backend** | `8000` | `8000` | HTTP / WS | Core API server and WebSocket chat hub (`/ws/chat`) |
| **Vite Frontend Dev** | `5173` | `5173` | HTTP | Local application web interface |
| **PostgreSQL DB** | `5434` | `5432` | TCP | Containerized DB instance (`dbmodel-db-1`) |
| **Adminer UI** | `8083` | `8080` | HTTP | Visual database administration console (`dbmodel-adminer-1`) |

> [!IMPORTANT]
> **Host Port Override Notice:** PostgreSQL is explicitly mapped to host port `5434` in `docker-compose.yaml` to avoid conflicts with existing local PostgreSQL installations on default port `5432`.

### Required Environment Variables

#### Backend Environment Variables (`Backend/.env`)

```ini
# Database Connection String
# NOTE: Ensure this matches your Docker Compose configuration or external cluster
DATABASE_URL="postgresql://chaiaurcode:chaiaurcode@localhost:5434/chaiDB"

# Google Generative AI API Key
GOOGLE_API_KEY="your_google_genai_api_key_here"

# MeitY Bhashini API Configuration (Required for Multilingual ASR/NMT/TTS)
BHASHINI_USER_ID="your_udyat_user_id"
BHASHINI_ULCA_API_KEY="your_udyat_ulca_api_key"
BHASHINI_PIPELINE_ID="64392f96daac500b55c543cd"
