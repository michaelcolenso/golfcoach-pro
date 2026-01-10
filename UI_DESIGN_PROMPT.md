# UI Design Prompt for GolfCoach Pro

## Mission

Design a **premium, pro-grade** mobile-first UI/UX for GolfCoach Pro - an AI-powered golf coaching application that provides real-time swing analysis. This is the "Tiger Woods version" of golf coaching software.

## Design Philosophy

### Core Principles

1. **Mobile-First, Range-Ready**
   - Golfers use this outdoors, in bright sunlight
   - One-handed operation while holding clubs
   - Large touch targets (minimum 44x44px)
   - High contrast for outdoor visibility
   - Quick access to camera and analysis

2. **Pro-Grade, Not Gamified**
   - Serious tool for serious golfers
   - Data-driven, not trophy-driven
   - Clean, focused, professional aesthetic
   - Think "Bloomberg Terminal for Golf" not "Candy Crush for Golf"

3. **Real-Time First**
   - Immediate feedback is critical
   - Show progress, not loading spinners
   - Streaming data visualization
   - Smooth 60 FPS animations

4. **Information Density Without Clutter**
   - Golfers want detailed biomechanical data
   - Use progressive disclosure (basics → advanced)
   - Charts, graphs, 3D visualizations
   - Collapsible sections for deep analysis

5. **Privacy and Professionalism**
   - Swing videos are personal
   - Clear privacy controls
   - Professional sharing options (coach, trainer)
   - No social media gimmicks

## Target Users

### Primary Persona: "Competitive Chris"
- **Age:** 28-45
- **Handicap:** 5-15
- **Goals:** Lower handicap, compete in club tournaments
- **Tech Savvy:** High (uses TrackMan, Arccos, Apple Watch)
- **Budget:** Willing to pay premium for quality coaching
- **Pain Points:**
  - Can't afford regular lessons ($150/hour)
  - Needs immediate feedback during practice
  - Wants to track improvement over time
  - Struggles to remember coach's feedback

### Secondary Persona: "Elite Emma"
- **Age:** 22-35
- **Level:** College golfer / Tour aspirant
- **Goals:** Professional-level swing mechanics
- **Tech Savvy:** Very high
- **Budget:** Cost is secondary to results
- **Pain Points:**
  - Needs frame-by-frame biomechanical analysis
  - Requires integration with TrackMan, K-Vest data
  - Wants to share swings with coach remotely
  - Needs to compare swings to tour pros

### Tertiary Persona: "Coach Carlos"
- **Age:** 35-60
- **Role:** Golf instructor with 10-50 students
- **Goals:** Monitor students remotely, provide async feedback
- **Tech Savvy:** Medium to high
- **Budget:** Subscription model for coaching business
- **Pain Points:**
  - Can't watch every student practice
  - Needs to review multiple swings efficiently
  - Wants to send video feedback with annotations
  - Requires progress tracking dashboard

## Key Screens & User Flows

### 1. Onboarding Flow (First-Time User)

**Screens:**
1. **Welcome Splash**
   - Hero image: Professional golfer mid-swing
   - Value proposition: "AI-Powered Coaching, On Demand"
   - CTA: "Get Started" or "Sign In"

2. **Profile Setup**
   - Name, email, password
   - Handicap (dropdown: +5 to 28+)
   - Primary goal (dropdown: Lower handicap, Fix slice, Increase distance, etc.)
   - Swing hand (Right/Left)
   - Upload profile photo (optional)

3. **Camera Permissions**
   - Clear explanation: "We need camera access to analyze your swing"
   - Show sample swing video being analyzed
   - Grant permission CTA

4. **Recording Setup Guide**
   - Interactive tutorial: "How to record your swing"
   - Down-the-line vs. Face-on camera angles (diagrams)
   - Distance from camera (6-10 feet)
   - Tripod/phone holder recommendations
   - Skip option for experienced users

