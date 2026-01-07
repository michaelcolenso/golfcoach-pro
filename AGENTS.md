# Architecture Document

 

## Overview

 

GolfCoach Pro is a distributed system designed to provide real-time, AI-powered golf swing analysis at scale. This document provides a comprehensive technical overview of the system architecture.

 

## System Architecture

 

### High-Level Architecture

 

```

┌─────────────────────────────────────────────────────────────────┐

│                          Client Layer                            │

│                                                                  │

│  ┌──────────────────────┐         ┌──────────────────────┐     │

│  │   Mobile Clients     │         │     Web Client       │     │

│  │  (React Native)      │         │     (Next.js)        │     │

│  │  - iOS App           │         │  - Admin Dashboard   │     │

│  │  - Android App       │         │  - Marketing Site    │     │

│  └──────────┬───────────┘         └──────────┬───────────┘     │

│             │                                 │                 │

│             └─────────────┬───────────────────┘                 │

│                           │                                     │

└───────────────────────────┼─────────────────────────────────────┘

                            │

                    (WebSocket + REST)

                            │

┌───────────────────────────┼─────────────────────────────────────┐

│                      API Gateway                                │

│                 (Nginx + Load Balancer)                         │

│  - SSL Termination                                              │

│  - Rate Limiting                                                │

│  - Request Routing                                              │

└───────────────────────────┼─────────────────────────────────────┘

                            │

          ┌─────────────────┼─────────────────┐

          │                 │                 │

┌─────────▼────────┐  ┌────▼─────────┐  ┌───▼──────────┐

│  FastAPI App     │  │  WebSocket   │  │    Celery    │

│  (REST API)      │  │   Server     │  │   Workers    │

│                  │  │              │  │              │

│ - User Auth      │  │ - Real-time  │  │ - Video      │

│ - Video Upload   │  │   Updates    │  │   Processing │

│ - Analysis API   │  │ - Streaming  │  │ - AI Tasks   │

│ - User Data      │  │   Pose Data  │  │ - Batch Jobs │

└─────────┬────────┘  └────┬─────────┘  └───┬──────────┘

          │                │                │

          └────────────────┼────────────────┘

                           │

          ┌────────────────┼────────────────┐

          │                │                │

┌─────────▼────────┐ ┌────▼─────────┐ ┌───▼──────────┐

│   PostgreSQL     │ │    Redis     │ │    MinIO     │

│ + TimescaleDB    │ │              │ │  (S3-like)   │

│                  │ │ - Cache      │ │              │

│ - User Data      │ │ - Sessions   │ │ - Videos     │

│ - Swing Data     │ │ - Task Queue │ │ - Images     │

│ - Analysis       │ │ - Pub/Sub    │ │ - Exports    │

└──────────────────┘ └──────────────┘ └──────────────┘

                           │

          ┌────────────────┼────────────────┐

          │                │                │

┌─────────▼────────┐ ┌────▼─────────────┐ │

│  Anthropic API   │ │   MediaPipe      │ │

│                  │ │   Holistic       │ │

│ - Claude Opus    │ │                  │ │

│   4.5 Vision     │ │ - Pose Detection │ │

│ - Coaching LLM   │ │ - Hand Tracking  │ │

└──────────────────┘ └──────────────────┘ │

                                          │

┌─────────────────────────────────────────┘

│

│  ┌──────────────────┐

│  │   Monitoring     │

│  │                  │

└─▶│ - Prometheus     │

   │ - Grafana        │

   │ - Loki           │

   │ - Sentry         │

   └──────────────────┘

```

 

## Data Flow

 

### 1. Video Upload & Analysis Flow

 

