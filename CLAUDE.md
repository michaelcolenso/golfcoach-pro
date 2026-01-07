# Claude.md - AI Agent Development Guide

 

## Project Overview

 

**GolfCoach Pro** is an AI-powered golf coaching application that provides real-time swing analysis, personalized feedback, and biomechanical insights using frontier AI models. This is the "Tiger Woods version" of golf coaching software.

 

## Quick Context for AI Agents

 

When working on this project, you should:

 

1. **Read this file first** - It contains critical context about architecture, decisions, and workflows

2. **Check `/docs` directory** - Detailed specifications for features, API design, and architecture

3. **Follow established patterns** - We prioritize consistency over cleverness

4. **Test as you build** - Every feature should have tests before merging

 

## Project Philosophy

 

### Core Principles

 

1. **Mobile-First**: Golfers use this on the range, not at a desktop

2. **Real-Time First**: Immediate feedback > Batch processing

3. **AI-Augmented, Not AI-Dependent**: Graceful degradation when AI fails

4. **Privacy-First**: User swing data is sensitive, treat it like PHI

5. **Pro-Grade Quality**: This is for serious golfers, not casual users

 

### Technical Philosophy

 

- **Type Safety**: TypeScript everywhere, no `any` types

- **API-First Design**: Backend and frontend are separate concerns

- **Async by Default**: Use async/await, avoid blocking operations

- **Fail Fast**: Validate early, return clear errors

- **Observable Systems**: Metrics, logging, and tracing on everything

 

## Technology Stack

 

### Backend

```

- Language: Python 3.11+

- Framework: FastAPI 0.104+

- Database: PostgreSQL 15+ with TimescaleDB extension

- Cache: Redis 7+

- Task Queue: Celery with Redis broker

- Storage: MinIO (S3-compatible)

- Video Processing: OpenCV, FFmpeg

- AI Models: Anthropic Claude Opus 4.5, MediaPipe Holistic

- Deployment: Docker + Kubernetes

```

 

### Frontend

```

- Framework: React Native 0.73+ (mobile), Next.js 14+ (web)

- Language: TypeScript 5.3+

- State Management: Zustand + React Query

- Styling: TailwindCSS + Shadcn/ui

- 3D Graphics: Three.js + React Three Fiber

- Video: react-native-video, expo-av

- Real-time: Socket.io-client

- Build: Expo for React Native, Turbopack for Next.js

```

 

### DevOps

```

- IaC: Terraform

- CI/CD: GitHub Actions

- Monitoring: Prometheus + Grafana

- Logging: Loki + Promtail

- Error Tracking: Sentry

- Container Registry: GitHub Container Registry

```

 

## Architecture Overview

 

### System Architecture

 

```

┌─────────────────────────────────────────────────────────────┐

│                        Client Layer                          │

│  ┌──────────────────┐              ┌──────────────────┐     │

│  │  React Native    │              │    Next.js Web   │     │

│  │  (iOS/Android)   │              │    Application   │     │

│  └──────────────────┘              └──────────────────┘     │

│         │                                    │               │

│         └────────────────┬───────────────────┘               │

│                          │                                   │

│                    WebSocket + REST API                      │

│                          │                                   │

└──────────────────────────┼───────────────────────────────────┘

                           │

┌──────────────────────────┼───────────────────────────────────┐

│                    API Gateway                               │

│                   (FastAPI + Nginx)                          │

└──────────────────────────┼───────────────────────────────────┘

                           │

          ┌────────────────┼────────────────┐

          │                │                │

┌─────────▼────────┐ ┌────▼─────────┐ ┌───▼──────────┐

│  FastAPI Server  │ │   Celery     │ │  WebSocket   │

│  (REST + WS)     │ │   Workers    │ │    Server    │

└─────────┬────────┘ └────┬─────────┘ └───┬──────────┘

          │               │               │

          └───────────────┼───────────────┘

                          │

          ┌───────────────┼───────────────┐

          │               │               │

┌─────────▼────────┐ ┌───▼────────┐ ┌───▼──────────┐

│   PostgreSQL     │ │   Redis    │ │    MinIO     │

│  + TimescaleDB   │ │   Cache    │ │   Storage    │

└──────────────────┘ └────────────┘ └──────────────┘

                          │

          ┌───────────────┼───────────────┐

          │               │               │

┌─────────▼────────┐ ┌───▼────────────┐ │

│  Claude Opus 4.5 │ │   MediaPipe    │ │

│  Vision Analysis │ │  Pose Detection│ │

└──────────────────┘ └────────────────┘ │

```

 

