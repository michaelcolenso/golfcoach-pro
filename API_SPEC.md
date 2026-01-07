# API Specification

 

## Overview

 

GolfCoach Pro REST API v1 - Complete API reference for golf swing analysis and coaching.

 

**Base URL:** `https://api.golfcoachpro.com/api/v1`

 

**Authentication:** Bearer token (JWT)

 

**Content-Type:** `application/json` (except file uploads)

 

## Authentication

 

### Register

 

Create a new user account.

 

```http

POST /auth/register

```

 

**Request Body:**

```json

{

  "email": "user@example.com",

  "password": "SecurePassword123!",

  "full_name": "John Doe"

}

```

 

**Response:** `201 Created`

```json

{

  "user": {

    "id": 1,

    "email": "user@example.com",

    "full_name": "John Doe",

    "created_at": "2026-01-07T10:00:00Z"

  },

  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",

  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",

  "token_type": "bearer",

  "expires_in": 900

}

```

 

**Errors:**

- `400 Bad Request`: Invalid input (weak password, invalid email)

- `409 Conflict`: Email already registered

 

---

 

### Login

 

Authenticate and receive access token.

 

```http

POST /auth/login

```

 

**Request Body:**

```json

{

  "email": "user@example.com",

  "password": "SecurePassword123!"

}

```

 

**Response:** `200 OK`

```json

{

  "user": {

    "id": 1,

    "email": "user@example.com",

    "full_name": "John Doe"

  },

  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",

  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",

  "token_type": "bearer",

  "expires_in": 900

}

```

 

**Errors:**

- `401 Unauthorized`: Invalid credentials

 

---

 

### Refresh Token

 

Get a new access token using refresh token.

 

```http

POST /auth/refresh

```

 

**Request Body:**

```json

{

  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."

}

```

 

**Response:** `200 OK`

```json

{

  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",

  "token_type": "bearer",

  "expires_in": 900

}

```

 

---

 

### Logout

 

Invalidate refresh token.

 

```http

POST /auth/logout

Authorization: Bearer {access_token}

```

 

**Request Body:**

```json

{

  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."

}

```

 

**Response:** `204 No Content`

 

---

 

## Users

 

### Get Current User

 

Retrieve authenticated user's profile.

 

```http

GET /users/me

Authorization: Bearer {access_token}

```

 

**Response:** `200 OK`

```json

{

  "id": 1,

  "email": "user@example.com",

  "full_name": "John Doe",

  "handicap": 12.5,

  "profile": {

    "date_of_birth": "1990-05-15",

    "height_cm": 180,

    "weight_kg": 80,

    "dominant_hand": "right",

    "primary_miss": "slice",

    "goals": ["Lower handicap to 10", "Fix driver slice"],

    "physical_limitations": []

  },

  "created_at": "2026-01-01T10:00:00Z",

  "updated_at": "2026-01-07T10:00:00Z"

}

```

 

---

 

### Update User Profile

 

Update user information.

 

```http

PATCH /users/me

Authorization: Bearer {access_token}

```

 

**Request Body:**

```json

{

  "full_name": "John Smith",

  "handicap": 11.0,

  "profile": {

    "goals": ["Break 80", "Fix driver slice"],

    "primary_miss": "push"

  }

}

```

 

**Response:** `200 OK`

```json

{

  "id": 1,

  "email": "user@example.com",

  "full_name": "John Smith",

  "handicap": 11.0,

  "profile": {

    "goals": ["Break 80", "Fix driver slice"],

    "primary_miss": "push"

  },

  "updated_at": "2026-01-07T11:00:00Z"

}

```

 

---

 

### Get User Statistics

 

Retrieve user's golf statistics.

 

```http

GET /users/{user_id}/stats

Authorization: Bearer {access_token}

```

 

**Query Parameters:**

- `period`: `week` | `month` | `year` | `all` (default: `month`)

 

**Response:** `200 OK`