```

┌──────────┐

│  Client  │

└────┬─────┘

     │ 1. Upload video (multipart/form-data)

     │    POST /api/v1/swings/upload

     ↓

┌────────────┐

│  FastAPI   │

└────┬───────┘

     │ 2. Validate video

     │    - Check file size (< 100MB)

     │    - Validate format (MP4, MOV)

     │    - Check duration (3-30s)

     ↓

┌────────────┐

│   MinIO    │ 3. Save video to object storage

└────┬───────┘    Key: users/{user_id}/swings/{swing_id}/video.mp4

     │

     ↓

┌────────────┐

│ PostgreSQL │ 4. Create swing record

└────┬───────┘    Status: PROCESSING

     │

     ↓

┌────────────┐

│   Celery   │ 5. Enqueue processing task

└────┬───────┘    Task: process_swing_analysis

     │

     ↓

┌─────────────────────────────────────────┐

│         Video Processing Pipeline        │

│                                         │

│  6. Pre-processing                      │

│     - Load video from MinIO             │

│     - Stabilize (OpenCV)                │

│     - Auto-crop to golfer               │

│     - Enhance lighting/contrast         │

│                                         │

│  7. Pose Detection (MediaPipe)          │

│     - Extract frames @ 60 FPS           │

│     - Detect 33 body landmarks          │

│     - Track hands and face              │

│     - Store pose data in PostgreSQL     │

│                                         │

│  8. Swing Segmentation (ML Model)       │

│     - Identify swing phases:            │

│       * Address                         │

│       * Takeaway                        │

│       * Backswing                       │

│       * Transition                      │

│       * Downswing                       │

│       * Impact                          │

│       * Follow-through                  │

│       * Finish                          │

│                                         │

│  9. Key Frame Extraction                │

│     - Select biomechanically            │

│       significant frames                │

│     - Extract 12-16 frames              │

│     - Save to MinIO                     │

│                                         │

│  10. Multi-Modal Analysis (Parallel)    │

│      ┌──────────────────────────┐      │

│      │  Claude Opus 4.5 Vision  │      │

│      │  - Analyze key frames    │      │

│      │  - Identify technique    │      │

│      │    errors                │      │

│      │  - Generate coaching     │      │

│      │    feedback              │      │

│      └──────────────────────────┘      │

│      ┌──────────────────────────┐      │

│      │  Biomechanics Engine     │      │

│      │  - Calculate angles:     │      │

│      │    * Spine angle         │      │

│      │    * Hip rotation        │      │

│      │    * Shoulder turn       │      │

│      │    * Knee flex           │      │

│      │  - Compute swing metrics │      │

│      └──────────────────────────┘      │

│      ┌──────────────────────────┐      │

│      │  Audio Analysis          │      │

│      │  - Extract audio track   │      │

│      │  - Analyze impact sound  │      │

│      │  - Detect timing issues  │      │

│      └──────────────────────────┘      │

│                                         │

│  11. Synthesis Layer                   │

│      - Combine all analysis results    │

│      - Prioritize issues               │

│      - Generate recommendations        │

│      - Create drill assignments        │

│                                         │

└─────────────┬───────────────────────────┘

              │

              ↓

┌─────────────────────┐

│    PostgreSQL       │ 12. Store results

└─────────┬───────────┘     Status: COMPLETED

          │

          ↓

┌─────────────────────┐

│     WebSocket       │ 13. Notify client

└─────────┬───────────┘     Event: ANALYSIS_COMPLETE

          │

          ↓

┌─────────────────────┐

│      Client         │ 14. Fetch results

└─────────────────────┘     GET /api/v1/swings/{id}/analysis

```

 

### 2. Real-Time Analysis Flow

 

```

┌──────────┐

│  Client  │

└────┬─────┘

     │ 1. Establish WebSocket connection

     │    WS /api/v1/realtime/connect

     ↓

┌────────────┐

│  WebSocket │

│   Server   │

└────┬───────┘

     │ 2. Authenticate & create session

     │    Store session in Redis

     ↓

┌────────────┐

│   Redis    │

└────┬───────┘

     │

     ↓

┌──────────┐

│  Client  │ 3. Start video stream

└────┬─────┘    Message: START_STREAM

     │           { camera: "front", resolution: "1080p" }

     ↓

┌────────────┐

│  WebSocket │ 4. Setup WebRTC peer connection

└────┬───────┘

     │

     ↓ (WebRTC stream)

     │

┌─────────────────────────────────────────┐

│      Real-Time Processing Pipeline       │

│                                         │

│  5. Receive video frames (30 FPS)       │

│                                         │

│  6. Edge pose detection (MediaPipe)     │

│     - Run on CPU (fast inference)       │

│     - Extract skeletal data             │

│     - < 16ms latency                    │

│                                         │

│  7. Biomechanics calculation            │

│     - Compute key angles                │

│     - Detect swing phase                │

│     - Identify errors in real-time      │

│                                         │

│  8. Decision engine                     │

│     - If significant error detected:    │

│       * Generate coaching cue           │

│       * Queue audio feedback            │

│     - If swing completed:               │

│       * Trigger full analysis           │

│                                         │

└─────────────┬───────────────────────────┘

              │

              ↓

┌─────────────────────┐

│     WebSocket       │ 9. Stream results

└─────────┬───────────┘    Message: POSE_UPDATE

          │                { landmarks, angles, phase }

          │

          ↓               10. Stream audio coaching

┌─────────────────────┐      Message: AUDIO_CUE

│   ElevenLabs TTS    │      { text, audio_url }

└─────────┬───────────┘

          │

          ↓

┌─────────────────────┐

│      Client         │ 11. Render overlays + play audio

└─────────────────────┘

```

 