### Data Flow: Video Analysis Pipeline

 

```

1. Client uploads video (or streams via WebRTC)

   ↓

2. API Gateway validates, saves to MinIO

   ↓

3. Celery task initiated for processing

   ↓

4. Video pre-processing (stabilization, crop, enhance)

   ↓

5. Pose detection (MediaPipe @ 60 FPS)

   ↓

6. Swing segmentation (ML model identifies phases)

   ↓

7. Key frame extraction (biomechanically significant frames)

   ↓

8. Multi-modal analysis (parallel):

   - Claude Opus 4.5: Visual swing analysis

   - Audio analysis: Impact sound

   - Biomechanics: Angle calculations from pose data

   ↓

9. Synthesis layer combines insights

   ↓

10. Results stored in PostgreSQL, streamed to client via WebSocket

    ↓

11. Client renders results with 3D overlays

```

 

## Directory Structure

 

```

golfcoach-pro/

├── backend/

│   ├── app/

│   │   ├── api/              # API routes

│   │   │   ├── v1/

│   │   │   │   ├── analysis.py

│   │   │   │   ├── users.py

│   │   │   │   └── swings.py

│   │   │   └── websocket.py

│   │   ├── core/             # Core configuration

│   │   │   ├── config.py

│   │   │   ├── security.py

│   │   │   └── dependencies.py

│   │   ├── models/           # Database models

│   │   ├── schemas/          # Pydantic schemas

│   │   ├── services/         # Business logic

│   │   │   ├── video_processor.py

│   │   │   ├── pose_analyzer.py

│   │   │   ├── ai_coach.py

│   │   │   └── swing_analyzer.py

│   │   ├── tasks/            # Celery tasks

│   │   └── utils/            # Utilities

│   ├── tests/

│   ├── alembic/              # Database migrations

│   ├── Dockerfile

│   └── requirements.txt

│

├── mobile/                   # React Native app

│   ├── src/

│   │   ├── components/

│   │   ├── screens/

│   │   ├── services/

│   │   ├── hooks/

│   │   ├── store/

│   │   └── utils/

│   ├── ios/

│   ├── android/

│   └── package.json

│

├── web/                      # Next.js web app

│   ├── src/

│   │   ├── app/

│   │   ├── components/

│   │   ├── lib/

│   │   └── hooks/

│   └── package.json

│

├── ml/                       # ML models and training

│   ├── pose_detection/

│   ├── swing_segmentation/

│   └── notebooks/

│

├── infrastructure/           # IaC and deployment

│   ├── terraform/

│   ├── kubernetes/

│   └── docker-compose.yml

│

├── docs/                     # Documentation

│   ├── architecture/

│   ├── api/

│   └── features/

│

├── .github/

│   └── workflows/

│

├── Claude.md                 # This file

├── README.md

├── ARCHITECTURE.md

├── ROADMAP.md

├── CONTRIBUTING.md

└── API_SPEC.md

```

 

## Key Design Decisions

 

### 1. Why FastAPI over Flask?

 

**Decision**: Use FastAPI for backend

**Rationale**:

- Native async/await support for real-time video streaming

- Automatic OpenAPI documentation

- Built-in WebSocket support

- 3x faster than Flask for concurrent requests

- Better type validation with Pydantic

 

### 2. Why React Native over Flutter?

 

**Decision**: Use React Native + Expo for mobile

**Rationale**:

- Shared codebase with web (React/Next.js)

- Better video/camera libraries

- Larger ecosystem for sports/fitness apps

- Easier to hire developers

- Better integration with Three.js for 3D

 

### 3. Why Claude Opus 4.5 over GPT-4?

 

**Decision**: Primary AI model is Claude Opus 4.5

**Rationale**:

- Superior visual reasoning for spatial relationships

- Better at nuanced coaching feedback (less robotic)

- 200K token context = analyze full swing sequences

- More reliable JSON output

- Better at following complex system prompts

 

### 4. Why Separate MediaPipe + Claude?

 

**Decision**: Use MediaPipe for pose, Claude for coaching

**Rationale**:

- MediaPipe: Fast, real-time skeletal tracking (60 FPS)

- Claude: High-level reasoning and coaching feedback

- Hybrid approach = speed + intelligence

- MediaPipe runs locally (privacy), Claude in cloud

- Can function offline with MediaPipe only

 

### 5. Why TimescaleDB?

 

**Decision**: PostgreSQL + TimescaleDB extension