```json

{

  "user_id": 1,

  "period": "month",

  "swings_analyzed": 45,

  "average_score": 7.8,

  "improvement_trend": "improving",

  "most_common_issues": [

    {

      "issue": "early_extension",

      "count": 23,

      "percentage": 51.1

    },

    {

      "issue": "over_the_top",

      "count": 12,

      "percentage": 26.7

    }

  ],

  "biomechanics_avg": {

    "spine_angle": 38.5,

    "hip_rotation": 52.3,

    "shoulder_turn": 95.7,

    "x_factor": 43.4

  },

  "drills_completed": 8,

  "practice_sessions": 12

}

```

 

---

 

## Swings

 

### Upload Swing Video

 

Upload a golf swing video for analysis.

 

```http

POST /swings/upload

Authorization: Bearer {access_token}

Content-Type: multipart/form-data

```

 

**Request Body (multipart/form-data):**

```

video: <file> (MP4, MOV, max 100MB)

club: "driver" (optional)

intended_shape: "straight" (optional)

notes: "Working on backswing" (optional)

```

 

**Response:** `202 Accepted`

```json

{

  "swing_id": 123,

  "status": "PROCESSING",

  "message": "Video uploaded successfully. Analysis in progress.",

  "estimated_time_seconds": 30

}

```

 

**Errors:**

- `400 Bad Request`: Invalid file format or size

- `413 Payload Too Large`: File > 100MB

- `429 Too Many Requests`: Rate limit exceeded

 

---

 

### List User Swings

 

Get paginated list of user's swings.

 

```http

GET /swings

Authorization: Bearer {access_token}

```

 

**Query Parameters:**

- `page`: Page number (default: 1)

- `limit`: Items per page (default: 20, max: 100)

- `club`: Filter by club (e.g., "driver", "7-iron")

- `date_from`: Filter by date (ISO 8601)

- `date_to`: Filter by date (ISO 8601)

- `sort`: `date_desc` | `date_asc` | `score_desc` | `score_asc` (default: `date_desc`)

 

**Response:** `200 OK`

```json

{

  "swings": [

    {

      "id": 123,

      "recorded_at": "2026-01-07T14:30:00Z",

      "club_type": "driver",

      "intended_shape": "straight",

      "duration_ms": 2500,

      "thumbnail_url": "https://cdn.golfcoachpro.com/thumbs/123.jpg",

      "status": "COMPLETED",

      "has_analysis": true,

      "overall_score": 7.5

    }

  ],

  "pagination": {

    "page": 1,

    "limit": 20,

    "total_items": 45,

    "total_pages": 3,

    "has_next": true,

    "has_prev": false

  }

}

```

 

---

 

### Get Swing Details

 

Retrieve detailed information about a specific swing.

 

```http

GET /swings/{swing_id}

Authorization: Bearer {access_token}

```

 

**Response:** `200 OK`

```json

{

  "id": 123,

  "user_id": 1,

  "recorded_at": "2026-01-07T14:30:00Z",

  "club_type": "driver",

  "intended_shape": "straight",

  "video_url": "https://cdn.golfcoachpro.com/videos/123.mp4?signature=...",

  "thumbnail_url": "https://cdn.golfcoachpro.com/thumbs/123.jpg",

  "duration_ms": 2500,

  "status": "COMPLETED",

  "metadata": {

    "resolution": "1920x1080",

    "fps": 60,

    "file_size_bytes": 15728640

  }

}

```

 

**Errors:**

- `404 Not Found`: Swing doesn't exist or user doesn't have access

 

---

 

### Delete Swing

 

Delete a swing and its analysis.

 

```http

DELETE /swings/{swing_id}

Authorization: Bearer {access_token}

```

 

**Response:** `204 No Content`

 

---

 

### Get Swing Video

 

Get signed URL for video playback.

 

```http

GET /swings/{swing_id}/video

Authorization: Bearer {access_token}

```

 

**Query Parameters:**

- `quality`: `high` | `medium` | `low` (default: `high`)

 

**Response:** `200 OK`

```json

{

  "video_url": "https://cdn.golfcoachpro.com/videos/123-high.mp4?signature=...",

  "expires_at": "2026-01-07T15:00:00Z",

  "duration_ms": 2500,

  "resolution": "1920x1080"

}

```

 

---

 

### Get Swing Frames

 

Get key frames from the swing.

 

```http

GET /swings/{swing_id}/frames

Authorization: Bearer {access_token}

```

 

