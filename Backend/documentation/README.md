# ArthaNetra AI — Backend Technical Documentation

Welcome to the centralized technical documentation for the **ArthaNetra AI Backend API**, structured and reconciled according to the specifications in `document-maker.md`.

Each module is documented with:
- **High-Level Overview:** Architectural purpose and business logic.
- **Interface Breakdown:** Request parameters, Pydantic data models, and HTTP response specifications.
- **Architecture & Flow:** Embedded **Mermaid.js diagrams** illustrating request flow pipelines and transaction boundaries.
- **Dependencies & Environment:** Package imports and database interactions.
- **Security & Limitations:** Known edge cases, transaction rollback safeguards, and identity resolution rules.

---

## Centralized Table of Contents

### 1. General API & Route Summary
- [API Reference](./api-reference.md) — Cross-stack reconciliation table mapping frontend client requests (`api/*.js`) to backend endpoints (`routes/*.py`).
- [Backend Routes Overview](./routes.md) — Summary overview of all API endpoints defined across the backend routers.

### 2. Route Modules (`routes/`)
- [Profile Router Documentation](./routes/profile.md) — Comprehensive documentation for [`routes/profile.py`](file:///home/abhijay/python/arthanetra/Backend/routes/profile.py) detailing `GET /profile` and `PUT /profile` endpoints, Pydantic schemas (`ProfileResponse`, `ProfileUpdateRequest`), identity resolution workflows, and transaction rollback sequence diagrams.