**Rationale**:

- Need time-series analysis for swing progression

- Efficient storage of pose data (33 keypoints @ 60 FPS)

- Fast aggregation queries for trends

- Still get all PostgreSQL features (relations, JSONB)

 

### 6. Why MinIO over S3?

 

**Decision**: MinIO for video storage (S3-compatible)

**Rationale**:

- Self-hosted option for privacy-conscious customers

- S3-compatible API (easy to switch to real S3)

- Lower costs for high-volume video storage

- Can deploy on-premises for pro teams

 

## Development Workflows

 

### Feature Development Process

 

1. **Planning**

   - Read feature spec in `/docs/features/`

   - Create issue on GitHub with label

   - Discuss approach in issue comments

 

2. **Implementation**

   - Create feature branch: `feature/short-description`

   - Write tests first (TDD approach)

   - Implement feature

   - Ensure all tests pass

   - Update documentation

 

3. **Review**

   - Create PR with description

   - Automated checks must pass

   - Code review from team

   - Approve and merge

 

4. **Deployment**

   - Merge to `develop` triggers staging deploy

   - QA testing in staging

   - Merge to `main` triggers production deploy

 

### Testing Strategy

 

**Backend:**

```python

# Unit tests: Test individual functions

pytest backend/tests/unit/

 

# Integration tests: Test API endpoints

pytest backend/tests/integration/

 

# E2E tests: Test full workflows

pytest backend/tests/e2e/

 

# Coverage requirement: 80%+

pytest --cov=app --cov-report=html

```

 

**Frontend:**

```bash

# Unit tests: Components and hooks

npm test

 

# Integration tests: Screens and flows

npm run test:integration

 

# E2E tests: Full user flows

npm run test:e2e

 

# Coverage requirement: 70%+

npm run test:coverage

```

 

### Git Workflow

 

**Branch Strategy:**

- `main`: Production-ready code

- `develop`: Integration branch for features

- `feature/*`: Feature development

- `bugfix/*`: Bug fixes

- `hotfix/*`: Emergency production fixes

 

**Commit Messages:**

```

<type>(<scope>): <subject>

 

<body>

 

<footer>

```

 

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

 

Example:

```

feat(analysis): add real-time pose detection

 

Implemented MediaPipe Holistic integration for 60 FPS pose tracking.

Includes WebSocket streaming of pose data to clients.

 

Closes #123

```

 

### Code Style

 

**Python:**

- Follow PEP 8

- Use `black` for formatting

- Use `ruff` for linting

- Type hints required

- Docstrings for public functions (Google style)

 

**TypeScript:**

- Use ESLint + Prettier

- Strict mode enabled

- No `any` types (use `unknown` if needed)

- JSDoc comments for complex functions

 

## Common Tasks for AI Agents

 

### Task: Add a new API endpoint

 

1. Read `/docs/api/API_SPEC.md` for conventions

2. Create route in `backend/app/api/v1/`

3. Define Pydantic schemas in `backend/app/schemas/`

4. Implement service logic in `backend/app/services/`

5. Add tests in `backend/tests/`

6. Update OpenAPI docs (automatic with FastAPI)

 

### Task: Add a new screen to mobile app

 

1. Read design spec in `/docs/features/`

2. Create screen component in `mobile/src/screens/`

3. Create reusable components in `mobile/src/components/`

4. Add navigation route

5. Connect to API using React Query hooks

6. Add loading/error states

7. Write component tests

 

### Task: Implement a new AI feature

 

1. Read AI feature spec in `/docs/features/`

2. Design prompt in `backend/app/services/prompts/`

3. Implement service in `backend/app/services/`

4. Add caching for expensive calls (Redis)

5. Add fallback for AI failures

6. Monitor token usage and costs

7. Test with various video types

 

### Task: Optimize a slow query

 

1. Identify slow query in logs (> 100ms)

2. Run `EXPLAIN ANALYZE` in PostgreSQL

3. Add appropriate indexes

4. Consider materialized views for aggregations

5. Add query result caching in Redis

6. Monitor improvement in Grafana

 

### Task: Fix a bug

 

1. Reproduce bug locally

2. Write failing test that captures bug

3. Fix code to make test pass

4. Ensure no regressions

5. Add to changelog

 

## AI Model Integration Guidelines

 

### Claude Opus 4.5 Integration

 

**Usage Pattern:**

