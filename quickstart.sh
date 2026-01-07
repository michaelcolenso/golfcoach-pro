#!/bin/bash

 

# GolfCoach Pro - Quick Start Script

# This script sets up the development environment

 

set -e  # Exit on error

 

echo "🏌️  GolfCoach Pro - Quick Start"

echo "================================"

echo ""

 

# Check prerequisites

echo "📋 Checking prerequisites..."

 

# Check Docker

if ! command -v docker &> /dev/null; then

    echo "❌ Docker is not installed. Please install Docker first."

    echo "   Visit: https://docs.docker.com/get-docker/"

    exit 1

fi

echo "✅ Docker found"

 

# Check Docker Compose

if ! command -v docker-compose &> /dev/null; then

    echo "❌ Docker Compose is not installed. Please install Docker Compose first."

    echo "   Visit: https://docs.docker.com/compose/install/"

    exit 1

fi

echo "✅ Docker Compose found"

 

# Check Python

if ! command -v python3 &> /dev/null; then

    echo "❌ Python 3 is not installed. Please install Python 3.11+."

    exit 1

fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)

echo "✅ Python $PYTHON_VERSION found"

 

# Check Node.js

if ! command -v node &> /dev/null; then

    echo "❌ Node.js is not installed. Please install Node.js 18+."

    exit 1

fi

NODE_VERSION=$(node --version)

echo "✅ Node.js $NODE_VERSION found"

 

echo ""

echo "📝 Setting up environment..."

 

# Create .env file if it doesn't exist

if [ ! -f .env ]; then

    echo "Creating .env file from template..."

    cp .env.example .env

    echo "⚠️  Please edit .env and add your API keys (especially ANTHROPIC_API_KEY)"

    echo ""

    read -p "Press Enter to continue after editing .env..."

fi

 

# Check if ANTHROPIC_API_KEY is set

source .env

if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "your-anthropic-api-key-here" ]; then

    echo "⚠️  Warning: ANTHROPIC_API_KEY not set in .env"

    echo "   AI features will not work without this key"

    echo ""

    read -p "Continue anyway? (y/n) " -n 1 -r

    echo

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then

        echo "Exiting. Please add ANTHROPIC_API_KEY to .env and run again."

        exit 1

    fi

fi

 

echo ""

echo "🐳 Starting Docker services..."

docker-compose up -d

 

# Wait for services to be healthy

echo ""

echo "⏳ Waiting for services to be ready..."

sleep 10

 

# Check if PostgreSQL is ready

echo "Checking PostgreSQL..."

until docker-compose exec -T postgres pg_isready -U golfcoach_user -d golfcoach &> /dev/null; do

    echo "  Waiting for PostgreSQL..."

    sleep 2

done

echo "✅ PostgreSQL is ready"

 

# Check if Redis is ready

echo "Checking Redis..."

until docker-compose exec -T redis redis-cli ping &> /dev/null; do

    echo "  Waiting for Redis..."

    sleep 2

done

echo "✅ Redis is ready"

 

# Check if MinIO is ready

echo "Checking MinIO..."

until curl -sf http://localhost:9000/minio/health/live &> /dev/null; do

    echo "  Waiting for MinIO..."

    sleep 2

done

echo "✅ MinIO is ready"

 

echo ""

echo "🗄️  Running database migrations..."

if [ -d "backend" ]; then

    cd backend

    if [ -f "alembic.ini" ]; then

        docker-compose exec -T backend alembic upgrade head

    else

        echo "⚠️  No migrations found yet. Skipping..."

    fi

    cd ..

fi

 

echo ""

echo "✨ Setup complete!"

echo ""

echo "================================================"

echo "  GolfCoach Pro is now running!"

echo "================================================"

echo ""

echo "🌐 Services:"

echo "  - Backend API:       http://localhost:8000"

echo "  - API Docs:          http://localhost:8000/docs"

echo "  - MinIO Console:     http://localhost:9001"

echo "  - Flower (Celery):   http://localhost:5555"

echo "  - Grafana:           http://localhost:3001"

echo "  - pgAdmin:           http://localhost:5050"

echo ""

echo "📱 Next steps:"

echo ""

echo "  Backend development:"

echo "    cd backend"

echo "    poetry install"

echo "    poetry shell"

echo "    pytest  # Run tests"

echo ""

echo "  Mobile development:"

echo "    cd mobile"

echo "    npm install"

echo "    npm start  # Start Expo"

echo ""

echo "  Web development:"

echo "    cd web"

echo "    npm install"

echo "    npm run dev"

echo ""

echo "  View logs:"

echo "    docker-compose logs -f backend"

echo "    docker-compose logs -f celery-worker"

echo ""

echo "  Stop all services:"

echo "    docker-compose down"

echo ""

echo "  Full cleanup (including data):"

echo "    docker-compose down -v"

echo ""

echo "================================================"

echo ""

echo "📚 Documentation:"

echo "  - Claude.md         - AI agent guide"

echo "  - README.md         - Project overview"

echo "  - ARCHITECTURE.md   - System architecture"

echo "  - API_SPEC.md       - Complete API reference"

echo "  - ROADMAP.md        - Development roadmap"

echo ""

echo "Happy coding! 🏌️‍♂️"
