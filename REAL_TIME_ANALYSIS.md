# Feature Specification: Real-Time Swing Analysis

 

## Overview

 

Real-time swing analysis provides golfers with instant feedback during practice sessions using live video streaming and AI-powered pose detection. This feature enables on-the-range coaching with audio cues delivered through AirPods or phone speakers.

 

## User Story

 

**As a** golfer practicing on the range

**I want** real-time feedback on my swing

**So that** I can make immediate corrections without having to review video after each shot

 

## Success Metrics

 

- Real-time latency: < 100ms from swing to feedback

- Pose detection accuracy: > 95%

- Session length: Average 20+ minutes

- User satisfaction: 4.5+ stars

- Adoption: 30%+ of Pro tier users use weekly

 

## User Flow

 

### 1. Setup Phase

 

```

User opens app

  ↓

Navigates to "Live Practice" mode

  ↓

Positions phone on tripod/holder

  ↓

Selects camera angle (face-on or down-the-line)

  ↓

Calibrates position (app guides proper framing)

  ↓

Connects AirPods for audio feedback

  ↓

Starts live session

```

 

### 2. Practice Phase

 

```

User addresses ball

  ↓

App displays live skeleton overlay

  ↓

Real-time metrics shown (spine angle, posture)

  ↓

User swings

  ↓

AI detects swing phases in real-time

  ↓

Errors detected (e.g., early extension)

  ↓

Audio cue played: "Maintain spine angle"

  ↓

Swing automatically saved to library

  ↓

User reviews quick summary on screen

  ↓

Repeat

```

 

### 3. Review Phase

 

```

User ends session

  ↓

Session summary displayed

  ↓

All swings saved with annotations

  ↓

Key insights highlighted

  ↓

Recommended drills based on session

```

 

## Technical Architecture

 

### Frontend (React Native)

 

**Components:**

 

```typescript

// LivePracticeScreen.tsx

- Camera integration (expo-camera)

- WebRTC stream setup

- Skeleton overlay renderer (Three.js/SVG)

- Audio playback manager

- Real-time metrics display

 

// SkeletonOverlay.tsx

- Canvas rendering of pose keypoints

- 60 FPS animation loop

- Angle calculations and display

 

// AudioCoach.tsx

- Queue management for audio cues

- TTS integration (ElevenLabs)

- Volume/mute controls

```

 

**State Management:**

 

```typescript

interface LiveSessionState {

  status: 'idle' | 'calibrating' | 'active' | 'paused' | 'ended';

  connectionQuality: 'excellent' | 'good' | 'poor';

  poseData: PoseLandmarks | null;

  currentPhase: SwingPhase | null;

  metrics: BiomechanicsMetrics;

  errors: ErrorDetection[];

  swingCount: number;

  sessionStartTime: number;

}

```

 

### Backend (FastAPI + WebSocket)

 

**WebSocket Server:**

 

```python

# app/api/websocket.py

 

@app.websocket("/api/v1/realtime/connect")

async def websocket_endpoint(

    websocket: WebSocket,

    token: str = Query(...)

):

    # Authenticate

    user = await authenticate_websocket(token)

 

    # Accept connection

    await websocket.accept()

 

    # Store connection

    await connection_manager.connect(user.id, websocket)

 

    try:

        while True:

            # Receive messages from client

            data = await websocket.receive_json()

 

            # Handle different event types

            if data['event'] == 'START_STREAM':

                await handle_stream_start(user, data)

            elif data['event'] == 'VIDEO_FRAME':

                await handle_video_frame(user, data)

            elif data['event'] == 'STOP_STREAM':

                await handle_stream_stop(user, data)

 

    except WebSocketDisconnect:

        await connection_manager.disconnect(user.id)

```

 

**Real-Time Processing Pipeline:**

 