## Component Architecture

 

### Backend Services

 

#### 1. FastAPI Application (`backend/app/`)

 

**Responsibilities:**

- RESTful API endpoints

- User authentication & authorization

- Request validation

- Business logic orchestration

 

**Key Modules:**

 

```python

app/

├── api/

│   └── v1/

│       ├── auth.py          # JWT auth endpoints

│       ├── users.py         # User management

│       ├── swings.py        # Swing upload/retrieval

│       ├── analysis.py      # Analysis results

│       └── integrations.py  # 3rd party integrations

├── core/

│   ├── config.py           # Configuration management

│   ├── security.py         # Auth, JWT, hashing

│   └── dependencies.py     # FastAPI dependencies

├── models/

│   ├── user.py             # User SQLAlchemy model

│   ├── swing.py            # Swing data model

│   └── analysis.py         # Analysis results model

├── schemas/

│   ├── user.py             # Pydantic schemas

│   ├── swing.py

│   └── analysis.py

├── services/

│   ├── video_processor.py  # Video processing logic

│   ├── ai_coach.py         # AI integration

│   ├── pose_analyzer.py    # Pose analysis

│   └── swing_analyzer.py   # Swing metrics

└── main.py                 # Application entry point

```

 

**Key Endpoints:**

 

```python

# Authentication

POST   /api/v1/auth/register

POST   /api/v1/auth/login

POST   /api/v1/auth/refresh

POST   /api/v1/auth/logout

 

# Users

GET    /api/v1/users/me

PATCH  /api/v1/users/me

GET    /api/v1/users/{id}/stats

 

# Swings

POST   /api/v1/swings/upload

GET    /api/v1/swings

GET    /api/v1/swings/{id}

DELETE /api/v1/swings/{id}

GET    /api/v1/swings/{id}/video

GET    /api/v1/swings/{id}/frames

 

# Analysis

GET    /api/v1/swings/{id}/analysis

POST   /api/v1/swings/{id}/reanalyze

GET    /api/v1/swings/{id}/compare/{other_id}

 

# Drills

GET    /api/v1/drills

GET    /api/v1/drills/recommended

POST   /api/v1/drills/{id}/complete

```

 

#### 2. WebSocket Server

 

**Responsibilities:**

- Real-time bidirectional communication

- Video stream handling (WebRTC)

- Live pose data streaming

- Audio coaching delivery

 

**Connection Flow:**

 

```python

# Client connects

ws://api.golfcoachpro.com/api/v1/realtime/connect?token=JWT_TOKEN

 

# Server authenticates

→ Validate JWT

→ Create session in Redis

→ Send: { event: "CONNECTED", session_id: "..." }

 

# Client messages

{

  "event": "START_STREAM",

  "data": { "camera": "front", "resolution": "1080p" }

}

 

# Server messages

{

  "event": "POSE_UPDATE",

  "data": {

    "timestamp": 1234567890,

    "landmarks": [...],

    "angles": { "spine": 45, "hip_rotation": 60 },

    "swing_phase": "BACKSWING",

    "errors": ["early_extension"]

  }

}

 

{

  "event": "AUDIO_CUE",

  "data": {

    "text": "Keep your spine angle consistent",

    "audio_url": "https://..."

  }

}

```

 

#### 3. Celery Workers

 

**Responsibilities:**

- Async video processing

- Batch AI analysis

- Database maintenance tasks

- Report generation

 

**Task Queue:**

 

