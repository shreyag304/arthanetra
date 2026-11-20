# ArthaNetra AI — Database Setup & Installation Guide

This comprehensive guide covers the architecture, setup, configuration, startup procedures, and troubleshooting steps for the **ArthaNetra AI PostgreSQL Database** running via Docker Compose.

---

## 1. Architecture Overview

ArthaNetra AI uses a containerized **PostgreSQL 16** relational database orchestrated via **Docker Compose**, alongside **Adminer** for lightweight web-based database administration.

```mermaid
graph TD
    subgraph Host Machine
        FastAPI[FastAPI Backend Application<br>localhost:8000]
        Browser[Web Browser<br>localhost:8083]
    end

    subgraph Docker Compose Network: dbmodel_default
        PG[PostgreSQL 16 Container<br>dbmodel-db-1<br>Internal Port: 5432]
        ADM[Adminer GUI Container<br>dbmodel-adminer-1<br>Internal Port: 8080]
    end

    subgraph Persistent Storage
        Vol[Local Volume Mount<br>./Backend/dbmodel/data/db]
    end

    FastAPI -->|TCP / localhost:5434| PG
    Browser -->|HTTP / localhost:8083| ADM
    ADM -->|Internal DNS / db:5432| PG
    PG --- Vol
```

### Container Specifications

| Service Name | Docker Image | Host Port | Internal Port | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **`db`** | `postgres:16` | `5434` | `5432` | Primary PostgreSQL database engine |
| **`adminer`** | `adminer` | `8083` | `8080` | Web-based visual database management client |

---

## 2. Prerequisites

Ensure your system has the following installed before starting:
* **Docker Engine** (v20.10+): [Install Guide](https://docs.docker.com/engine/install/)
* **Docker Compose CLI Plugin** (v2.0+): Verify with `docker compose version`
* **Python 3.12+**: For running the FastAPI backend server

---

## 3. Quick-Start Instructions

### Step 1: Navigate to the Database Module Directory
All Docker configurations reside inside the `Backend/dbmodel` folder:
```bash
cd Backend/dbmodel
```

### Step 2: Stop Any Conflicting or Ghost Containers
If older projects or duplicate containers are occupying port `5434` or `8083`, clean them up first:
```bash
# Stop and remove any ghost containers running from older directory names (e.g., dbmodels)
docker compose -p dbmodels down 2>/dev/null || true
docker compose down
```

### Step 3: Start the Database & Adminer Containers
Launch the containers in detached (`-d`) mode:
```bash
docker compose up -d
```

### Step 4: Verify Container Health & Ports
Check that both containers are running and actively bound to host ports:
```bash
docker ps
```
You should see output indicating:
* `0.0.0.0:5434->5432/tcp` for `dbmodel-db-1`
* `0.0.0.0:8083->8080/tcp` for `dbmodel-adminer-1`

---

## 4. Connection Credentials & Configuration

### A. Direct Connection Parameters
When connecting via terminal tools (`psql`), pgAdmin, DBeaver, or code:
* **Host**: `localhost` (or `127.0.0.1`)
* **Port**: `5434`
* **Database Name**: `chaiDB`
* **Username**: `chaiaurcode`
* **Password**: `chaiaurcode`

### B. SQLAlchemy / SQLModel Connection URL
The connection string used inside `Backend/dbmodel/Database.py` is formatted as follows:
```text
postgresql://chaiaurcode:chaiaurcode@localhost:5434/chaiDB
```

### C. Accessing Adminer Web UI
Once the containers are running, open your web browser and navigate to:
👉 **http://localhost:8083**

Fill in the login screen with:
* **System**: `PostgreSQL`
* **Server**: `db` *(Use the Docker service name, NOT localhost)*
* **Username**: `chaiaurcode`
* **Password**: `chaiaurcode`
* **Database**: `chaiDB`

---

## 5. Table Initialization & Schema Generation

ArthaNetra AI utilizes **SQLModel** (built on SQLAlchemy and Pydantic) to manage database schemas automatically.

When you start the FastAPI application server, the startup lifecycle hook (`lifespan`) executes `create_db_and_tables()`, which automatically creates all required tables (`users`, etc.) if they do not already exist.

To initialize or verify tables via code startup:
```bash
cd Backend
source .venv/bin/activate  # Or your active virtual environment
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
Look for terminal logs showing `CREATE TABLE users (...)` indicating successful database schema initialization.

---

## 6. Troubleshooting Guide

### Issue 1: Database Container Starts Without Port Mappings or Fails to Bind Port 5434
**Symptom**: `docker ps` shows `dbmodel-db-1` running, but the `PORTS` column is empty, or `docker compose up` returns `Bind for 0.0.0.0:5434 failed: port is already allocated`.

**Root Cause**: Another container (often from an old directory name like `dbmodels-db-1`) or a local PostgreSQL instance is running on port `5434`.

**Fix**:
```bash
# Find any Docker container occupying port 5434
docker ps --filter "publish=5434"

# Stop and remove all containers associated with duplicate project names
docker rm -f dbmodels-db-1 dbmodels-adminer-1 2>/dev/null

# Restart clean
cd Backend/dbmodel
docker compose up -d --force-recreate
```

---

### Issue 2: Permission Denied on `./data/db` Directory
**Symptom**: `open Backend/dbmodel/data/db: permission denied` when trying to inspect or clean local files.

**Root Cause**: PostgreSQL runs inside Docker under user ID `999` (`postgres`). When Docker mounts `./data/db`, it sets folder ownership to `999:999` (root/postgres on Linux).

**Fix**:
If you need to reset or wipe the local database files:
```bash
sudo rm -rf Backend/dbmodel/data/db
sudo rm -rf Backend/DBmodels  # Remove unused duplicate folders if present
cd Backend/dbmodel
docker compose up -d
```

---

### Issue 3: FastAPI Backend Says `Connection Refused` or `OperationalError`
**Symptom**: `sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost", port 5434 failed: Connection refused`

**Fix Checkpoints**:
1. Verify the container is up: `docker ps | grep postgres`
2. Ensure you are connecting to port **`5434`** (host port mapped in `docker-compose.yaml`), **not** default port `5432`.
3. If running FastAPI inside another Docker container on the same network, change host from `localhost` to `db` and port to `5432` (`postgresql://chaiaurcode:chaiaurcode@db:5432/chaiDB`).