**Response:** `200 OK`

```json

{

  "frames": [

    {

      "frame_number": 0,

      "timestamp_ms": 0,

      "phase": "ADDRESS",

      "image_url": "https://cdn.golfcoachpro.com/frames/123/0.jpg",

      "biomechanics": {

        "spine_angle": 40.5,

        "hip_rotation": 0,

        "shoulder_turn": 0

      }

    },

    {

      "frame_number": 45,

      "timestamp_ms": 750,

      "phase": "BACKSWING",

      "image_url": "https://cdn.golfcoachpro.com/frames/123/45.jpg",

      "biomechanics": {

        "spine_angle": 38.2,

        "hip_rotation": 45.3,

        "shoulder_turn": 92.1

      }

    }

  ]

}

```

 

---

 

## Analysis

 

### Get Swing Analysis

 

Retrieve analysis results for a swing.

 

```http

GET /swings/{swing_id}/analysis

Authorization: Bearer {access_token}

```

 

**Response:** `200 OK`

```json

{

  "swing_id": 123,

  "analyzed_at": "2026-01-07T14:31:00Z",

  "model_version": "claude-opus-4.5-v1",

  "processing_time_ms": 28500,

 

  "swing_phases": [

    {

      "phase": "ADDRESS",

      "frame_number": 0,

      "timestamp_ms": 0,

      "observations": [

        "Good athletic stance with slight knee flex",

        "Spine angle at 40 degrees - excellent",

        "Arms hanging naturally"

      ],

      "quality_score": 8.5

    },

    {

      "phase": "BACKSWING",

      "frame_number": 45,

      "timestamp_ms": 750,

      "observations": [

        "Full shoulder turn achieved (92 degrees)",

        "Slight early wrist hinge noticed",

        "Good weight shift to trail side"

      ],

      "quality_score": 7.0

    },

    {

      "phase": "IMPACT",

      "frame_number": 90,

      "timestamp_ms": 1500,

      "observations": [

        "Early extension detected",

        "Loss of spine angle at impact",

        "Hands slightly ahead of ball - good"

      ],

      "quality_score": 6.5

    }

  ],

 

  "technical_analysis": {

    "positives": [

      "Excellent setup position with athletic posture",

      "Full shoulder turn in backswing",

      "Good tempo and rhythm",

      "Hands ahead at impact"

    ],

    "issues": [

      {

        "issue": "Early extension at impact",

        "severity": "major",

        "impact": "Leads to inconsistent contact and loss of power",

        "biomechanical_cause": "Hips thrusting toward ball causing loss of spine angle"

      },

      {

        "issue": "Early wrist hinge in takeaway",

        "severity": "minor",

        "impact": "Can lead to timing issues and inconsistent club face control",

        "biomechanical_cause": "Wrists hinging before shoulders complete turn"

      }

    ]

  },

 

  "recommendations": [

    {

      "priority": 1,

      "change": "Fix early extension at impact",

      "why": "Causing 60% of your mishits and losing 15 yards of distance",

      "how": "Practice maintaining spine angle through impact. Feel like you're staying in your posture.",

      "drill_id": 42,

      "expected_improvement": "More consistent contact, 10-15 yards added distance"

    },

    {

      "priority": 2,

      "change": "Delay wrist hinge in takeaway",

      "why": "Will improve timing and create more width in backswing",

      "how": "Keep triangle formed by arms and shoulders intact longer in takeaway",

      "drill_id": 18,

      "expected_improvement": "Better timing, more consistent ball striking"

    }

  ],

 

  "biomechanics": {

    "address": {

      "spine_angle": 40.5,

      "hip_rotation": 0,

      "shoulder_turn": 0

    },

    "top_of_backswing": {

      "spine_angle": 38.2,

      "hip_rotation": 45.3,

      "shoulder_turn": 92.1,

      "x_factor": 46.8

    },

    "impact": {

      "spine_angle": 32.1,

      "hip_rotation": -12.5,

      "shoulder_turn": 15.3,

      "weight_distribution": "70-30 (front-back)"

    }

  },

 

  "overall_feedback": "You have a solid foundation with good setup and shoulder turn. The main area to focus on is early extension - maintaining your spine angle through impact will dramatically improve consistency and add distance. Start with the wall drill and focus on the feeling of staying in your posture.",

 

  "coaching_cues": [

    "Maintain your spine angle through impact",

    "Feel like you're staying bent over the ball",

    "Keep your belt buckle pointing at the ground longer",

    "Push through your lead leg, not toward the ball"

  ],

 

  "overall_score": 7.5

}

```

 