```python

from anthropic import Anthropic

 

async def analyze_swing(frames: List[bytes], user_context: dict) -> dict:

    """

    Analyze golf swing using Claude Opus 4.5

 

    Args:

        frames: List of JPEG images as bytes

        user_context: User profile and preferences

 

    Returns:

        Structured analysis with coaching feedback

    """

    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

 

    # Build message with images

    content = [

        {"type": "text", "text": build_analysis_prompt(user_context)},

        *[{"type": "image", "source": {"type": "base64",

           "media_type": "image/jpeg", "data": base64.b64encode(frame)}}

          for frame in frames]

    ]

 

    response = await client.messages.create(

        model="claude-opus-4-5-20251101",

        max_tokens=4096,

        temperature=0.3,  # Lower for consistent coaching

        messages=[{"role": "user", "content": content}]

    )

 

    # Parse structured output

    return parse_swing_analysis(response.content[0].text)

```

 

**Prompt Engineering Best Practices:**

 

1. **Provide Context**: Always include user handicap, goals, and history

2. **Request Structure**: Use JSON schema for consistent outputs

3. **Examples**: Include few-shot examples for complex tasks

4. **Temperature**: 0.3-0.5 for coaching (consistent), 0.7-1.0 for creative content

5. **Token Management**: Monitor and cap at 4096 for cost control

 

**Error Handling:**

```python

try:

    analysis = await analyze_swing(frames, context)

except anthropic.RateLimitError:

    # Implement exponential backoff

    await asyncio.sleep(2 ** retry_count)

except anthropic.APIError as e:

    # Fallback to cached similar swing or generic advice

    logger.error(f"Claude API error: {e}")

    return get_fallback_analysis(frames, context)

```

 

### MediaPipe Integration

 

**Usage Pattern:**

```python

import mediapipe as mp

 

def extract_pose_keypoints(video_path: str) -> List[dict]:

    """Extract pose keypoints from video at 60 FPS"""

    mp_pose = mp.solutions.pose

 

    with mp_pose.Pose(

        static_image_mode=False,

        model_complexity=2,  # Highest accuracy

        min_detection_confidence=0.5,

        min_tracking_confidence=0.5

    ) as pose:

        cap = cv2.VideoCapture(video_path)

        fps = int(cap.get(cv2.CAP_PROP_FPS))

        keypoints = []

 

        while cap.isOpened():

            success, frame = cap.read()

            if not success:

                break

 

            # Convert BGR to RGB

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = pose.process(rgb_frame)

 

            if results.pose_landmarks:

                # Extract 33 keypoints (x, y, z, visibility)

                kp = [{

                    'x': lm.x, 'y': lm.y, 'z': lm.z,

                    'visibility': lm.visibility

                } for lm in results.pose_landmarks.landmark]

                keypoints.append(kp)

 

        cap.release()

        return keypoints

```

 

## Performance Requirements

 

### API Response Times

- Simple endpoints (GET user): < 50ms

- Video upload: < 2s for < 100MB file

- Real-time pose streaming: < 16ms latency (60 FPS)

- Full swing analysis: < 30s for 10s video

- WebSocket message latency: < 100ms

 

### Database Query Times

- Simple queries: < 10ms

- Complex aggregations: < 100ms

- Time-series queries: < 500ms

 

### Frontend Performance

- Time to Interactive (TTI): < 3s

- First Contentful Paint (FCP): < 1s

- Video playback startup: < 500ms

- Smooth animations: 60 FPS

 

## Security Considerations

 

### Authentication & Authorization

- JWT tokens with 15-minute expiry

- Refresh tokens with 7-day expiry

- Role-based access control (RBAC)

- API rate limiting: 100 req/min per user

 

### Data Privacy

- Video data encrypted at rest (AES-256)

- Video data encrypted in transit (TLS 1.3)

- User data anonymized in analytics

- GDPR compliance: data export and deletion

 

### Video Security

- Signed URLs with 5-minute expiry

- No public video access

- Watermarking option for shared videos

- Content scanning for inappropriate material

 

## Monitoring & Observability

 

### Metrics to Track

- API latency (p50, p95, p99)

- Error rates by endpoint

- AI model token usage and costs

- Video processing queue length

- Database connection pool utilization

- Cache hit rates

- WebSocket connection count

 

### Alerts

- API error rate > 5%

- P95 latency > 1s

- Video processing queue > 100

- Database CPU > 80%

- AI costs > $100/hour

- Storage > 80% capacity

 

### Logging

- Structured JSON logs

- Correlation IDs for request tracing

- User actions for audit trail

- AI prompt/response pairs (for debugging)

- Video processing pipeline events

 

