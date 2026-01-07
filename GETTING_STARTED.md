# Getting Started with GolfCoach Pro Development

 

Welcome to GolfCoach Pro! This guide will help you get up and running quickly.

 

## Prerequisites

 

Before you begin, ensure you have the following installed:

 

- **Docker Desktop** (includes Docker Compose) - [Download](https://docs.docker.com/get-docker/)

- **Python 3.11+** - [Download](https://www.python.org/downloads/)

- **Node.js 18+** - [Download](https://nodejs.org/)

- **Git** - [Download](https://git-scm.com/)

 

### Optional but Recommended

 

- **Poetry** (Python package manager) - `pip install poetry`

- **VS Code** with extensions:

  - Python

  - Pylance

  - ESLint

  - Prettier

  - Docker

 

## Quick Start (5 minutes)

 

### 1. Clone the Repository

 

```bash

git clone https://github.com/YOUR_USERNAME/golfcoach-pro.git

cd golfcoach-pro

```

 

### 2. Run the Quick Start Script

 

```bash

./scripts/quickstart.sh

```

 

This script will:

- Check all prerequisites

- Create `.env` file from template

- Start all Docker services

- Run database migrations

- Display service URLs

 

### 3. Add Your API Keys

 

Edit `.env` and add your Anthropic API key:

 

```bash

ANTHROPIC_API_KEY=sk-ant-your-key-here

```

 

Get your API key from: https://console.anthropic.com/

 

### 4. Restart Services

 

```bash

docker-compose restart backend celery-worker

```

 

### 5. Verify Everything Works

 

Visit http://localhost:8000/docs - you should see the API documentation.

 

## Manual Setup (If Quick Start Fails)

 

### Backend Setup

 

```bash

# Navigate to backend directory

cd backend

 

# Install dependencies

poetry install

 

# Activate virtual environment

poetry shell

 

# Copy environment template

cp .env.example .env

# Edit .env and add your API keys

 

# Start Docker services

docker-compose up -d postgres redis minio

 

# Run database migrations

alembic upgrade head

 

# Start development server

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```

 

Backend will be available at: http://localhost:8000

 

### Mobile App Setup

 

```bash

# Navigate to mobile directory

cd mobile

 

# Install dependencies

npm install

 

# Start Expo development server

npm start

 

# Or run directly on iOS/Android

npm run ios      # iOS simulator (macOS only)

npm run android  # Android emulator

```

 

Expo will open in your browser at: http://localhost:19006

 

### Web App Setup

 

```bash

# Navigate to web directory

cd web

 

# Install dependencies

npm install

 

# Start Next.js development server

npm run dev

```

 

Web app will be available at: http://localhost:3000

 

## Development Workflow

 

### Running Tests

 

**Backend:**

```bash

cd backend

pytest                    # Run all tests

pytest -v                # Verbose output

pytest -k test_specific  # Run specific test

pytest --cov=app         # With coverage report

```

 

**Mobile:**

```bash

cd mobile

npm test                 # Run all tests

npm run test:watch      # Watch mode

npm run test:coverage   # With coverage

```

 

### Code Formatting

 

**Backend:**

```bash

cd backend

black .                  # Format Python code

ruff check .            # Lint Python code

ruff check --fix .      # Auto-fix linting issues

```

 

**Mobile:**

```bash

cd mobile

npm run format          # Format with Prettier

npm run lint            # Lint with ESLint

npm run lint:fix        # Auto-fix linting issues

```

 

### Database Migrations

 

**Create a new migration:**

```bash

cd backend

alembic revision --autogenerate -m "Description of changes"

```

 

**Apply migrations:**

```bash

alembic upgrade head

```

 

**Rollback migration:**

```bash

alembic downgrade -1

```

 

### Docker Commands

 

**Start all services:**

```bash

docker-compose up -d

```

 

**View logs:**

```bash

docker-compose logs -f backend

docker-compose logs -f celery-worker

```

 

**Restart a service:**

```bash

docker-compose restart backend

```

 

**Stop all services:**

```bash

docker-compose down

```

 

**Full cleanup (including data):**

```bash

docker-compose down -v

```

 

## Project Structure

 

```

golfcoach-pro/

├── backend/              # FastAPI backend

│   ├── app/             # Application code

│   │   ├── api/         # API routes

│   │   ├── models/      # Database models

│   │   ├── schemas/     # Pydantic schemas

│   │   ├── services/    # Business logic

│   │   └── tasks/       # Celery tasks

│   ├── tests/           # Backend tests

│   ├── alembic/         # Database migrations

│   └── pyproject.toml   # Python dependencies

│

├── mobile/              # React Native app

│   ├── src/

│   │   ├── components/  # Reusable components

│   │   ├── screens/     # App screens

│   │   ├── services/    # API client, etc.

│   │   └── hooks/       # Custom hooks

│   └── package.json     # Node dependencies

│

├── web/                 # Next.js web app

│   ├── src/

│   │   ├── app/         # App router

│   │   ├── components/  # React components

│   │   └── lib/         # Utilities

│   └── package.json     # Node dependencies

│

├── docs/                # Documentation

│   ├── architecture/    # Architecture docs

│   ├── api/            # API documentation

│   └── features/       # Feature specifications

│

├── infrastructure/      # IaC and deployment

│   ├── terraform/      # Terraform configs

│   └── kubernetes/     # K8s manifests

│

├── scripts/            # Utility scripts

│

├── Claude.md           # AI agent guide

├── README.md           # Project overview

├── ARCHITECTURE.md     # System architecture

├── API_SPEC.md         # API reference

├── ROADMAP.md          # Development roadmap

├── CONTRIBUTING.md     # Contribution guidelines

└── docker-compose.yml  # Local development setup

```

 

## Accessing Services

 

### Development Services

 

| Service | URL | Description |

|---------|-----|-------------|

| Backend API | http://localhost:8000 | FastAPI server |

| API Docs | http://localhost:8000/docs | Interactive API docs |

| Web App | http://localhost:3000 | Next.js web application |

| Mobile (Expo) | http://localhost:19006 | Expo development server |

| MinIO Console | http://localhost:9001 | Object storage UI |

| Flower | http://localhost:5555 | Celery task monitor |

| Grafana | http://localhost:3001 | Metrics dashboards |

| pgAdmin | http://localhost:5050 | Database UI |

 

### Default Credentials

 

**MinIO:**

- Username: `minioadmin`

- Password: `minioadmin`

 

**Grafana:**

- Username: `admin`

- Password: `admin`

 

**pgAdmin:**

- Email: `admin@golfcoach.local`

- Password: `admin`

 

## Common Tasks

 

### Upload a Test Video

 

```bash

curl -X POST http://localhost:8000/api/v1/swings/upload \

  -H "Authorization: Bearer YOUR_TOKEN" \

  -F "video=@test-video.mp4" \

  -F "club=driver"

```

 

### Create a Test User

 

```bash

curl -X POST http://localhost:8000/api/v1/auth/register \

  -H "Content-Type: application/json" \

  -d '{

    "email": "test@example.com",

    "password": "TestPassword123!",

    "full_name": "Test User"

  }'

```

 

### Test AI Integration

 

```python

# In backend directory

from app.services.ai_coach import AICoachService

 

service = AICoachService()

result = await service.analyze_swing(

    frames=[...],

    pose_data=[...],

    user_context={...}

)

print(result)

```

 

## Troubleshooting

 

### Docker Issues

 

**"Port already in use"**

```bash

# Find process using port 8000

lsof -i :8000

# Kill the process

kill -9 <PID>

```

 

**"Cannot connect to Docker daemon"**

```bash

# Start Docker Desktop application

# Or on Linux:

sudo systemctl start docker

```

 

### Database Issues

 

**"Database doesn't exist"**

```bash

# Recreate database

docker-compose down -v

docker-compose up -d postgres

docker-compose exec backend alembic upgrade head

```

 

**"Migration conflicts"**

```bash

# Reset to base

alembic downgrade base

alembic upgrade head

```

 

### Python Issues

 

**"Module not found"**

```bash

# Ensure virtual environment is activated

poetry shell

# Reinstall dependencies

poetry install

```

 

### Node.js Issues

 

**"Module not found"**

```bash

# Clear cache and reinstall

rm -rf node_modules package-lock.json

npm install

```

 

**"Expo won't start"**

```bash

# Clear Expo cache

expo start -c

```

 

## Next Steps

 

### 1. Read the Documentation

 

- **[Claude.md](../Claude.md)** - Essential guide for AI-assisted development

- **[ARCHITECTURE.md](../ARCHITECTURE.md)** - Understand the system design

- **[API_SPEC.md](../API_SPEC.md)** - Learn the API endpoints

 

### 2. Explore the Codebase

 

- Browse `backend/app/api/` to see API routes

- Check `mobile/src/screens/` for mobile screens

- Review `backend/tests/` for test examples

 

### 3. Pick a Task

 

- Check [Issues](https://github.com/OWNER/golfcoach-pro/issues)

- Look for `good first issue` label

- Read [CONTRIBUTING.md](../CONTRIBUTING.md)

 

### 4. Make Your First Contribution

 

```bash

# Create feature branch

git checkout -b feature/my-first-feature

 

# Make changes

# Write tests

# Commit with good message

git commit -m "feat(api): add new endpoint"

 

# Push and create PR

git push origin feature/my-first-feature

```

 

## Getting Help

 

- **Documentation**: Check `/docs` directory

- **API Docs**: http://localhost:8000/docs

- **Issues**: GitHub Issues

- **Questions**: GitHub Discussions

 

## Tips for Success

 

1. **Read Claude.md first** - It contains critical context

2. **Run tests before committing** - Ensure nothing breaks

3. **Follow code style** - Use formatters (Black, Prettier)

4. **Write good commit messages** - Follow Conventional Commits

5. **Ask questions** - Use GitHub Discussions

 

## Resources

 

### Learning Materials

 

- **FastAPI**: https://fastapi.tiangolo.com/

- **React Native**: https://reactnative.dev/

- **PostgreSQL**: https://www.postgresql.org/docs/

- **TimescaleDB**: https://docs.timescale.com/

- **Celery**: https://docs.celeryproject.org/

 

### Tools

 

- **Postman**: Test API endpoints

- **Insomnia**: Alternative API client

- **TablePlus**: Database GUI

- **React Native Debugger**: Mobile debugging

 

---

 

Welcome to the team! Let's build the best golf coaching app in the world. 🏌️