5. **First Swing Analysis**
   - Guided recording of first swing
   - Real-time pose detection preview
   - "Analyzing..." with progress (not just spinner)
   - Results with celebration for completion

### 2. Home / Dashboard Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  ☰  GolfCoach Pro          🔔  👤  │  Header
├─────────────────────────────────────┤
│                                     │
│  Good morning, Chris! 👋            │  Personalization
│  You've practiced 3 times this week │
│                                     │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │   📹 Record New Swing       │   │  Primary CTA
│  │   (Large, prominent button) │   │
│  └─────────────────────────────┘   │
├─────────────────────────────────────┤
│  Quick Stats (This Week)            │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │  Stats Cards
│  │ 12  │ │ 85% │ │ 3°  │ │ 4.2 │  │
│  │Swing│ │Club │ │Tilt │ │ mi  │  │
│  │  s  │ │Path │ │Impr.│ │Drive│  │
│  └─────┘ └─────┘ └─────┘ └─────┘  │
├─────────────────────────────────────┤
│  Recent Swings                      │  Recent List
│  ┌───────────────────────────────┐ │
│  │ 🎬 Driver - 2 hours ago       │ │
│  │ Score: B+ | View Analysis →  │ │
│  └───────────────────────────────┘ │
│  ┌───────────────────────────────┐ │
│  │ 🎬 7-Iron - Yesterday         │ │
│  │ Score: A- | View Analysis →  │ │
│  └───────────────────────────────┘ │
│                                     │
│  View All Swings →                  │
├─────────────────────────────────────┤
│  Recommended Drills                 │  AI Suggestions
│  ┌───────────────────────────────┐ │
│  │ 🎯 Fix Outside-In Swing Path  │ │
│  │ Based on your last 5 swings   │ │
│  │ Start Drill →                 │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
   ── Home ── Swings ── Progress ──    Bottom Nav
```

**Design Notes:**
- Use card-based layout for easy scanning
- Primary CTA (Record Swing) should be unmissable
- Stats should update in real-time
- Pull-to-refresh for new data

### 3. Record Swing Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  ✕                             ⚙️  │  Close | Settings
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │     CAMERA VIEWFINDER       │   │  Camera Feed
│  │                             │   │  with overlay
│  │     [Skeleton overlay]      │   │
│  │                             │   │
│  │     ┌─────────────────┐     │   │
│  │     │   Align body    │     │   │  Guide
│  │     │   in frame      │     │   │
│  │     └─────────────────┘     │   │
│  │                             │   │
│  └─────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│  Angle: Down-the-line ▼             │  Camera Angle
├─────────────────────────────────────┤
│  Club: Driver ▼                     │  Club Selection
├─────────────────────────────────────┤
│                                     │
│       ┌─────────────────┐           │
│       │   ⏺ RECORD      │           │  Record Button
│       │  (Large, red)   │           │
│       └─────────────────┘           │
│                                     │
│  [Real-Time Mode] [Upload Video]   │  Mode Toggle
└─────────────────────────────────────┘
```

**Features:**
- Real-time pose detection overlay (skeleton)
- Alignment guides (vertical/horizontal lines)
- Camera angle selector (Down-the-line, Face-on, Behind, Front)
- Club selector (Driver, 3W, 5W, Hybrids, Irons, Wedges, Putter)
- Real-time mode vs. Upload mode toggle
- Recording timer (countdown 3-2-1 before recording)
- Instant replay after recording

