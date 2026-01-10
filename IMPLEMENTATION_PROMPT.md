# Implementation Prompt for AI Assistants

## Mission

Implement the **GolfCoach Pro** application according to the comprehensive specifications and architecture documented in this repository. This is a documentation-first repository with complete planning already done - your job is to bring it to life.

## Current State (As of Jan 2026)

**What Exists:**
- ✅ Complete architecture documentation (ARCHITECTURE.md)
- ✅ Full API specifications (API_SPEC.md)
- ✅ Development roadmap with priorities (ROADMAP.md)
- ✅ Feature specifications (REAL_TIME_ANALYSIS.md)
- ✅ Docker Compose infrastructure configuration
- ✅ Environment variable templates
- ✅ AI agent development guide (CLAUDE.md)

**What Needs Implementation:**
- ❌ Backend (FastAPI server)
- ❌ Mobile app (React Native)
- ❌ Web app (Next.js)
- ❌ ML models and pipelines
- ❌ Infrastructure as Code (Terraform/K8s)
- ❌ CI/CD pipelines

## Your Mission: Start with Backend Implementation

### Phase 1: Backend Foundation (START HERE)

**Objective:** Create a working FastAPI backend that can be run locally with Docker Compose.

**Steps:**

1. **Read Required Documentation First**
   - Read `CLAUDE.md` - Critical context and patterns
   - Read `ARCHITECTURE.md` - System design and data flow
   - Read `API_SPEC.md` - Exact API contracts to implement
   - Read `ROADMAP.md` - Implementation priorities

2. **Create Backend Directory Structure**
   ```
   backend/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py              # FastAPI application entry point
   │   ├── api/
   │   │   ├── __init__.py
   │   │   └── v1/
   │   │       ├── __init__.py
   │   │       ├── users.py     # User endpoints
   │   │       ├── auth.py      # Authentication
   │   │       └── health.py    # Health check
   │   ├── core/
   │   │   ├── __init__.py
   │   │   ├── config.py        # Settings and configuration
   │   │   ├── security.py      # JWT, password hashing
   │   │   └── dependencies.py  # FastAPI dependencies
   │   ├── models/
   │   │   ├── __init__.py
   │   │   └── user.py          # SQLAlchemy models
   │   ├── schemas/
   │   │   ├── __init__.py
   │   │   └── user.py          # Pydantic schemas
   │   ├── services/
   │   │   ├── __init__.py
   │   │   └── user_service.py  # Business logic
   │   └── utils/
   │       └── __init__.py
   ├── tests/
   │   ├── __init__.py
   │   ├── conftest.py
   │   └── test_health.py
   ├── alembic/
   │   ├── versions/
   │   ├── env.py
   │   └── script.py.mako
   ├── Dockerfile
   ├── pyproject.toml           # Poetry dependencies
   ├── alembic.ini
   └── README.md
   ```

3. **Set Up Python Project**
   - Use Python 3.11+
   - Use Poetry for dependency management
   - Add dependencies: FastAPI, uvicorn, sqlalchemy, alembic, psycopg2-binary, redis, anthropic, pydantic-settings
   - Follow the exact versions and patterns in CLAUDE.md

4. **Implement Core Components (In Order)**

   a. **Configuration (`app/core/config.py`)**
      - Use Pydantic Settings
      - Load from environment variables (see .env.example)
      - Include all settings: database, redis, JWT, Claude API, etc.

   b. **Database Models (`app/models/user.py`)**
      - Follow schema in API_SPEC.md
      - Use SQLAlchemy 2.0 style
      - Add timestamps, UUID primary keys

   c. **Pydantic Schemas (`app/schemas/user.py`)**
      - Request/response schemas
      - Validation rules from API_SPEC.md

   d. **Security (`app/core/security.py`)**
      - JWT token creation/validation
      - Password hashing (bcrypt)
      - OAuth2 password bearer

   e. **Main Application (`app/main.py`)**
      - FastAPI app initialization
      - CORS middleware (use settings from .env.example)
      - Router registration
      - Database session management
      - Exception handlers

   f. **Health Endpoint (`app/api/v1/health.py`)**
      - Basic health check
      - Database connectivity check
      - Redis connectivity check

   g. **User Endpoints (`app/api/v1/users.py` and `app/api/v1/auth.py`)**
      - Follow exact API_SPEC.md contracts
      - Implement authentication flow
      - User CRUD operations

5. **Database Migrations**
   - Initialize Alembic
   - Create initial migration for User model
   - Test migrations locally

6. **Write Dockerfile**
   - Multi-stage build for optimization
   - Use Python 3.11-slim base image
   - Install dependencies via Poetry
   - Expose port 8000
   - Health check endpoint

7. **Testing**
   - Write pytest fixtures (conftest.py)
   - Test health endpoint
   - Test user authentication flow
   - Aim for 80%+ coverage
   - Use MOCK_AI_IN_TESTS=true for AI services

8. **Local Testing**
   ```bash
   # Copy environment file
   cp .env.example .env

   # Start infrastructure services
   docker-compose up -d postgres redis

   # Run migrations
   cd backend
   alembic upgrade head

   # Run tests
   pytest

   # Start backend
   uvicorn app.main:app --reload

   # Visit http://localhost:8000/docs
   ```