```python

# Video processing tasks

@celery.task

def process_swing_video(swing_id: int):

    """Main video processing pipeline"""

    pass

 

@celery.task

def extract_poses(swing_id: int):

    """Extract pose keypoints from video"""

    pass

 

@celery.task

def analyze_with_ai(swing_id: int):

    """Send to Claude for analysis"""

    pass

 

@celery.task

def calculate_biomechanics(swing_id: int):

    """Compute angles and metrics"""

    pass

 

@celery.task

def generate_drill_plan(user_id: int):

    """Create personalized drill recommendations"""

    pass

 

# Scheduled tasks

@celery.task

def cleanup_old_videos():

    """Delete videos older than retention period"""

    pass

 

@celery.task

def update_user_stats():

    """Compute aggregate user statistics"""

    pass

```

 

### Database Schema

 

#### PostgreSQL Schema

 

```sql

-- Users

CREATE TABLE users (

    id SERIAL PRIMARY KEY,

    email VARCHAR(255) UNIQUE NOT NULL,

    password_hash VARCHAR(255) NOT NULL,

    full_name VARCHAR(255),

    handicap DECIMAL(3,1),

    created_at TIMESTAMP DEFAULT NOW(),

    updated_at TIMESTAMP DEFAULT NOW()

);

 

-- User profiles

CREATE TABLE user_profiles (

    user_id INTEGER PRIMARY KEY REFERENCES users(id),

    date_of_birth DATE,

    height_cm INTEGER,

    weight_kg INTEGER,

    dominant_hand VARCHAR(10), -- 'left' or 'right'

    primary_miss VARCHAR(20),  -- 'slice', 'hook', etc.

    goals JSONB,

    physical_limitations JSONB,

    updated_at TIMESTAMP DEFAULT NOW()

);

 

-- Swings (using TimescaleDB hypertable)

CREATE TABLE swings (

    id SERIAL,

    user_id INTEGER NOT NULL REFERENCES users(id),

    recorded_at TIMESTAMP NOT NULL DEFAULT NOW(),

    club_type VARCHAR(50),

    intended_shape VARCHAR(20),

    video_url TEXT,

    thumbnail_url TEXT,

    duration_ms INTEGER,

    status VARCHAR(20), -- 'PROCESSING', 'COMPLETED', 'FAILED'

    metadata JSONB,

    PRIMARY KEY (id, recorded_at)

);

 

-- Convert to TimescaleDB hypertable for time-series optimization

SELECT create_hypertable('swings', 'recorded_at');

 

-- Pose data (time-series data)

CREATE TABLE pose_keypoints (

    swing_id INTEGER,

    timestamp_ms INTEGER,

    frame_number INTEGER,

    keypoints JSONB, -- Array of 33 landmarks

    recorded_at TIMESTAMP NOT NULL,

    PRIMARY KEY (swing_id, timestamp_ms, recorded_at)

);

 

SELECT create_hypertable('pose_keypoints', 'recorded_at');

 

-- Swing analysis results

CREATE TABLE analyses (

    id SERIAL PRIMARY KEY,

    swing_id INTEGER NOT NULL,

    analyzed_at TIMESTAMP DEFAULT NOW(),

    model_version VARCHAR(50),

    swing_phases JSONB, -- Array of detected phases

    biomechanics JSONB, -- Calculated angles and metrics

    ai_feedback JSONB,  -- Claude's analysis

    issues_detected JSONB, -- List of errors

    recommendations JSONB, -- Drill suggestions

    overall_score DECIMAL(3,1)

);

 

CREATE INDEX idx_analyses_swing_id ON analyses(swing_id);

 

-- Comparisons

CREATE TABLE swing_comparisons (

    id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(id),

    swing_a_id INTEGER,

    swing_b_id INTEGER,

    comparison_data JSONB,

    created_at TIMESTAMP DEFAULT NOW()

);

 

-- Drills

CREATE TABLE drills (

    id SERIAL PRIMARY KEY,

    name VARCHAR(255) NOT NULL,

    description TEXT,

    video_url TEXT,

    difficulty VARCHAR(20),

    targets JSONB, -- Issues this drill addresses

    created_at TIMESTAMP DEFAULT NOW()

);

 

-- User drill assignments

CREATE TABLE user_drills (

    id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(id),

    drill_id INTEGER REFERENCES drills(id),

    assigned_at TIMESTAMP DEFAULT NOW(),

    completed_at TIMESTAMP,

    notes TEXT

);

 

-- Integration data (TrackMan, Arccos, etc.)

CREATE TABLE integration_shots (

    id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(id),

    swing_id INTEGER, -- Optional link to video swing

    source VARCHAR(50), -- 'trackman', 'arccos', etc.

    shot_data JSONB,

    recorded_at TIMESTAMP NOT NULL

);

 

SELECT create_hypertable('integration_shots', 'recorded_at');

```

 

