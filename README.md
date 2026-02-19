# Geolocation API Service

Geolocation API Service — REST API built with FastAPI that automatically detects the client’s IP address and returns geolocation information using a third-party IP geolocation provider.

The API is designed with OpenAPI as the source of truth, clean architecture, retry handling, and production-ready structure.

![FastAPI](https://img.shields.io/badge/FastAPI-blue)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Docker](https://img.shields.io/badge/Docker-✓-blue)
![Ruff](https://img.shields.io/badge/Ruff-linting-blue)
![Mypy](https://img.shields.io/badge/Mypy-type--checking-blue)

---

# ⚙️ Tech Stack

**Backend**
* FastAPI
* Python 3.12
* Uvicorn (ASGI server)

**Architecture**
* Layered architecture (API → Service → External API)
* Pydantic models (request/response validation)
* OpenAPI-first design

**External Integration**
* IP-API (geolocation provider)
* Async HTTP client (httpx)

**Code Quality**
* Ruff (linting)
* Mypy (type checking)
* Pytest (testing)
* Pre-commit hooks

**DevOps**
* Docker
* Dockerfile
* Makefile
* UV (dependency management)

---

# 📁 Project Structure

```
src/
├── main.py                 # FastAPI application entrypoint
│
├── api/                    # API layer (routers, endpoints)
│   ├── router.py
│   └── v1/
│       ├── router.py
│       └── geolocation.py
│
├── services/               # Business logic layer
│   └── geolocation_service.py
│
├── schemas/                # Pydantic request/response models
│   ├── geo_response.py
│   └── ip_api_response.py
│
├── core/                   # Core utilities and configuration
│   ├── config.py
│   ├── logger.py
│   ├── constants.py
│   └── enums.py
│
logs/
└── logger.log              # Application logs

tests/                      # Unit and integration tests

scripts/
└── entrypoint.sh          # Docker entrypoint
```

---

# 📄 OpenAPI Documentation

Available at:

```
http://localhost:8000/docs
```

Alternative:

```
http://localhost:8000/redoc
```

or

```
http://localhost:8000/openapi.json
```

---

# ⚙️ Environment Setup

Create `.env` file from example:

```
cp .env.example .env
```

Example `.env`:

```
# Logger
LOG_LEVEL=INFO
LOGS_DIR=logs

# App
APP_NAME=IP Geolocation Service
APP_HOST=0.0.0.0
APP_PORT=8000
APP_RELOAD=True

# GeoAPI
IP_API_BASE_URL=http://ip-api.com/json
IP_API_TIMEOUT=10
IP_API_FIELDS=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,isp,org,as,asname,reverse,mobile,proxy,hosting,query
```

---

# 📦 Dependency Installation

Install UV if not installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies:

```bash
uv sync
```

Activate virtual environment:

```bash
source .venv/bin/activate
```

Install pre-commit hooks:

```bash
uv run pre-commit install
```

---

# ▶️ Running Locally

Run development server:

```bash
make run
```

Server will start at:

```
http://localhost:8000
```

Test endpoint:

```
http://localhost:8000/api/v1/geo
```

---

# 🐳 Running with Docker

Build image:

```bash
docker build -t geolocation-api .
```

Run container:

```bash
docker run -p 8000:8000 --env-file .env geolocation-api
```

---

# 🧪 Running Tests

```bash
make test
```

---

# 🧹 Linting and Type Checking

Run all checks:

```bash
make lint

make format
```

---

# 📝 Logging

Logs are stored in:

```
logs/logger.log
```

Includes:

* Request logs
* Errors
* External API failures

---

# 🧱 Architecture Overview

The project follows clean layered architecture:

```
Client
  ↓
API Layer (FastAPI routers)
  ↓
Service Layer (business logic)
  ↓
External API (IP-API)
  ↓
Response Schema
```

Benefits:

* Separation of concerns
* Testability
* Maintainability
* Scalability

---