**Errors:**

- `404 Not Found`: Analysis not found

- `202 Accepted`: Analysis still processing (includes estimated time)

 

---

 

### Reanalyze Swing

 

Trigger a new analysis with updated AI model or user context.

 

```http

POST /swings/{swing_id}/reanalyze

Authorization: Bearer {access_token}

```

 

**Request Body:**

```json

{

  "force": false,

  "focus_areas": ["driver", "power"]

}

```

 

**Response:** `202 Accepted`

```json

{

  "swing_id": 123,

  "status": "PROCESSING",

  "estimated_time_seconds": 25

}

```

 

---

 

### Compare Swings

 

Compare two swings side-by-side.

 

```http

GET /swings/{swing_id}/compare/{other_swing_id}

Authorization: Bearer {access_token}

```

 

**Response:** `200 OK`

```json

{

  "swing_a": {

    "id": 123,

    "recorded_at": "2026-01-07T14:30:00Z",

    "overall_score": 7.5

  },

  "swing_b": {

    "id": 120,

    "recorded_at": "2026-01-05T10:15:00Z",

    "overall_score": 6.8

  },

  "comparison": {

    "score_change": 0.7,

    "score_change_percentage": 10.3,

    "improvement_areas": [

      "Reduced early extension",

      "Better spine angle at impact"

    ],

    "regression_areas": [],

    "biomechanics_diff": {

      "spine_angle_at_impact": {

        "swing_a": 32.1,

        "swing_b": 28.5,

        "change": 3.6,

        "better": "swing_a"

      },

      "x_factor": {

        "swing_a": 46.8,

        "swing_b": 44.2,

        "change": 2.6,

        "better": "swing_a"

      }

    }

  },

  "synchronized_frames": [

    {

      "phase": "ADDRESS",

      "swing_a_frame": 0,

      "swing_b_frame": 0,

      "swing_a_image_url": "...",

      "swing_b_image_url": "..."

    }

  ],

  "coaching_feedback": "Great improvement! You've successfully reduced early extension, which is showing in better spine angle at impact. Keep focusing on the wall drill to maintain this improvement."

}

```

 

---

 

## Drills

 

### List All Drills

 

Get complete drill library.

 

```http

GET /drills

Authorization: Bearer {access_token}

```

 

**Query Parameters:**

- `difficulty`: `beginner` | `intermediate` | `advanced`

- `category`: `setup` | `backswing` | `downswing` | `impact` | `tempo` | `general`

 

**Response:** `200 OK`

```json

{

  "drills": [

    {

      "id": 42,

      "name": "Wall Drill for Early Extension",

      "description": "Practice maintaining spine angle through impact by using a wall as feedback.",

      "difficulty": "beginner",

      "category": "impact",

      "duration_minutes": 10,

      "video_url": "https://cdn.golfcoachpro.com/drills/42.mp4",

      "thumbnail_url": "https://cdn.golfcoachpro.com/drills/42-thumb.jpg",

      "instructions": [

        "Stand with your butt against a wall",

        "Take your setup position",

        "Make slow practice swings",

        "Focus on keeping contact with wall through impact"

      ],

      "targets": ["early_extension", "spine_angle"],

      "equipment_needed": ["Wall", "Golf club"]

    }

  ]

}

```

 

---

 

### Get Recommended Drills

 

Get personalized drill recommendations.

 

```http

GET /drills/recommended

Authorization: Bearer {access_token}

```

 

**Response:** `200 OK`

```json

{

  "recommendations": [

    {

      "drill": {

        "id": 42,

        "name": "Wall Drill for Early Extension",

        "difficulty": "beginner",

        "duration_minutes": 10

      },

      "priority": 1,

      "reason": "Addresses your most common issue (early extension) found in 51% of your swings",

      "expected_improvement": "Consistent spine angle will add 10-15 yards and improve contact",

      "sessions_recommended": 5

    }

  ],

  "practice_plan": {

    "weekly_sessions": 3,

    "session_duration_minutes": 30,

    "weeks_to_goal": 4

  }

}

```

 