#### Redis Schema

 

```

# Sessions

session:{session_id} → {

  user_id: int,

  expires_at: timestamp

}

 

# WebSocket connections

ws_conn:{user_id} → {

  connection_id: str,

  connected_at: timestamp

}

 

# Task queue (Celery)

celery:task:{task_id} → task_data

 

# Cache: Analysis results

cache:analysis:{swing_id} → analysis_json

TTL: 7 days

 

# Cache: User stats

cache:user_stats:{user_id} → stats_json

TTL: 1 hour

 

# Cache: Similar swings (for AI prompt optimization)

cache:similar_swings:{swing_hash} → analysis_json

TTL: 30 days

 

# Rate limiting

ratelimit:{user_id}:{endpoint} → request_count

TTL: 1 minute

```

 

### Frontend Architecture

 

#### Mobile App (React Native)

 

**Directory Structure:**

 

```

mobile/src/

├── components/

│   ├── ui/                  # Reusable UI components

│   │   ├── Button.tsx

│   │   ├── Card.tsx

│   │   └── Input.tsx

│   ├── video/               # Video-related components

│   │   ├── VideoPlayer.tsx

│   │   ├── VideoRecorder.tsx

│   │   └── VideoTrimmer.tsx

│   ├── analysis/            # Analysis display components

│   │   ├── SkeletonOverlay.tsx

│   │   ├── BiometricsPanel.tsx

│   │   └── FeedbackCard.tsx

│   └── 3d/                  # 3D visualization

│       ├── SwingVisualization.tsx

│       └── PoseRenderer.tsx

├── screens/

│   ├── HomeScreen.tsx

│   ├── RecordScreen.tsx

│   ├── AnalysisScreen.tsx

│   ├── LibraryScreen.tsx

│   ├── CompareScreen.tsx

│   └── ProfileScreen.tsx

├── services/

│   ├── api.ts               # API client (axios + React Query)

│   ├── websocket.ts         # WebSocket manager

│   ├── auth.ts              # Authentication

│   └── storage.ts           # Local storage (AsyncStorage)

├── hooks/

│   ├── useSwingAnalysis.ts

│   ├── useRealTimeStream.ts

│   ├── useVideoUpload.ts

│   └── usePoseDetection.ts

├── store/

│   ├── authStore.ts         # Zustand store for auth

│   ├── swingStore.ts        # Zustand store for swings

│   └── settingsStore.ts

├── navigation/

│   └── AppNavigator.tsx     # React Navigation setup

└── utils/

    ├── biomechanics.ts      # Angle calculations

    ├── video.ts             # Video utilities

    └── formatters.ts

```

 

**State Management:**

 

```typescript

// Zustand store for authentication

import create from 'zustand';

 

interface AuthState {

  user: User | null;

  token: string | null;

  login: (email: string, password: string) => Promise<void>;

  logout: () => void;

  refreshToken: () => Promise<void>;

}

 

export const useAuthStore = create<AuthState>((set) => ({

  user: null,

  token: null,

  login: async (email, password) => {

    const { user, token } = await api.login(email, password);

    set({ user, token });

    await AsyncStorage.setItem('token', token);

  },

  logout: () => {

    set({ user: null, token: null });

    AsyncStorage.removeItem('token');

  },

  refreshToken: async () => {

    const newToken = await api.refreshToken();

    set({ token: newToken });

  },

}));

```

 

**API Integration:**

 

```typescript

// React Query for data fetching

import { useQuery, useMutation } from '@tanstack/react-query';

 

export function useSwingAnalysis(swingId: number) {

  return useQuery({

    queryKey: ['swing', swingId, 'analysis'],

    queryFn: () => api.getSwingAnalysis(swingId),

    staleTime: 5 * 60 * 1000, // 5 minutes

  });

}

 

export function useUploadVideo() {

  const queryClient = useQueryClient();

 

  return useMutation({

    mutationFn: (video: VideoFile) => api.uploadVideo(video),

    onSuccess: () => {

      queryClient.invalidateQueries({ queryKey: ['swings'] });

    },

  });

}

```

 