### 4. Analysis Results Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  ← Back              Share 📤       │  Navigation
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │   VIDEO PLAYER              │   │  Video with
│  │   [Swing video]             │   │  scrubber
│  │   ═══●══════════════════    │   │
│  │   0:00 / 0:03               │   │
│  │                             │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Play] [Slow-Mo] [Frame-by-Frame] │  Playback
├─────────────────────────────────────┤
│  Overall Score: A-                  │  Grade
│  ★★★★☆                             │
├─────────────────────────────────────┤
│  AI Coach Feedback                  │
│  ┌───────────────────────────────┐ │
│  │ 💬 "Your swing path is        │ │  Claude
│  │ excellent, but you're tilting │ │  Analysis
│  │ 5° too much at address.       │ │
│  │ This is causing inconsistent  │ │
│  │ contact. See details below ↓" │ │
│  └───────────────────────────────┘ │
├─────────────────────────────────────┤
│  ── Biomechanics ── Comparison ──   │  Tabs
│                                     │
│  Key Metrics                        │
│  ┌─────────────────┬─────┬─────┐  │
│  │ Club Path       │ -2° │  ✓  │  │  Metrics
│  │ Face Angle      │ 1°  │  ✓  │  │  Table
│  │ Attack Angle    │ -3° │  ⚠  │  │
│  │ Body Tilt       │ 34° │  ✗  │  │
│  │ Hip Rotation    │ 45° │  ✓  │  │
│  └─────────────────┴─────┴─────┘  │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  Swing Plane Visualization    │ │  3D
│  │  [3D skeleton animation]      │ │  Viz
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  📊 Angle Graphs              │ │  Charts
│  │  [Time-series charts]         │ │
│  └───────────────────────────────┘ │
│                                     │
│  Recommendations                    │
│  • Practice with alignment stick    │  Action
│  • Focus on setup tilt              │  Items
│  • Record face-on view next         │
│                                     │
│  [Save to Library] [Start Drill]   │  CTAs
└─────────────────────────────────────┘
```

**Key Features:**
- Video player with frame-by-frame scrubbing
- Side-by-side comparison (pro swing vs. user)
- Overlay of skeleton/swing plane on video
- Annotated key frames (address, top, impact, follow-through)
- Expandable metrics sections
- Export options (PDF report, video with annotations)

### 5. Swing Library Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  Swing Library        🔍  ⚙️        │  Header
├─────────────────────────────────────┤
│  ┌─────┬─────┬─────┬─────┬─────┐  │
│  │ All │Driver│Irons│Wedge│Short│  │  Filter Tabs
│  └─────┴─────┴─────┴─────┴─────┘  │
├─────────────────────────────────────┤
│  Sort: Most Recent ▼                │  Sort/Filter
│  View: Grid ▢  List ☰              │
├─────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────┐  │
│  │ [Thumb] │ │ [Thumb] │ │[Thb]│  │  Grid View
│  │ Driver  │ │ 7-Iron  │ │ PW  │  │  (3 columns)
│  │  A-     │ │   B+    │ │  A  │  │
│  │ 2h ago  │ │ 1d ago  │ │ 3d  │  │
│  └─────────┘ └─────────┘ └─────┘  │
│                                     │
│  ┌─────────┐ ┌─────────┐ ┌─────┐  │
│  │ [Thumb] │ │ [Thumb] │ │[Thb]│  │
│  │ Driver  │ │ 5-Iron  │ │ SW  │  │
│  │   B     │ │   A-    │ │  B+ │  │
│  │ 1 wk    │ │ 1 wk    │ │ 2wk │  │
│  └─────────┘ └─────────┘ └─────┘  │
│                                     │
│  [Load More...]                     │
└─────────────────────────────────────┘
```

**Features:**
- Filter by club type, date range, score
- Search by notes/tags
- Batch actions (compare, delete)
- Export multiple swings
- Create collections/playlists