```python

# app/services/realtime_analyzer.py

 

class RealtimeAnalyzer:

    def __init__(self):

        self.pose_detector = MediaPipeHolistic()

        self.swing_detector = SwingDetector()

        self.error_detector = ErrorDetector()

 

    async def process_frame(

        self,

        frame: np.ndarray,

        user_id: int

    ) -> RealtimeAnalysisResult:

        """

        Process single video frame in real-time

 

        Target: < 16ms processing time (60 FPS)

        """

        # 1. Detect pose (MediaPipe) - ~8ms

        pose = self.pose_detector.process(frame)

 

        if not pose.landmarks:

            return RealtimeAnalysisResult(has_pose=False)

 

        # 2. Calculate biomechanics - ~2ms

        metrics = calculate_biomechanics(pose.landmarks)

 

        # 3. Detect swing phase - ~1ms

        phase = self.swing_detector.detect_phase(

            pose.landmarks,

            metrics

        )

 

        # 4. Detect errors - ~3ms

        errors = self.error_detector.check(

            phase,

            metrics,

            user_context=await get_user_context(user_id)

        )

 

        # 5. Generate coaching cue if needed - ~2ms

        cue = None

        if errors and should_provide_feedback(errors):

            cue = generate_coaching_cue(errors[0])

 

        return RealtimeAnalysisResult(

            has_pose=True,

            landmarks=pose.landmarks,

            metrics=metrics,

            phase=phase,

            errors=errors,

            coaching_cue=cue

        )

```

 

**Swing Detection:**

 

```python

# app/services/swing_detector.py

 

class SwingDetector:

    """Detect when a swing starts and ends"""

 

    def __init__(self):

        self.buffer = []

        self.buffer_size = 180  # 3 seconds at 60 FPS

        self.state = 'idle'

 

    def detect_phase(

        self,

        landmarks: List[Landmark],

        metrics: BiomechanicsMetrics

    ) -> SwingPhase:

        """

        Detect current swing phase using heuristics

        """

        # Add to buffer

        self.buffer.append({

            'landmarks': landmarks,

            'metrics': metrics,

            'timestamp': time.time()

        })

 

        if len(self.buffer) > self.buffer_size:

            self.buffer.pop(0)

 

        # Analyze recent motion

        motion = analyze_motion(self.buffer[-30:])  # Last 0.5s

 

        # State machine for phase detection

        if self.state == 'idle':

            if motion.shoulder_velocity > BACKSWING_THRESHOLD:

                self.state = 'backswing'

                return SwingPhase.BACKSWING

 

        elif self.state == 'backswing':

            if motion.shoulder_velocity < 0:  # Direction change

                self.state = 'downswing'

                return SwingPhase.TRANSITION

 

        elif self.state == 'downswing':

            if motion.hip_velocity > IMPACT_THRESHOLD:

                self.state = 'impact'

                return SwingPhase.IMPACT

 

        elif self.state == 'impact':

            if motion.overall_velocity < FINISH_THRESHOLD:

                self.state = 'finish'

                self.save_swing(self.buffer)  # Auto-save

                return SwingPhase.FINISH

 

        elif self.state == 'finish':

            if motion.overall_velocity < IDLE_THRESHOLD:

                self.state = 'idle'

                self.buffer = []

 

        return SwingPhase.from_state(self.state)

```

 

**Error Detection:**

 

```python

# app/services/error_detector.py

 

class ErrorDetector:

    """Detect common swing errors in real-time"""

 

    def check(

        self,

        phase: SwingPhase,

        metrics: BiomechanicsMetrics,

        user_context: UserContext

    ) -> List[ErrorDetection]:

        """

        Check for errors based on phase and user history

        """

        errors = []

 

        # Check phase-specific errors

        if phase == SwingPhase.ADDRESS:

            errors.extend(self.check_setup(metrics, user_context))

 

        elif phase == SwingPhase.BACKSWING:

            errors.extend(self.check_backswing(metrics, user_context))

 

        elif phase == SwingPhase.IMPACT:

            errors.extend(self.check_impact(metrics, user_context))

 

        # Prioritize by severity and user history

        return self.prioritize_errors(errors, user_context)

 

    def check_impact(

        self,

        metrics: BiomechanicsMetrics,

        user_context: UserContext

    ) -> List[ErrorDetection]:

        """Check for impact phase errors"""

        errors = []

 

        # Early extension check

        if metrics.spine_angle < 30:  # Lost posture

            # Compare to address position

            if user_context.address_spine_angle - metrics.spine_angle > 8:

                errors.append(ErrorDetection(

                    error='early_extension',

                    severity='major',

                    confidence=0.95,

                    data={

                        'spine_angle_loss':

                            user_context.address_spine_angle - metrics.spine_angle

                    }

                ))

 

        # Over-the-top check

        if metrics.shoulder_plane_angle > 5:  # Outside-in path

            errors.append(ErrorDetection(

                error='over_the_top',

                severity='major',

                confidence=0.88,

                data={

                    'plane_deviation': metrics.shoulder_plane_angle

                }

            ))

 

        return errors

```

 

**Audio Feedback:**

 