## AI Integration Architecture

 

### Claude Opus 4.5 Integration

 

**Service Layer:**

 

```python

# backend/app/services/ai_coach.py

 

from anthropic import Anthropic

import base64

from typing import List, Dict

import json

 

class AICoachService:

    def __init__(self):

        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        self.model = "claude-opus-4-5-20251101"

 

    async def analyze_swing(

        self,

        frames: List[bytes],

        pose_data: List[Dict],

        user_context: Dict

    ) -> Dict:

        """

        Analyze golf swing using Claude Opus 4.5

 

        Args:

            frames: List of key frame images (JPEG bytes)

            pose_data: Pose keypoints for each frame

            user_context: User profile (handicap, goals, history)

 

        Returns:

            Structured analysis with coaching feedback

        """

        # Build system prompt

        system_prompt = self._build_system_prompt(user_context)

 

        # Build user message with images and pose data

        content = [

            {

                "type": "text",

                "text": self._build_analysis_prompt(pose_data, user_context)

            },

            *[

                {

                    "type": "image",

                    "source": {

                        "type": "base64",

                        "media_type": "image/jpeg",

                        "data": base64.b64encode(frame).decode()

                    }

                }

                for frame in frames

            ]

        ]

 

        # Call Claude API

        response = await self.client.messages.create(

            model=self.model,

            max_tokens=4096,

            temperature=0.3,  # Lower for consistent coaching

            system=system_prompt,

            messages=[{"role": "user", "content": content}]

        )

 

        # Parse structured output

        analysis = self._parse_response(response.content[0].text)

 

        # Cache similar swing analysis for cost optimization

        await self._cache_analysis(frames, analysis)

 

        return analysis

 

    def _build_system_prompt(self, user_context: Dict) -> str:

        """Build personalized system prompt"""

        return f"""You are a PGA Master Professional with 30 years of experience

coaching tour players. You have the combined expertise of David Leadbetter,

Butch Harmon, and Sean Foley.

 

GOLFER PROFILE:

- Name: {user_context.get('name', 'Golfer')}

- Handicap: {user_context.get('handicap', 'Unknown')}

- Primary miss: {user_context.get('primary_miss', 'Unknown')}

- Current goal: {user_context.get('current_goal', 'Improve overall game')}

- Physical limitations: {user_context.get('limitations', 'None noted')}

- Learning style: {user_context.get('learning_style', 'visual')}

 

CONTEXT:

You have access to:

1. Sequential images of the golf swing

2. Pose estimation data with 33 body landmarks per frame

3. Historical swing data for this golfer

4. Biomechanical angle measurements

 

YOUR TASK:

Provide professional, actionable coaching feedback as if you were coaching

this golfer one-on-one. Be specific, encouraging, and prioritize the most

impactful changes.

 

OUTPUT FORMAT:

Return a JSON object with the following structure:

{{

  "swing_phases": [

    {{

      "phase": "address|takeaway|backswing|transition|downswing|impact|follow_through|finish",

      "frame_number": int,

      "observations": ["list of technical observations"],

      "quality_score": float (0-10)

    }}

  ],

  "technical_analysis": {{

    "positives": ["list of things done well"],

    "issues": [

      {{

        "issue": "description of the problem",

        "severity": "critical|major|minor",

        "impact": "how this affects ball flight",

        "biomechanical_cause": "root cause"

      }}

    ]

  }},

  "recommendations": [

    {{

      "priority": int (1-5, 1=highest),

      "change": "what to change",

      "why": "why this matters",

      "how": "how to practice this",

      "drill_id": int | null,

      "expected_improvement": "what will improve"

    }}

  ],

  "overall_feedback": "2-3 sentence summary",

  "coaching_cues": ["list of feel-based swing thoughts"]

}}"""

 

    def _build_analysis_prompt(self, pose_data: List[Dict], user_context: Dict) -> str:

        """Build analysis request prompt"""

        # Calculate key biomechanical angles from pose data

        biomechanics = self._calculate_biomechanics(pose_data)

 

        return f"""Analyze this golf swing sequence. I've provided {len(pose_data)} frames

from the swing, along with pose estimation data.

 

BIOMECHANICAL MEASUREMENTS:

{json.dumps(biomechanics, indent=2)}

 

SWING CONTEXT:

- Club: {user_context.get('club', 'Unknown')}

- Intended shot shape: {user_context.get('intended_shape', 'Straight')}

- Conditions: {user_context.get('conditions', 'Range practice')}

 

RECENT HISTORY:

{self._format_swing_history(user_context.get('recent_swings', []))}

 

Please analyze this swing and provide detailed coaching feedback following

the JSON format specified in the system prompt."""

 

    def _parse_response(self, response_text: str) -> Dict:

        """Parse Claude's JSON response"""

        try:

            # Extract JSON from response (may be wrapped in markdown)

            json_match = re.search(r'```json\s*(\{.*\})\s*```', response_text, re.DOTALL)

            if json_match:

                return json.loads(json_match.group(1))

            return json.loads(response_text)

        except json.JSONDecodeError:

            logger.error(f"Failed to parse AI response: {response_text}")

            raise AIParsingError("Could not parse AI response")

 

    async def _cache_analysis(self, frames: List[bytes], analysis: Dict):

        """Cache analysis for similar swings to reduce API costs"""

        # Create perceptual hash of frames

        swing_hash = self._hash_swing(frames)

 

        # Store in Redis for 30 days

        await redis.setex(

            f"cache:similar_swings:{swing_hash}",

            30 * 24 * 60 * 60,  # 30 days

            json.dumps(analysis)

        )

 

    def _calculate_biomechanics(self, pose_data: List[Dict]) -> Dict:

        """Calculate key angles from pose keypoints"""

        # Implementation of biomechanical calculations

        # Returns angles like spine angle, hip rotation, etc.

        pass

```

 