### 6. Progress / Analytics Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  Progress             📅 This Month │  Header
├─────────────────────────────────────┤
│  Practice Streak: 🔥 12 days        │  Gamification
├─────────────────────────────────────┤
│  Overall Improvement                │
│  ┌───────────────────────────────┐ │
│  │  📈 Trend Graph               │ │  Main Chart
│  │  [Line chart showing scores]  │ │
│  │  Time → A to B+ average       │ │
│  └───────────────────────────────┘ │
├─────────────────────────────────────┤
│  Key Metrics Over Time              │
│  ┌─────┬─────┬─────┬─────┐        │  Metric
│  │Club │Face │Atk  │Body │        │  Cards
│  │Path │Angle│Angle│Tilt │        │
│  │ ↑   │  →  │  ↓  │  ↑  │        │
│  │+3%  │ 0%  │-2%  │+5%  │        │
│  └─────┴─────┴─────┴─────┘        │
├─────────────────────────────────────┤
│  Breakdown by Club                  │
│  ┌───────────────────────────────┐ │
│  │  📊 Bar Chart                 │ │  Club
│  │  Driver: A-  (avg)            │ │  Performance
│  │  Irons:  B+                   │ │
│  │  Wedges: A                    │ │
│  └───────────────────────────────┘ │
├─────────────────────────────────────┤
│  Goals                              │
│  ☑ Reduce club path variance        │  Goal
│  ☐ Maintain 45° hip rotation        │  Tracking
│  ☐ Record 50 swings this month      │
│                                     │
│  [Set New Goal]                     │
└─────────────────────────────────────┘
```

**Features:**
- Time-based views (Week, Month, Quarter, Year, All Time)
- Metric-specific deep dives (tap any metric to see detail)
- Goal setting and tracking
- Export progress reports
- Share achievements

### 7. Real-Time Analysis Mode

**Special Screen for Live Practice (see REAL_TIME_ANALYSIS.md)**

```
┌─────────────────────────────────────┐
│  ✕ Exit Real-Time Mode              │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │     LIVE CAMERA FEED        │   │  Camera
│  │     [Skeleton overlay]      │   │  with
│  │     [Swing plane overlay]   │   │  real-time
│  │                             │   │  analysis
│  └─────────────────────────────┘   │
│                                     │
│  Live Metrics (Updates per frame)  │
│  ┌─────┬─────┬─────┬─────┐        │
│  │Club │Face │Atk  │Body │        │  Real-time
│  │Path │Angle│Angle│Tilt │        │  Metrics
│  │ -2° │ +1° │ -3° │ 34° │        │  (60 FPS)
│  │  ✓  │  ✓  │  ⚠  │  ✗  │        │
│  └─────┴─────┴─────┴─────┘        │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 💬 "Tilt back 3° at address" │ │  Live
│  └───────────────────────────────┘ │  Coaching
│                                     │
│  Swings This Session: 8             │  Session
│  Average Score: B+                  │  Stats
│                                     │
│  [End Session] [Save Highlights]   │
└─────────────────────────────────────┘
```

**Critical Requirements:**
- Sub-100ms latency for pose detection
- Real-time visual feedback (green/yellow/red indicators)
- Voice feedback option (optional audio cues)
- Session summary after practice
- Auto-save best swings

### 8. Settings & Profile

**Sections:**
- **Account**: Email, password, subscription
- **Profile**: Name, handicap, goals, photo
- **Camera Settings**: Default angle, resolution, framerate
- **Analysis Preferences**: Metric visibility, AI verbosity, comparison pro
- **Integrations**: TrackMan, Arccos, Apple Health
- **Privacy**: Video sharing, data export, account deletion
- **Notifications**: Push settings, email digest
- **Help & Support**: FAQs, tutorial videos, contact support

## Design System

### Color Palette

**Primary Colors:**
- **Golf Green**: `#2D5016` (dark green, professional)
- **Fairway Green**: `#4A7C2E` (medium green, accents)
- **Grass Green**: `#6B9D4D` (light green, highlights)

**Accent Colors:**
- **Gold Medal**: `#D4AF37` (achievements, premium features)
- **Sky Blue**: `#4A90E2` (links, interactive elements)
- **Sunset Orange**: `#F57C00` (warnings, attention)

**Neutral Colors:**
- **Charcoal**: `#1A1A1A` (primary text)
- **Slate Gray**: `#424242` (secondary text)
- **Light Gray**: `#E0E0E0` (borders, dividers)
- **Off-White**: `#F5F5F5` (backgrounds)
- **Pure White**: `#FFFFFF` (cards, surfaces)