9. **Integration with Docker Compose**
   - Ensure backend service in docker-compose.yaml works
   - Test with: `docker-compose up backend`
   - Verify API docs at http://localhost:8000/docs

### Phase 2: Video Analysis Foundation

**After Phase 1 is complete and tested**, implement video upload and analysis:

1. **Add Video Endpoints** (reference API_SPEC.md `/api/v1/swings`)
   - POST /api/v1/swings/upload
   - GET /api/v1/swings/{swing_id}
   - POST /api/v1/swings/{swing_id}/analyze

2. **MinIO Integration**
   - Video upload to MinIO storage
   - Signed URLs for video access
   - Follow storage patterns in ARCHITECTURE.md

3. **Celery Task Queue**
   - Configure Celery with Redis broker
   - Create video processing task
   - Status tracking for async jobs

4. **MediaPipe Integration**
   - Extract pose keypoints from video
   - Follow code examples in CLAUDE.md
   - Store pose data in PostgreSQL/TimescaleDB

5. **Claude Opus 4.5 Integration**
   - Implement swing analysis service
   - Use prompts from REAL_TIME_ANALYSIS.md
   - Follow integration patterns in CLAUDE.md
   - Add caching for similar swings
   - Implement fallback mechanisms

### Phase 3: Real-Time Analysis (WebSocket)

Reference `REAL_TIME_ANALYSIS.md` for complete specifications:

1. **WebSocket Server** (`app/api/websocket.py`)
   - Real-time pose streaming
   - Follow exact protocol from REAL_TIME_ANALYSIS.md

2. **Real-Time Processing Pipeline**
   - Frame-by-frame pose detection
   - Streaming results to client
   - Sub-100ms latency target

## Critical Guidelines

### Code Quality Standards

1. **Type Safety**
   - Type hints on all functions
   - No `any` types in TypeScript
   - Use Pydantic for validation

2. **Testing**
   - Write tests FIRST (TDD approach)
   - 80%+ coverage for backend
   - Test all error cases

3. **Documentation**
   - Docstrings for public functions (Google style)
   - Update API_SPEC.md if you deviate
   - Comment complex business logic

4. **Security**
   - Input validation everywhere
   - SQL injection prevention (use SQLAlchemy ORM)
   - Secure video storage (signed URLs)
   - Rate limiting (from .env.example)

5. **Performance**
   - Follow performance requirements in CLAUDE.md
   - API endpoints < 50ms for simple queries
   - Real-time pose streaming < 16ms latency
   - Full swing analysis < 30s for 10s video

### AI Integration Best Practices

1. **Claude Opus 4.5**
   - Use temperature 0.3-0.5 for coaching
   - Include user context (handicap, goals, history)
   - Request structured JSON output
   - Monitor token usage (target $0.50 per analysis)
   - Implement caching in Redis

2. **MediaPipe**
   - Use model_complexity=2 for highest accuracy
   - Process at 60 FPS
   - Extract all 33 pose keypoints

3. **Error Handling**
   - Graceful degradation when AI fails
   - Fallback to cached analyses
   - Clear error messages to users

### Development Workflow

1. **Git Workflow**
   - Create feature branches: `feature/backend-foundation`
   - Commit messages: `<type>(<scope>): <subject>` (see CLAUDE.md)
   - Commit frequently with clear messages

2. **Code Style**
   - Python: Black formatter, Ruff linter, PEP 8
   - Run formatters before committing

3. **Testing Before Committing**
   - All tests must pass
   - Run `pytest` before every commit
   - Check code coverage

## Success Criteria

You've completed Phase 1 successfully when:

- [ ] Backend runs via `docker-compose up backend`
- [ ] API docs visible at http://localhost:8000/docs
- [ ] Health check endpoint works
- [ ] User registration and authentication work
- [ ] Database migrations run successfully
- [ ] All tests pass with 80%+ coverage
- [ ] Can create user, login, get JWT token
- [ ] Code follows style guidelines (black, ruff pass)

## Reference Files (Read These!)

**Essential Reading:**
1. `CLAUDE.md` - Your primary guide, read this FIRST
2. `ARCHITECTURE.md` - System design and data flow
3. `API_SPEC.md` - Exact API contracts (this is your spec!)
4. `ROADMAP.md` - Implementation priorities

**Supporting Documentation:**
5. `REAL_TIME_ANALYSIS.md` - Real-time feature specs
6. `GETTING_STARTED.md` - Development environment setup
7. `.env.example` - All configuration options
8. `docker-compose.yaml` - Infrastructure services

## Philosophy

Remember from CLAUDE.md:

> "This is a premium product for serious golfers. Every feature should be polished, fast, and delightful. We're building the tool Tiger Woods would want to use."

**Core Principles:**
- Mobile-First: Golfers use this on the range
- Real-Time First: Immediate feedback matters
- AI-Augmented, Not AI-Dependent: Graceful degradation
- Privacy-First: Treat swing data like medical records
- Pro-Grade Quality: No compromises

## Questions?

If you're unsure about implementation details:
1. Check `API_SPEC.md` for exact API contracts
2. Review `ARCHITECTURE.md` for system design patterns
3. See code examples in `CLAUDE.md`
4. Follow the technology stack specified in `CLAUDE.md`

## Ready? Let's Build!

Start with Phase 1, Step 1: Read the documentation.

Then begin creating the backend directory structure and implementing the FastAPI foundation.

Good luck! 🏌️