### MediaPipe Integration

 

```python

# backend/app/services/pose_analyzer.py

 

import mediapipe as mp

import cv2

import numpy as np

from typing import List, Dict

 

class PoseAnalyzer:

    def __init__(self):

        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(

            static_image_mode=False,

            model_complexity=2,  # Highest accuracy

            smooth_landmarks=True,

            min_detection_confidence=0.5,

            min_tracking_confidence=0.5

        )

 

    def extract_pose_sequence(self, video_path: str) -> List[Dict]:

        """

        Extract pose keypoints from entire video

 

        Returns:

            List of pose data per frame with 33 landmarks

        """

        cap = cv2.VideoCapture(video_path)

        fps = int(cap.get(cv2.CAP_PROP_FPS))

 

        pose_sequence = []

        frame_number = 0

 

        while cap.isOpened():

            success, frame = cap.read()

            if not success:

                break

 

            # Convert BGR to RGB

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

 

            # Process frame

            results = self.pose.process(rgb_frame)

 

            if results.pose_landmarks:

                # Extract 33 keypoints

                landmarks = [

                    {

                        'x': lm.x,

                        'y': lm.y,

                        'z': lm.z,

                        'visibility': lm.visibility

                    }

                    for lm in results.pose_landmarks.landmark

                ]

 

                pose_sequence.append({

                    'frame_number': frame_number,

                    'timestamp_ms': int((frame_number / fps) * 1000),

                    'landmarks': landmarks

                })

 

            frame_number += 1

 

        cap.release()

        return pose_sequence

 

    def calculate_angles(self, landmarks: List[Dict]) -> Dict[str, float]:

        """Calculate biomechanical angles from landmarks"""

        # Get key points

        left_shoulder = np.array([landmarks[11]['x'], landmarks[11]['y']])

        right_shoulder = np.array([landmarks[12]['x'], landmarks[12]['y']])

        left_hip = np.array([landmarks[23]['x'], landmarks[23]['y']])

        right_hip = np.array([landmarks[24]['x'], landmarks[24]['y']])

 

        # Calculate spine angle

        spine_vector = (left_shoulder + right_shoulder) / 2 - (left_hip + right_hip) / 2

        spine_angle = np.degrees(np.arctan2(spine_vector[1], spine_vector[0]))

 

        # Calculate shoulder rotation

        shoulder_vector = right_shoulder - left_shoulder

        shoulder_rotation = np.degrees(np.arctan2(shoulder_vector[1], shoulder_vector[0]))

 

        # Calculate hip rotation

        hip_vector = right_hip - left_hip

        hip_rotation = np.degrees(np.arctan2(hip_vector[1], hip_vector[0]))

 

        return {

            'spine_angle': float(spine_angle),

            'shoulder_rotation': float(shoulder_rotation),

            'hip_rotation': float(hip_rotation),

            'x_factor': float(abs(shoulder_rotation - hip_rotation))

        }

```

 