**Feedback Colors:**
- **Success Green**: `#4CAF50`
- **Warning Orange**: `#FF9800`
- **Error Red**: `#F44336`
- **Info Blue**: `#2196F3`

**Score/Grade Colors:**
- **A Grade**: `#4CAF50` (Excellent)
- **B Grade**: `#8BC34A` (Good)
- **C Grade**: `#FFC107` (Average)
- **D Grade**: `#FF9800` (Needs Work)
- **F Grade**: `#F44336` (Poor)

### Typography

**Primary Font**: **Inter** or **SF Pro** (system font for iOS/Android)
- Clean, readable, professional
- Excellent at small sizes
- Wide range of weights

**Hierarchy:**
- **H1**: 32px, Bold, Charcoal
- **H2**: 24px, Semibold, Charcoal
- **H3**: 20px, Semibold, Charcoal
- **Body**: 16px, Regular, Charcoal
- **Small**: 14px, Regular, Slate Gray
- **Caption**: 12px, Regular, Slate Gray

**Data/Numbers Font**: **JetBrains Mono** or **SF Mono**
- For metrics, angles, measurements
- Monospace for alignment
- 14-18px depending on context

### Spacing & Layout

**Base Unit**: 8px (all spacing should be multiples of 8)
- **XS**: 4px
- **S**: 8px
- **M**: 16px
- **L**: 24px
- **XL**: 32px
- **XXL**: 48px

**Card Padding**: 16px
**Screen Padding**: 16px (mobile), 24px (tablet)
**Between Cards**: 16px vertical gap

### Components

**Buttons:**
- **Primary**: Golf Green background, white text, 48px height, 16px padding
- **Secondary**: White background, Golf Green border/text, 48px height
- **Tertiary**: Text only, no background, Golf Green text
- **Destructive**: Error Red background, white text

**Cards:**
- White background
- 8px border radius
- Subtle shadow: `0 2px 4px rgba(0,0,0,0.1)`
- 16px padding

**Input Fields:**
- Light Gray border, 1px
- 8px border radius
- 48px height
- 16px horizontal padding
- Focus: Sky Blue border

**Navigation:**
- **Bottom Tab Bar**: 5 items max
  - Home, Swings, Record (center, prominent), Progress, Profile
- **Top Navigation**: Back arrow, title, actions

### Icons

**Icon Set**: Use **Feather Icons** or **SF Symbols**
- Consistent stroke width (2px)
- 24px default size
- 32px for primary actions

**Custom Icons Needed:**
- Golf club types (Driver, woods, irons, wedges, putter)
- Swing phases (Address, backswing, downswing, impact, follow-through)
- Biomechanical angles (shoulder, hip, spine)

### Animations

**Timing:**
- **Fast**: 200ms (micro-interactions)
- **Normal**: 300ms (page transitions)
- **Slow**: 500ms (complex animations)

**Easing:**
- **Standard**: `cubic-bezier(0.4, 0.0, 0.2, 1)`
- **Decelerate**: `cubic-bezier(0.0, 0.0, 0.2, 1)`
- **Accelerate**: `cubic-bezier(0.4, 0.0, 1, 1)`

**Key Animations:**
- Page transitions: Slide in from right
- Modal dialogs: Fade in + scale from 0.95 to 1.0
- Loading states: Skeleton screens (not spinners)
- Success feedback: Checkmark with scale + fade animation

## Mobile Considerations

### iOS Specific
- Respect safe areas (notch, home indicator)
- Use iOS native bottom sheet for modals
- Haptic feedback on important actions
- Support Dynamic Type for accessibility

### Android Specific
- Material Design principles where appropriate
- Floating Action Button (FAB) for primary action
- Snackbar for feedback messages
- Respect system back button

### Performance
- Lazy load images (thumbnail → full resolution)
- Virtualized lists for long scrolling
- Optimize video playback (streaming, not full download)
- Cache analysis results locally

### Offline Support
- Show cached swings when offline
- Queue uploads for when online
- Clear offline mode indicator