```python

# app/services/audio_coach.py

 

class AudioCoach:

    """Generate and deliver audio coaching cues"""

 

    def __init__(self):

        self.tts_client = ElevenLabsClient()

        self.cache = AudioCache()

 

    async def generate_coaching_cue(

        self,

        error: ErrorDetection,

        user_id: int

    ) -> AudioCue:

        """

        Generate audio coaching cue for detected error

        """

        # Get coaching text based on error

        text = self.get_coaching_text(error, user_id)

 

        # Check cache first

        cache_key = f"audio:{error.error}:{text}"

        if cached := await self.cache.get(cache_key):

            return AudioCue(

                text=text,

                audio_url=cached,

                cached=True

            )

 

        # Generate with TTS

        audio_data = await self.tts_client.generate(

            text=text,

            voice='coaching_voice',

            stability=0.7,

            similarity_boost=0.8

        )

 

        # Upload to CDN

        audio_url = await upload_to_cdn(audio_data)

 

        # Cache for future use

        await self.cache.set(cache_key, audio_url, ttl=86400)

 

        return AudioCue(

            text=text,

            audio_url=audio_url,

            cached=False

        )

 

    def get_coaching_text(

        self,

        error: ErrorDetection,

        user_id: int

    ) -> str:

        """

        Get appropriate coaching text for error

 

        Considers:

        - User's learning style (visual, kinesthetic, analytical)

        - Error frequency (new issue vs recurring)

        - Session context (early in session vs late)

        """

        user = get_user_context(user_id)

 

        # Different cues for different learning styles

        cues = {

            'early_extension': {

                'visual': 'Stay bent over the ball',

                'kinesthetic': 'Feel like you\'re sitting in a chair',

                'analytical': 'Maintain spine angle - you lost 8 degrees'

            },

            'over_the_top': {

                'visual': 'Drop the club inside',

                'kinesthetic': 'Feel like you\'re skipping a stone',

                'analytical': 'Shallow your path - 5 degrees outside-in'

            }

        }

 

        learning_style = user.profile.learning_style or 'kinesthetic'

        return cues[error.error][learning_style]

```

 

### Data Flow

 

```

Mobile Camera (30 FPS)

    ↓ WebRTC stream

Backend receives frame

    ↓ < 16ms processing

MediaPipe pose detection

    ↓

Biomechanics calculation

    ↓

Swing phase detection

    ↓

Error detection

    ↓ WebSocket

Mobile renders skeleton overlay (60 FPS)

Mobile displays metrics

    ↓ If error detected

Generate audio cue

    ↓ WebSocket

Mobile plays audio through AirPods

```

 

## UI/UX Design

 

### Main Screen Layout

 

```

┌─────────────────────────────────────┐

│  [◀] Live Practice        [⚙️] [X]  │ Header

├─────────────────────────────────────┤

│                                     │

│        📹 Camera View                │

│     with Skeleton Overlay           │

│                                     │

│        [Pose visualization]         │

│                                     │

│   Spine: 38° | Hip: 45° | X: 43°   │ Metrics overlay

│                                     │

├─────────────────────────────────────┤

│  ● RECORDING    00:15:32    🔊 8    │ Status bar

├─────────────────────────────────────┤

│  Phase: BACKSWING                   │

│  Swings: 15    Last: 7.5/10         │ Info panel

├─────────────────────────────────────┤

│  [⏸ Pause]  [💾 Save & End]         │ Controls

└─────────────────────────────────────┘

```

 

### Calibration Screen

 

```

┌─────────────────────────────────────┐

│  Position Setup                     │

│                                     │

│    ┌─────────────────┐              │

│    │                 │              │

│    │   [Silhouette]  │              │

│    │   of golfer     │              │

│    │                 │              │

│    └─────────────────┘              │

│                                     │

│  ✓ Camera angle: Correct            │

│  ✓ Distance: Correct                │

│  ⚠️ Lighting: Adjust brighter        │

│  ✓ Full body visible                │

│                                     │

│  [Start Practice Session]           │

└─────────────────────────────────────┘

```

 

### Session Summary

 

```

┌─────────────────────────────────────┐

│  Practice Session Complete! 🎉      │

├─────────────────────────────────────┤

│  Duration: 23 minutes               │

│  Swings: 18                         │

│  Average Score: 7.2/10              │

├─────────────────────────────────────┤

│  Key Insights:                      │

│  • Improved spine angle (+3°)       │

│  • Consistent tempo                 │

│  • Still working on early extension │

├─────────────────────────────────────┤

│  Recommended Next Steps:            │

│  1. Wall drill (5 minutes)          │

│  2. Focus on finish position        │

├─────────────────────────────────────┤

│  [View All Swings]  [Share]  [Done] │

└─────────────────────────────────────┘

```

 

