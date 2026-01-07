
# GolfCoach Pro ⛳

 

> The Tiger Woods version of golf coaching software

 

AI-powered golf coaching that provides real-time swing analysis, personalized feedback, and biomechanical insights using frontier AI models.

 

![Version](https://img.shields.io/badge/version-0.1.0-blue)

![License](https://img.shields.io/badge/license-MIT-green)

![Python](https://img.shields.io/badge/python-3.11+-blue)

![React Native](https://img.shields.io/badge/react--native-0.73+-blue)

 

## What is GolfCoach Pro?

 

GolfCoach Pro is not just swing analysis—it's your **AI caddie, biomechanics coach, and performance scientist** combined. Imagine having Butch Harmon, Hank Haney, and Sean Foley available 24/7, analyzing every swing in real-time, backed by AI that's studied every tour pro swing ever recorded.

 

### Key Features

 

🎥 **Real-Time Analysis**

- Live swing analysis with audio coaching feedback

- Mount your phone, hit balls, get instant feedback in your AirPods

- 60 FPS biomechanical overlays on your screen

 

🧠 **AI-Powered Coaching**

- Claude Opus 4.5 for nuanced, human-like coaching feedback

- Learns YOUR swing over time for personalized recommendations

- Identifies swing phases and biomechanical errors with pro-grade accuracy

 

📊 **Pro-Grade Biomechanics**

- Skeletal tracking with 33 body landmarks

- Swing plane visualization (3D arc overlay)

- Hip-shoulder separation, club path, weight distribution

- Compare to tour pros or your own baseline

 

🎯 **Personalized Training**

- Historical trend analysis (are you improving or regressing?)

- Custom drill recommendations based on YOUR weaknesses

- Shot pattern analysis and tournament prep mode

 

🔗 **Integration Ecosystem**

- TrackMan/FlightScope launch monitor data

- Apple Watch/Garmin biometrics

- Arccos/Shot Scope on-course stats

- WHOOP/Oura recovery tracking

 

## Tech Stack

 

**Backend**

- FastAPI (Python 3.11+) - Async API server

- PostgreSQL + TimescaleDB - Time-series swing data

- Redis - Caching and session management

- Celery - Async video processing

- MinIO - S3-compatible video storage

 

**Frontend**

- React Native (iOS/Android) - Mobile-first experience

- Next.js 14 (Web) - Progressive web app

- TypeScript - Type safety throughout

- TailwindCSS + Shadcn/ui - Modern UI components

- Three.js - 3D visualization

 

**AI/ML**

- Anthropic Claude Opus 4.5 - Vision analysis and coaching

- MediaPipe Holistic - Real-time pose detection (60 FPS)

- Custom ML models - Swing segmentation and classification

 

## Quick Start

 

### Prerequisites

 

- Python 3.11+

- Node.js 18+

- Docker & Docker Compose

- Git

 

### Local Development

 

```bash

# Clone the repository

git clone https://github.com/yourusername/golfcoach-pro.git

cd golfcoach-pro

 

# Copy environment variables

cp .env.example .env

# Edit .env and add your API keys (Anthropic, etc.)

 

# Start all services with Docker Compose

docker-compose up

 

# Backend runs at http://localhost:8000

# Web app runs at http://localhost:3000

# API docs at http://localhost:8000/docs

```

 

### Mobile Development

 

```bash

# Install dependencies

cd mobile

npm install

 

# Start Expo dev server

npm start

 

# Run on iOS simulator (macOS only)

npm run ios

 

# Run on Android emulator

npm run android

```

 

### Running Tests

 

```bash

# Backend tests

cd backend

pytest

 

# Frontend tests

cd mobile

npm test

 

# E2E tests

npm run test:e2e

```

 

## Project Structure

 

```

golfcoach-pro/

├── backend/           # FastAPI backend

│   ├── app/           # Application code

│   ├── tests/         # Backend tests

│   └── alembic/       # Database migrations

├── mobile/            # React Native mobile app

│   ├── src/           # Mobile source code

│   ├── ios/           # iOS native code

│   └── android/       # Android native code

├── web/               # Next.js web app

│   └── src/           # Web source code

├── ml/                # ML models and training

├── infrastructure/    # Infrastructure as Code

├── docs/              # Documentation

└── .github/           # GitHub workflows

```

 

## Documentation

 

- **[Claude.md](./Claude.md)** - AI agent development guide

- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System architecture deep dive

- **[API_SPEC.md](./API_SPEC.md)** - Complete API reference

- **[ROADMAP.md](./ROADMAP.md)** - Development roadmap

- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Contribution guidelines

- **[docs/](./docs/)** - Feature specifications and guides

 

## Roadmap

 

### Phase 1: Core Engine (Weeks 1-4)

- [x] Project setup and architecture

- [ ] FastAPI backend with WebSocket support

- [ ] React Native app with camera integration

- [ ] Claude Opus 4.5 vision analysis

- [ ] Basic pose detection (MediaPipe)

- [ ] Video upload + analysis flow

 

### Phase 2: Intelligence (Weeks 5-8)

- [ ] Multi-frame sequential analysis

- [ ] Swing segmentation

- [ ] Comparison features

- [ ] Historical tracking

- [ ] Drill recommendations

 

### Phase 3: Premium Features (Weeks 9-12)

- [ ] Real-time mode

- [ ] Audio coaching

- [ ] Multi-angle support

- [ ] Integration APIs

- [ ] Coach collaboration

 

### Phase 4: Polish & Launch (Weeks 13-16)

- [ ] 3D visualization

- [ ] Advanced biomechanics

- [ ] Tournament prep mode

- [ ] Marketing site

- [ ] Beta launch

 

See [ROADMAP.md](./ROADMAP.md) for detailed milestones.

 

## Contributing

 

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

 

### Development Workflow

 

1. Fork the repository

2. Create a feature branch (`feature/amazing-feature`)

3. Write tests for your changes

4. Implement your feature

5. Ensure all tests pass

6. Submit a pull request

 

## Architecture Highlights

 

### Video Analysis Pipeline

 

```

Video Upload → Pre-processing → Pose Detection → Swing Segmentation

     ↓              ↓                ↓                   ↓

  MinIO        Stabilize        MediaPipe        Phase Detection

  Storage      Crop/Enhance     60 FPS           (ML Model)

                                    ↓

                           Key Frame Extraction

                                    ↓

                    ┌───────────────┼───────────────┐

                    ↓               ↓               ↓

            Claude Opus 4.5    Audio Analysis  Biomechanics

            Vision Analysis    Impact Sound    Angle Calc

                    ↓               ↓               ↓

                    └───────────────┼───────────────┘

                                    ↓

                          Synthesis Layer

                                    ↓

                    PostgreSQL + WebSocket Streaming

                                    ↓

                        Client (3D Visualization)

```

 

### Real-Time Mode

 

```

Phone Camera → WebRTC Stream → Edge Pose Detection → Low-latency WebSocket

                                        ↓

                                Audio Coaching (TTS)

                                        ↓

                            Biomechanical Overlay

```

 

## Performance Targets

 

- **API Response**: < 50ms for simple endpoints

- **Video Upload**: < 2s for 100MB file

- **Real-time Pose**: < 16ms latency (60 FPS)

- **Full Analysis**: < 30s for 10s video

- **Mobile TTI**: < 3s (Time to Interactive)

 

## Security & Privacy

 

- **Encryption**: AES-256 at rest, TLS 1.3 in transit

- **Authentication**: JWT tokens with 15-minute expiry

- **Video Access**: Signed URLs with 5-minute expiry

- **Privacy**: User data anonymized in analytics

- **Compliance**: GDPR-compliant data export and deletion

 

## Deployment

 

### Environments

 

- **Development**: Docker Compose locally

- **Staging**: Kubernetes cluster (staging.golfcoachpro.com)

- **Production**: Kubernetes cluster (app.golfcoachpro.com)

 

### Deployment Process

 

```bash

# Build and push containers

./scripts/build.sh

 

# Deploy to staging

./scripts/deploy.sh staging

 

# Run smoke tests

./scripts/smoke-tests.sh staging

 

# Deploy to production

./scripts/deploy.sh production

```

 

## Cost Estimates

 

**AI Costs (per swing analysis)**

- Claude Opus 4.5: ~$0.30 per analysis

- Target optimization: < $0.50 per analysis

- Caching reduces costs by ~60%

 

**Infrastructure (monthly)**

- Database: ~$200 (managed PostgreSQL)

- Storage: ~$100 (video storage)

- Compute: ~$500 (Kubernetes)

- CDN: ~$50 (video delivery)

 

**Total**: ~$2-3 per active user per month

 

## License

 

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

 

## Acknowledgments

 

- Inspired by the need for accessible, pro-grade golf coaching

- Built with frontier AI models from Anthropic

- Powered by the amazing open-source community

 

## Contact

 

- **Website**: https://golfcoachpro.com

- **Issues**: https://github.com/yourusername/golfcoach-pro/issues

- **Email**: support@golfcoachpro.com

- **Twitter**: @golfcoachpro

 

---

 

**Built with ❤️ for golfers who want to get better**

 

*"This is the coach that travels with you, never gets tired, and has perfect recall of every swing you've ever taken."*