## Web App Considerations

**Desktop Enhancements:**
- Multi-column layouts (sidebar + main content)
- Keyboard shortcuts (space = play/pause, arrow keys = frame-by-frame)
- Drag-and-drop video upload
- Side-by-side swing comparison
- Export options (PDF reports, CSV data)

**Responsive Breakpoints:**
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

## Accessibility (WCAG 2.1 AA)

**Requirements:**
- Color contrast ratios ≥ 4.5:1 for text
- Touch targets ≥ 44x44px
- Screen reader support (semantic HTML, ARIA labels)
- Keyboard navigation for web
- VoiceOver/TalkBack announcements for key actions
- Reduced motion option (respect `prefers-reduced-motion`)

**Video Accessibility:**
- Closed captions for coaching audio
- Text transcripts of AI feedback
- High contrast mode option

## Design Deliverables

### Phase 1: Core Mobile App

**Screens to Design (High-Fidelity):**
1. Onboarding flow (5 screens)
2. Home/Dashboard
3. Record Swing
4. Analysis Results
5. Swing Library
6. Progress/Analytics
7. Profile/Settings

**Components to Design:**
- Navigation (bottom tabs, top bars)
- Buttons (all variants)
- Cards
- Input fields
- Video player
- Charts/graphs
- 3D skeleton viewer

### Phase 2: Advanced Features

8. Real-Time Analysis Mode
9. Comparison View (side-by-side swings)
10. Drill Library
11. Coach Portal (for Coach Carlos persona)
12. Sharing/Export flows

### Phase 3: Web App

- Responsive versions of all mobile screens
- Desktop-specific layouts
- Export/report templates

## Design Tools & Assets

**Recommended Tools:**
- **Figma**: For UI design and prototyping
- **Principle/ProtoPie**: For complex animations
- **Lottie**: For lightweight animations

**Assets Needed:**
- Golf club illustrations
- Swing phase diagrams
- Skeleton/biomechanics overlays
- Sample swing videos
- Iconography set

## References & Inspiration

**Apps to Study:**
- **Sportsbox 3D Golf**: Industry leader in swing analysis
- **V1 Golf**: Professional coaching app
- **TrackMan**: Data-rich golf analytics
- **Whoop**: Premium fitness tracking UI
- **Peloton**: Real-time workout feedback
- **Bloomberg**: Information density without clutter

**Design Principles:**
- Apple Human Interface Guidelines
- Material Design (for Android)
- Nielsen Norman Group (UX research)

## Testing & Validation

**Usability Testing:**
- Test with real golfers (various skill levels)
- Outdoor testing (sunlight readability)
- One-handed operation testing
- Time-to-complete key tasks
- A/B test critical flows

**Success Metrics:**
- Time to record first swing: < 2 minutes
- Analysis comprehension rate: > 80%
- Feature discovery rate: > 60%
- Return user rate (Day 7): > 40%

## Next Steps

1. **Read Documentation**: Review ARCHITECTURE.md, API_SPEC.md, REAL_TIME_ANALYSIS.md
2. **User Research**: Validate personas with real golfers
3. **Wireframes**: Sketch low-fidelity layouts
4. **Design System**: Build component library in Figma
5. **High-Fidelity Mockups**: Design all Phase 1 screens
6. **Prototype**: Create interactive prototype for testing
7. **Usability Testing**: Test with 5-8 target users
8. **Iterate**: Refine based on feedback
9. **Developer Handoff**: Create design specs and assets

## Remember

> "This is a premium product for serious golfers. Every screen should feel polished, professional, and purposeful. We're building the tool Tiger Woods would want to use."

- **Quality over Quantity**: One excellent screen > Five mediocre screens
- **Data-Driven**: Show metrics that matter, hide the rest
- **Fast**: Every interaction should feel instant
- **Clear**: Golfer should never be confused
- **Beautiful**: Pro-grade doesn't mean boring

Good luck designing! 🏌️⛳
