# GolfCoach Pro - Backend API

AI-powered golf swing analysis backend built with FastAPI.

## Overview

This is the backend API for GolfCoach Pro, providing:

- **User Authentication**: JWT-based authentication with access and refresh tokens
- **User Management**: User profiles with golf-specific data
- **Health Checks**: Database and Redis connectivity monitoring
- **RESTful API**: Following OpenAPI 3.0 specifications
- **Database Migrations**: Alembic for schema management
- **Type Safety**: Full type hints with Pydantic validation

## Tech Stack

- **Framework**: FastAPI 0.109+
- **Database**: PostgreSQL 15+ with SQLAlchemy 2.0
- **Caching**: Redis 7+
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Migrations**: Alembic
- **Testing**: pytest with coverage
- **Code Quality**: Black, Ruff, mypy

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── users.py         # User management endpoints
│   │       └── health.py        # Health check endpoints
│   ├── core/
│   │   ├── config.py           # Configuration management
│   │   ├── security.py         # JWT & password hashing
│   │   ├── database.py         # Database connection
│   │   └── dependencies.py     # FastAPI dependencies
│   ├── models/
│   │   └── user.py             # SQLAlchemy models
│   ├── schemas/
│   │   └── user.py             # Pydantic schemas
│   ├── services/
│   │   └── user_service.py     # Business logic
│   └── main.py                 # FastAPI application
├── alembic/
│   ├── versions/               # Migration files
│   └── env.py                  # Alembic configuration
├── tests/
│   ├── conftest.py             # Test fixtures
│   ├── test_auth.py            # Authentication tests
│   ├── test_users.py           # User endpoint tests
│   └── test_health.py          # Health check tests
├── Dockerfile
├── pyproject.toml              # Poetry dependencies
└── alembic.ini                 # Alembic configuration
```

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+ (optional for development)
- Poetry (for dependency management)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd golfcoach-pro/backend
   ```

2. **Install dependencies**:
   ```bash
   # Install Poetry if not already installed
   curl -sSL https://install.python-poetry.org | python3 -

   # Install project dependencies
   poetry install
   ```

3. **Set up environment variables**:
   ```bash
   cp ../.env.example ../.env
   # Edit .env with your configuration
   ```

4. **Start infrastructure services** (from project root):
   ```bash
   docker-compose up -d postgres redis
   ```

5. **Run database migrations**:
   ```bash
   poetry run alembic upgrade head
   ```

6. **Start the development server**:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

### Running with Docker Compose

From the project root directory:

```bash
# Start all services including backend
docker-compose up backend

# Or build and start
docker-compose up --build backend
```

### Database Migrations

```bash
# Create a new migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Rollback one migration
poetry run alembic downgrade -1

# Show migration history
poetry run alembic history
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_auth.py

# Run specific test
poetry run pytest tests/test_auth.py::test_login_success

# Run with verbose output
poetry run pytest -v
```

### Code Quality

```bash
# Format code with Black
poetry run black app tests

# Lint with Ruff
poetry run ruff check app tests

# Type check with mypy
poetry run mypy app

# Run all checks
poetry run black app tests && poetry run ruff check app tests && poetry run mypy app
```

## API Documentation

### Authentication Endpoints

#### Register
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

#### Login
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

#### Refresh Token
```bash
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### User Endpoints

#### Get Current User
```bash
GET /api/v1/users/me
Authorization: Bearer <access_token>
```

#### Update User Profile
```bash
PATCH /api/v1/users/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "John Smith",
  "handicap": 12.5,
  "profile": {
    "primary_miss": "slice",
    "goals": ["Break 80", "Fix driver slice"]
  }
}
```

### Health Check Endpoints

```bash
# Simple health check
GET /health

# Detailed health check
GET /api/v1/health

# Database health check
GET /api/v1/health/db

# Redis health check
GET /api/v1/health/redis

# Full health check
GET /api/v1/health/full
```

## Environment Variables

Key environment variables (see `.env.example` for complete list):

```env
# Application
APP_ENV=development
DEBUG=true

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=golfcoach
POSTGRES_USER=golfcoach_user
POSTGRES_PASSWORD=your-password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# AI Services
ANTHROPIC_API_KEY=your-anthropic-api-key
```

## Deployment

### Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t golfcoach-backend:latest .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     -p 8000:8000 \
     -e DATABASE_URL=postgresql://... \
     -e REDIS_URL=redis://... \
     -e SECRET_KEY=... \
     golfcoach-backend:latest
   ```

### Production Considerations

- Use a strong `SECRET_KEY` (generate with `openssl rand -hex 32`)
- Set `DEBUG=false` in production
- Use environment-specific configuration
- Enable HTTPS (`HTTPS_ONLY=true`)
- Configure proper CORS origins
- Set up monitoring and logging
- Use a process manager (e.g., supervisord)
- Enable database connection pooling
- Set up database backups

## Testing

The backend includes comprehensive tests:

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints
- **Fixtures**: Reusable test data and setup

Test coverage target: 80%+

## API Versioning

The API follows semantic versioning:
- Current version: v1 (`/api/v1/*`)
- Breaking changes will be released as new versions (v2, v3, etc.)
- Old versions maintained for 6 months after new version release

## Contributing

1. Follow the code style (Black, Ruff)
2. Add type hints to all functions
3. Write tests for new features
4. Update documentation
5. Create meaningful commit messages

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection
psql -h localhost -U golfcoach_user -d golfcoach

# Reset database
docker-compose down -v
docker-compose up -d postgres
poetry run alembic upgrade head
```

### Migration Issues

```bash
# Drop all tables and recreate
poetry run alembic downgrade base
poetry run alembic upgrade head

# Check current migration version
poetry run alembic current

# Show pending migrations
poetry run alembic heads
```

### Test Failures

```bash
# Run tests with verbose output
poetry run pytest -vv

# Run specific failing test
poetry run pytest tests/test_auth.py::test_login_success -vv

# Clear test cache
poetry run pytest --cache-clear
```

## License

Copyright © 2026 GolfCoach Pro. All rights reserved.

## Support

For questions or issues:
- GitHub Issues: [repository-url]/issues
- Documentation: See `../docs/` directory
- API Reference: http://localhost:8000/docs (when running)