## Scaling & Performance

 

### Horizontal Scaling

 

**API Server:**

- Stateless FastAPI instances behind load balancer

- Scale based on CPU/memory metrics

- Auto-scaling: 2-20 instances

 

**Celery Workers:**

- Separate worker pools for different task types:

  - Video processing: CPU-intensive (4 cores)

  - AI tasks: Memory-intensive (16GB RAM)

  - Maintenance: Low priority

- Scale based on queue length

 

**Database:**

- PostgreSQL read replicas for queries

- Connection pooling (PgBouncer)

- Query optimization with indexes

 

### Caching Strategy

 

**Redis Caching:**

```python

# Analysis results (7 days)

cache:analysis:{swing_id}

 

# User stats (1 hour)

cache:user_stats:{user_id}

 

# Similar swing analyses (30 days)

cache:similar_swings:{swing_hash}

 

# API responses (5 minutes)

cache:api:{endpoint}:{params_hash}

```

 

### CDN Strategy

 

- Static assets (videos, images) served via CloudFront/CloudFlare

- Signed URLs for security

- Edge caching for frequently accessed videos

 

## Monitoring & Observability

 

### Metrics (Prometheus)

 

```yaml

# API metrics

api_requests_total{endpoint, method, status}

api_request_duration_seconds{endpoint}

 

# Video processing metrics

video_processing_duration_seconds{stage}

video_processing_errors_total{stage}

video_queue_length

 

# AI metrics

ai_api_calls_total{model, endpoint}

ai_api_cost_dollars{model}

ai_api_latency_seconds{model}

ai_token_usage{model, type}

 

# Database metrics

db_connections_active

db_query_duration_seconds{query_type}

db_connection_errors_total

 

# Business metrics

users_active_daily

swings_analyzed_total

revenue_dollars_total{tier}

```

 

### Logging (Loki)

 

```python

# Structured logging

logger.info(

    "Swing analysis completed",

    extra={

        "swing_id": swing_id,

        "user_id": user_id,

        "duration_ms": duration,

        "model_version": model_version,

        "cost_dollars": cost

    }

)

```

 

### Alerting

 

**Critical Alerts (PagerDuty):**

- API error rate > 5%

- Database down

- Payment processing failure

 

**Warning Alerts (Slack):**

- API p95 latency > 1s

- Video processing queue > 100

- AI costs > $100/hour

 

## Security

 

### Authentication

 

- JWT tokens with RS256 signing

- Access token: 15 min expiry

- Refresh token: 7 days expiry

- Token rotation on refresh

 

### Authorization

 

- Role-based access control (RBAC)

- Roles: user, coach, admin

- Endpoint-level permissions

 

### Data Security

 

- TLS 1.3 in transit

- AES-256 encryption at rest (videos)

- Secure video URLs with expiry

- PII encryption in database

 

### API Security

 

- Rate limiting (100 req/min per user)

- Request size limits (100MB)

- Input validation (Pydantic)

- SQL injection prevention (SQLAlchemy ORM)

- XSS prevention (sanitized outputs)

 

## Disaster Recovery

 

### Backup Strategy

 

**Database:**

- Continuous WAL archiving to S3

- Point-in-time recovery (7 days)

- Daily full backups (retained 30 days)

 

**Video Storage:**

- Cross-region replication (MinIO)

- Lifecycle policies (delete after 1 year)

 

### Recovery Procedures

 

**Database failure:**

1. Promote read replica to primary

2. Update DNS to new primary

3. Restore from WAL if needed

 

**Complete outage:**

1. Deploy to backup region

2. Restore database from latest backup

3. Sync video storage

4. Update DNS

 

**RTO (Recovery Time Objective):** 1 hour

**RPO (Recovery Point Objective):** 5 minutes

 

---

 

This architecture is designed to scale to millions of users while maintaining sub-second response times and providing a premium user experience.