## Settings & Configuration

 

**Audio Settings:**

- Feedback frequency: All swings | Major errors only | Off

- Voice: Male | Female | Neutral

- Volume: 1-10

- Output: Phone speaker | AirPods | Bluetooth

 

**Display Settings:**

- Skeleton overlay: On | Off

- Metrics display: Full | Minimal | Off

- Phase indicator: On | Off

- Grid lines: On | Off

 

**Session Settings:**

- Auto-save swings: All | Good only (7+) | Manual

- Video quality: High | Medium | Low (battery)

- Camera angle: Face-on | Down-the-line

- Focus areas: Select specific issues to monitor

 

## Error States

 

### Poor Connection

```

┌─────────────────────────────────────┐

│  ⚠️ Connection Quality: Poor         │

│                                     │

│  Real-time analysis may be delayed. │

│                                     │

│  [Switch to Offline Mode]           │

│  [Continue Anyway]                  │

└─────────────────────────────────────┘

```

 

### Camera Blocked

```

┌─────────────────────────────────────┐

│  📷 Camera Blocked                   │

│                                     │

│  Unable to detect your position.    │

│  Please ensure full body is visible.│

│                                     │

│  [Adjust Position]                  │

└─────────────────────────────────────┘

```

 

### Low Battery

```

┌─────────────────────────────────────┐

│  🔋 Battery Low (15%)                │

│                                     │

│  Switch to Battery Saver mode?      │

│  (Reduces video quality)            │

│                                     │

│  [Switch]  [Continue]               │

└─────────────────────────────────────┘

```

 

## Performance Requirements

 

### Latency

- Pose detection: < 10ms per frame

- Error detection: < 5ms

- WebSocket roundtrip: < 50ms

- Audio cue generation: < 200ms

- Total latency (swing to feedback): < 100ms

 

### Accuracy

- Pose detection accuracy: > 95%

- Error detection precision: > 90%

- False positive rate: < 10%

 

### Battery Life

- Target: 45+ minutes continuous use

- Strategies:

  - Adaptive frame rate (30 FPS → 15 FPS on low battery)

  - Reduce video quality automatically

  - Disable non-essential features

  - Show battery warning at 20%

 

## Privacy & Security

 

### Data Handling

- Real-time video NOT stored on servers (client-side only)

- Only saved swings uploaded to cloud

- Pose data (keypoints) stored, not raw video frames

- User can delete sessions anytime

 

### Permissions

- Camera: Required for video capture

- Microphone: Optional for audio notes

- Location: Optional for range/course tagging

- Bluetooth: Optional for AirPods

 

## Testing Strategy

 

### Unit Tests

- Pose detection accuracy

- Biomechanics calculations

- Error detection logic

- Audio cue generation

 

### Integration Tests

- WebSocket connection handling

- Video streaming pipeline

- End-to-end latency

- Concurrent user handling

 

### Performance Tests

- Load testing (100+ concurrent sessions)

- Latency under poor network

- Battery drain measurement

- Memory leak detection

 

### User Acceptance Tests

- Setup flow completion rate

- Session duration

- Audio feedback clarity

- Overall satisfaction

 

## Launch Plan

 

### Phase 1: Private Beta (Week 1-2)

- 20 selected users

- Collect feedback on:

  - Setup experience

  - Audio feedback quality

  - Latency perception

  - Battery life

 

### Phase 2: Pro Tier Beta (Week 3-4)

- Roll out to all Pro tier users

- Monitor metrics:

  - Adoption rate

  - Session completion

  - Error rates

  - Support tickets

 

### Phase 3: General Release (Week 5+)

- Feature available to all users (Pro+ tier)

- Marketing campaign

- Tutorial content

- In-app promotion

 

## Future Enhancements

 

### v1.1

- Multiple camera angles simultaneously

- Swing comparison overlay (your swing vs pro)

- Custom coaching voice (upload your coach's voice)

 

### v1.2

- AR overlay on real environment

- Club tracking (detect which club in use)

- Ball flight tracking and prediction

 

### v1.3

- Group practice mode (multiple golfers)

- Competitive challenges

- Social sharing of practice highlights

 

---

 

**Questions or feedback?** Contact: product@golfcoachpro.com