---

 

### Mark Drill Complete

 

Log a completed drill session.

 

```http

POST /drills/{drill_id}/complete

Authorization: Bearer {access_token}

```

 

**Request Body:**

```json

{

  "duration_minutes": 15,

  "notes": "Felt good, focusing on the feeling really helped",

  "difficulty_rating": 3

}

```

 

**Response:** `201 Created`

```json

{

  "id": 567,

  "drill_id": 42,

  "user_id": 1,

  "completed_at": "2026-01-07T15:00:00Z",

  "duration_minutes": 15,

  "notes": "Felt good, focusing on the feeling really helped",

  "total_completions": 3

}

```

 

---

 

## Integrations

 

### List Connected Integrations

 

Get user's connected third-party integrations.

 

```http

GET /integrations

Authorization: Bearer {access_token}

```

 

**Response:** `200 OK`

```json

{

  "integrations": [

    {

      "provider": "trackman",

      "connected": true,

      "connected_at": "2026-01-01T10:00:00Z",

      "last_sync": "2026-01-07T14:00:00Z",

      "status": "active"

    },

    {

      "provider": "arccos",

      "connected": false

    }

  ]

}

```

 

---

 

### Connect Integration

 

Initiate OAuth flow for integration.

 

```http

POST /integrations/{provider}/connect

Authorization: Bearer {access_token}

```

 

**Response:** `200 OK`

```json

{

  "authorization_url": "https://trackman.com/oauth/authorize?client_id=...",

  "state": "random_state_token"

}

```

 

---

 

### Import Integration Data

 

Import data from connected integration.

 

```http

POST /integrations/{provider}/import

Authorization: Bearer {access_token}

```

 

**Request Body:**

```json

{

  "date_from": "2026-01-01",

  "date_to": "2026-01-07"

}

```

 

**Response:** `202 Accepted`

```json

{

  "import_id": 789,

  "status": "PROCESSING",

  "estimated_time_seconds": 10

}

```

 

---

 

## WebSocket API

 

### Connection

 

```

ws://api.golfcoachpro.com/api/v1/realtime/connect?token=JWT_TOKEN

```

 

### Events

 

#### Client → Server

 

**START_STREAM:**

```json

{

  "event": "START_STREAM",

  "data": {

    "camera": "front",

    "resolution": "1080p",

    "fps": 30

  }

}

```

 

**STOP_STREAM:**

```json

{

  "event": "STOP_STREAM"

}

```

 

**SAVE_SWING:**

```json

{

  "event": "SAVE_SWING",

  "data": {

    "start_timestamp": 1234567890,

    "end_timestamp": 1234570390

  }

}

```

 

#### Server → Client

 

**CONNECTED:**

```json

{

  "event": "CONNECTED",

  "data": {

    "session_id": "abc123",

    "user_id": 1

  }

}

```

 

**POSE_UPDATE:**

```json

{

  "event": "POSE_UPDATE",

  "data": {

    "timestamp": 1234567890,

    "landmarks": [

      {"x": 0.5, "y": 0.6, "z": -0.1, "visibility": 0.99},

      ...

    ],

    "angles": {

      "spine_angle": 38.5,

      "hip_rotation": 45.2,

      "shoulder_turn": 92.1

    },

    "swing_phase": "BACKSWING"

  }

}

```

 

**ERROR_DETECTED:**

```json

{

  "event": "ERROR_DETECTED",

  "data": {

    "error": "early_extension",

    "severity": "major",

    "coaching_cue": "Maintain your spine angle"

  }

}

```

 

**AUDIO_CUE:**

```json

{

  "event": "AUDIO_CUE",

  "data": {

    "text": "Keep your spine angle consistent",

    "audio_url": "https://cdn.golfcoachpro.com/audio/cues/123.mp3"

  }

}

```

 

**SWING_SAVED:**

```json

{

  "event": "SWING_SAVED",

  "data": {

    "swing_id": 124,

    "thumbnail_url": "..."

  }

}

```

 