## Cost Management

 

### AI Costs

- Claude Opus 4.5: ~$15 per 1M input tokens

- Budget: $0.50 per swing analysis (target)

- Optimization:

  - Cache similar swing analyses (Redis)

  - Use Claude Haiku for simple queries

  - Batch API requests where possible

  - Implement rate limiting per user tier

 

### Infrastructure Costs

- Database: ~$200/month (managed PostgreSQL)

- Storage: ~$0.02/GB/month (video storage)

- Compute: ~$500/month (Kubernetes cluster)

- CDN: ~$50/month (video delivery)

 

**Total estimated cost**: ~$2-3 per active user per month

 

## Deployment

 

### Environments

- **Development**: Local Docker Compose

- **Staging**: Kubernetes cluster (staging.golfcoachpro.com)

- **Production**: Kubernetes cluster (app.golfcoachpro.com)

 

### Deployment Process

```bash

# Build containers

docker build -t golfcoach-backend:$VERSION backend/

docker build -t golfcoach-mobile:$VERSION mobile/

 

# Push to registry

docker push ghcr.io/golfcoachpro/backend:$VERSION

 

# Deploy to k8s

kubectl apply -f infrastructure/kubernetes/

 

# Run migrations

kubectl exec -it backend-pod -- alembic upgrade head

 

# Smoke tests

./scripts/smoke-tests.sh production

```

 

### Rollback Plan

```bash

# Revert to previous version

kubectl rollout undo deployment/backend

 

# Check status

kubectl rollout status deployment/backend

```

 

## FAQ for AI Agents

 

**Q: Which file should I edit to add a new API endpoint?**

A: Create a new file in `backend/app/api/v1/` or add to existing route file. See `backend/app/api/v1/analysis.py` for examples.

 

**Q: How do I test video processing locally?**

A: Use sample videos in `backend/tests/fixtures/videos/`. Run `pytest -k video` to run video tests.

 

**Q: What's the process for updating the AI prompt?**

A: Edit prompt in `backend/app/services/prompts/`, test with sample videos, update tests, then deploy. Always version prompts for rollback.

 

**Q: How do I add a new database table?**

A: Create model in `backend/app/models/`, create Alembic migration with `alembic revision --autogenerate -m "description"`, review migration, then `alembic upgrade head`.

 

**Q: Where are the design mockups?**

A: `/docs/features/` contains feature specs with design references. Full Figma designs linked in README.

 

**Q: How do I run the full stack locally?**

A: `docker-compose up` starts all services. Backend at :8000, web at :3000, mobile via Expo.

 

**Q: What's the branching strategy?**

A: Feature branches off `develop`, PR to `develop`, then merge to `main` for production. See Git Workflow section.

 

**Q: How do I handle breaking API changes?**

A: API versioning (`/api/v1/`, `/api/v2/`). Maintain v1 for 6 months after v2 launch. Update client SDK versions.

 

## Getting Help

 

- **Documentation**: Read `/docs` directory

- **Examples**: Check `backend/tests/` and `mobile/src/` for patterns

- **API Docs**: Run backend, visit http://localhost:8000/docs

- **Slack**: #golfcoach-dev channel

- **Issues**: GitHub Issues with appropriate labels

 

## Useful Commands

 

```bash

# Backend

cd backend

python -m pytest                    # Run tests

uvicorn app.main:app --reload      # Run dev server

alembic upgrade head               # Run migrations

black .                            # Format code

ruff check .                       # Lint code

 

# Mobile

cd mobile

npm test                           # Run tests

npm start                          # Start Expo dev server

npm run ios                        # Run iOS simulator

npm run android                    # Run Android emulator

 

# Web

cd web

npm test                           # Run tests

npm run dev                        # Start Next.js dev server

npm run build                      # Build for production

 

# Infrastructure

docker-compose up                  # Run local stack

kubectl get pods                   # Check deployments

terraform plan                     # Preview infrastructure changes

```

 

## Key Files to Review

 

1. **`/docs/ARCHITECTURE.md`** - Deep dive on system design

2. **`/docs/API_SPEC.md`** - Complete API reference

3. **`/docs/features/`** - Feature specifications

4. **`/backend/app/services/ai_coach.py`** - AI integration

5. **`/mobile/src/screens/AnalysisScreen.tsx`** - Main UI

6. **`/ROADMAP.md`** - Development priorities

 

---

 

**Remember**: This is a premium product for serious golfers. Every feature should be polished, fast, and delightful. We're building the tool Tiger Woods would want to use.
