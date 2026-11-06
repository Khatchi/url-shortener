# URL Shortener API

A URL shortening service built with **FastAPI, SQLAlchemy, and PostgreSQL**. It provides an API for creating short URLs, redirecting users to their original destinations, and optionally setting expiration dates.

## Features

- Create short URLs from valid HTTP and HTTPS URLs.
- Generate unique six-character Base62 short codes.
- Redirect users to their original URLs.
- Support optional URL expiration.
- Reject expiration dates that are in the past.
- Return `404 Not Found` for expired or nonexistent short URLs.
- Asynchronous database operations.
- Automated testing and database migrations.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.12+ |
| API Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy (Async) |
| Database Driver | asyncpg |
| Migrations | Alembic |
| Validation | Pydantic |
| Testing | pytest |
| Linting & Formatting | Ruff |
| Package Management | uv |

## Project Structure

```text
url-shortener/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── urls.py
│   ├── core/
│   │   ├── config.py
│   │   └── short_code.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   └── url.py
│   ├── repositories/
│   │   └── url.py
│   ├── schemas/
│   │   └── url.py
│   ├── services/
│   │   └── url.py
│   └── main.py
├── migrations/
├── tests/
├── alembic.ini
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- [uv](https://docs.astral.sh/uv/)

### 1. Clone the repository

```bash
git clone <repository-url>
cd url-shortener
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/url_shortener
TEST_DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/url_shortener_test
BASE_URL=http://localhost:8000
```

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection URL used by the application. Required. |
| `TEST_DATABASE_URL` | PostgreSQL connection URL used for testing. Optional. |
| `BASE_URL` | Base URL used when constructing shortened URLs. Defaults to `http://localhost:8000`. |

The application loads settings from `.env` using Pydantic Settings.

Keep credentials out of version control. Do not commit your `.env` file.

### 4. Run database migrations

```bash
uv run alembic upgrade head
```

### 5. Start the application

```bash
uv run uvicorn app.main:create_app --factory --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive documentation:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## API Reference

### Create a Short URL

`POST /api/v1/urls`

Creates a shortened URL.

**Request:**

```json
{
  "original_url": "https://example.com"
}
```

Expiration is optional:

```json
{
  "original_url": "https://example.com",
  "expires_at": "2027-12-31T23:59:59Z"
}
```

**Response: `201 Created`**

```json
{
  "original_url": "https://example.com/",
  "short_code": "aB123x",
  "short_url": "http://localhost:8000/aB123x"
}
```

**Validation:**

- Only valid HTTP and HTTPS URLs are accepted.
- Expiration timestamps must be timezone-aware.
- Expiration dates must be in the future.

### Redirect to Original URL

`GET /{short_code}`

Redirects the client to the original URL associated with the supplied short code.

| Status | Description |
|---|---|
| `307 Temporary Redirect` | Successfully redirects to the original URL. |
| `404 Not Found` | Short code does not exist or has expired. |

## URL Expiration

URLs can be created with or without an expiration date.

- URLs without an expiration date remain available.
- URLs with a future expiration date remain available until expiration.
- Expired URLs are treated as unavailable.
- Expiration is checked whenever a short URL is requested.

Expiration timestamps should use timezone-aware ISO 8601 formats.

## Testing

Run the complete test suite:

```bash
uv run pytest -v
```

Run linting:

```bash
uv run ruff check .
```

Check formatting:

```bash
uv run ruff format --check .
```

Verify database migration consistency:

```bash
uv run alembic check
```

## Database Migrations

Generate a migration after modifying database models:

```bash
uv run alembic revision --autogenerate -m "migration description"
```

Apply migrations:

```bash
uv run alembic upgrade head
```

Roll back the most recent migration:

```bash
uv run alembic downgrade -1
```

## Architecture

The application follows a layered architecture:

- **API layer:** Handles HTTP requests, responses, and input validation.
- **Service layer:** Contains business logic and application rules.
- **Repository layer:** Handles database operations.
- **Model layer:** Defines database entities.
- **Schema layer:** Defines request and response validation.

This separation promotes maintainability, testability, and clear responsibility boundaries.

## Current Scope

The current implementation covers URL creation, redirection, and expiration management.

Authentication, click analytics, custom aliases, rate limiting, and administrative functionality are not currently implemented.

## License

Add a license before distributing this project.