---

 

## Rate Limiting

 

**Limits by tier:**

 

| Tier | Requests/minute | Uploads/day | Analysis/day |

|------|-----------------|-------------|--------------|

| Free | 60 | 5 | 5 |

| Pro | 120 | 100 | 100 |

| Elite | 300 | 500 | 500 |

 

**Headers:**

- `X-RateLimit-Limit`: Total requests allowed

- `X-RateLimit-Remaining`: Requests remaining

- `X-RateLimit-Reset`: Unix timestamp when limit resets

 

**Response on limit exceeded:**

```http

HTTP/1.1 429 Too Many Requests

Retry-After: 60

```

 

```json

{

  "error": "rate_limit_exceeded",

  "message": "Too many requests. Please try again in 60 seconds.",

  "retry_after": 60

}

```

 

---

 

## Error Responses

 

### Standard Error Format

 

```json

{

  "error": "error_code",

  "message": "Human-readable error message",

  "details": {

    "field": "Additional context"

  }

}

```

 

### Common Error Codes

 

| Code | HTTP Status | Description |

|------|-------------|-------------|

| `invalid_request` | 400 | Malformed request |

| `validation_error` | 400 | Invalid input data |

| `unauthorized` | 401 | Missing or invalid auth token |

| `forbidden` | 403 | Insufficient permissions |

| `not_found` | 404 | Resource not found |

| `conflict` | 409 | Resource already exists |

| `payload_too_large` | 413 | File too large |

| `rate_limit_exceeded` | 429 | Too many requests |

| `internal_server_error` | 500 | Server error |

| `service_unavailable` | 503 | Temporary outage |

 

---

 

## Pagination

 

List endpoints support cursor-based pagination.

 

**Request:**

```http

GET /swings?page=2&limit=20

```

 

**Response:**

```json

{

  "data": [...],

  "pagination": {

    "page": 2,

    "limit": 20,

    "total_items": 156,

    "total_pages": 8,

    "has_next": true,

    "has_prev": true,

    "next_page": 3,

    "prev_page": 1

  }

}

```

 

---

 

## Webhooks

 

Configure webhooks to receive real-time notifications.

 

### Events

 

- `swing.completed`: Swing analysis completed

- `swing.failed`: Swing analysis failed

- `user.upgraded`: User upgraded subscription

- `drill.completed`: User completed a drill

 

### Webhook Payload

 

```json

{

  "event": "swing.completed",

  "timestamp": "2026-01-07T14:31:00Z",

  "data": {

    "swing_id": 123,

    "user_id": 1,

    "overall_score": 7.5

  }

}

```

 

### Signature Verification

 

Verify webhook authenticity using HMAC-SHA256:

 

```python

import hmac

import hashlib

 

def verify_webhook(payload, signature, secret):

    expected = hmac.new(

        secret.encode(),

        payload.encode(),

        hashlib.sha256

    ).hexdigest()

    return hmac.compare_digest(signature, expected)

```

 

---

 

## SDK Examples

 

### Python

 

```python

from golfcoach import Client

 

client = Client(api_key="your_api_key")

 

# Upload swing

swing = client.swings.upload("path/to/video.mp4", club="driver")

print(f"Swing ID: {swing.id}")

 

# Get analysis

analysis = client.swings.get_analysis(swing.id)

print(f"Score: {analysis.overall_score}")

print(f"Issues: {[issue['issue'] for issue in analysis.issues]}")

```

 

### JavaScript/TypeScript

 

```typescript

import { GolfCoachClient } from '@golfcoach/sdk';

 

const client = new GolfCoachClient({ apiKey: 'your_api_key' });

 

// Upload swing

const swing = await client.swings.upload(videoFile, {

  club: 'driver',

  intendedShape: 'straight'

});

 

// Get analysis

const analysis = await client.swings.getAnalysis(swing.id);

console.log(`Score: ${analysis.overallScore}`);

```

 

---

 

## Changelog

 

### v1.0.0 (2026-01-07)

- Initial API release

- Swing upload and analysis

- User authentication

- Drill recommendations

 

---

 

For questions or support, contact: api-support@golfcoachpro.com
