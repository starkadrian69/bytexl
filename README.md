# CivicTrace

CivicTrace is a civic issue intelligence and accountability platform. It connects on-the-ground evidence with responsible authorities using AI perception and GIS determination.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 24+
- [Docker Compose](https://docs.docker.com/compose/) v2
- Python 3.11+ (for local development outside Docker)
- Node.js 20+ (for the frontend)

## Quick Start (Docker — Recommended)

```bash
# 1. Clone the repository
git clone <repo-url>
cd civictrace

# 2. Copy the environment template
cp .env.example .env
# Edit .env if you need to override any defaults (see Configuration section below)

# 3. Start the full development stack
docker compose up --build

# 4. Verify the API is healthy
curl http://localhost:8000/health
# Expected: {"status":"ok","service":"civictrace-api"}

# 5. Apply database migrations (separate terminal, or after containers are up)
docker compose exec api alembic upgrade head
```

The stack starts:
| Service   | URL                        |
|-----------|----------------------------|
| API       | http://localhost:8000      |
| API Docs  | http://localhost:8000/docs |
| DB        | localhost:5432             |

## Local Development (Without Docker)

```bash
cd apps/api

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp ../../.env.example .env

# Run database migrations
alembic upgrade head

# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Running Tests

```bash
cd apps/api

# Run the full test suite
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run a specific test file
pytest tests/test_health.py -v
```

## Configuration

All configuration is driven by environment variables. See [.env.example](.env.example) for the full list.

| Variable                | Default                                      | Description                              |
|-------------------------|----------------------------------------------|------------------------------------------|
| `ENVIRONMENT`           | `development`                                | `development`, `staging`, or `production`|
| `LOG_LEVEL`             | `INFO`                                       | Logging verbosity                        |
| `DATABASE_URL`          | `postgresql+asyncpg://...`                   | Full async DSN for PostgreSQL/PostGIS    |
| `ALLOWED_ORIGINS`       | `http://localhost:3000`                      | Comma-separated CORS origins             |
| `SECRET_KEY`            | *(required in production)*                   | JWT signing secret                       |
| `GEMINI_API_KEY`        | *(empty)*                                    | Google Gemini API key for AI Perception  |

## Project Structure

```
civictrace/
├── apps/
│   ├── api/                  # FastAPI backend
│   │   ├── app/
│   │   │   ├── api/          # Route handlers and dependencies
│   │   │   ├── core/         # Config, logging, error handling, security
│   │   │   ├── models/       # SQLAlchemy ORM models
│   │   │   ├── schemas/      # Pydantic request/response schemas
│   │   │   ├── repositories/ # Data access layer
│   │   │   ├── services/     # Domain service layer
│   │   │   └── main.py       # Application factory
│   │   ├── alembic/          # Database migrations
│   │   ├── tests/            # Test suite
│   │   └── requirements.txt
│   └── web/                  # TypeScript frontend (upcoming)
├── packages/shared/          # Shared types and constants
├── data/                     # Seed data and GIS layers
├── docs/                     # Architecture, ADRs, and contracts
├── infra/                    # Docker and deployment configs
└── scripts/                  # Utility scripts
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full system design.

Key principles:
- **AI is for perception only** — not accountability decisions
- **GIS determines jurisdiction** — point-in-polygon authority assignment
- **Deterministic fusion** — explainable incident grouping
- **Modular monolith** — clean service boundaries, simple deployment

## CivicTrace Data Foundation (Phases 1–3D)

> [!IMPORTANT]
> **Freeze & Grounding Notice**:
> - **Phase 1–3D data foundation is frozen for Phase 4 integration.**
> - **The data foundation contains synthetic evaluation records and documented real-world grounding references. Synthetic records must not be interpreted as real citizen complaints or official government records.**
> - All SLA targets in `data/authority/sla_rules.csv` are `CIVICTRACE_PILOT_RULE` hackathon demonstration targets, not statutory government commitments.

```
CivicTrace Data Foundation
        ↓
Phase 1 — Authority Foundation (6 authorities, 28 services, 4 conflicts)
Phase 2 — GIS / Jurisdiction Foundation (110 wards, 8 zones, 105 polygons)
Phase 3A — Physical Asset Foundation (39 assets across 6 categories)
Phase 3B — Incident Foundation (20 seed incidents across 4 languages)
Phase 3C — Evidence Foundation (13 records across 8 evidence chains)
Phase 3D — Duplicate Benchmark (26 synthetic records across 7 clusters)
SLA Configuration (21 CivicTrace pilot rules covering all 18 categories)
        ↓
Golden Demo Expectations (10 end-to-end benchmark scenarios)
        ↓
Phase 4 Prototype Integration (docs/phase4_data_contract.md)
```

### Data Foundation Scope vs. Hackathon Demo Scope

| Dimension | Full Data Foundation Scope | Hackathon Primary Demo Scope |
| :--- | :--- | :--- |
| **Authorities** | 6 statutory authorities (`AUTH-LMC`, `AUTH-UPPWD`, `AUTH-MVVNL`, `AUTH-LKO-JALSANSTHAN`, `AUTH-UPJN-URBAN`, `AUTH-LDA`) | Focused subset: LMC, UP PWD, MVVNL, Jal Sansthan |
| **Issue Domains** | 18 controlled issue categories | 4 core domains: 1) Road damage / pothole, 2) Drainage / waterlogging, 3) Garbage / sanitation, 4) Streetlight / electrical |
| **Jurisdictions** | 110 administrative wards across 8 zones | Focused test wards (e.g. Ward 34 Hazratganj, Ward 109 Aliganj, Ward 26 Aishbagh, Ward 80 Indira Nagar) |
| **Physical Assets** | 39 assets (Roads, Drains, Pipelines, Sewers, Streetlights, Electrical Poles) | Representative demo assets (`AST-ROAD-001/002`, `AST-DRN-003`, `AST-STL-001/004`, `AST-ELE-003`) |
| **Incidents** | 20 incidents (`CT-INC-001` through `CT-INC-020`) | Golden Demo Cases (`GD-CASE-01` through `GD-CASE-10`) |
| **Evidence** | 13 records (8 chains) covering before/after/contradictions | Key demo chains (`CHAIN-001`, `CHAIN-002`, `CHAIN-005`, `CHAIN-006`, `CHAIN-007`) |
| **Duplicates** | 26 benchmark cases across 7 candidate clusters | Primary clusters (`CLUSTER-001` multilingual, `CLUSTER-007` negative controls) |
| **SLA Rules** | 21 pilot rules across all 18 Phase 1 categories | Demo pilot rules (`SLA-RULE-001`, `002`, `010`, `013`, `015`, `016`, `018`) |

*Note: The broader categories are preserved for reference, routing, validation, benchmarking, and future expansion. They must not be deleted.*

### Data Validation Suite

All foundational datasets can be validated locally using the 7 included verification scripts:

```bash
# Phase 1: Authority & Lexicon Validation
python scripts/validate_lexicon.py

# Phase 2: GIS & Administrative Boundaries Validation
python scripts/validate_gis.py

# Phase 3A: Physical Asset Ownership Validation
python scripts/validate_assets.py

# Phase 3B: Seed Incidents Validation
python scripts/validate_incidents.py

# Phase 3C: Resolution Evidence Validation
python scripts/validate_evidence.py

# Phase 3D: Synthetic Duplicate Benchmark Validation
python scripts/validate_duplicates.py

# SLA & Escalation Configuration Validation
python scripts/validate_sla.py
```

