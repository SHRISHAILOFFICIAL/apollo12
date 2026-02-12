# DCET Platform - Backend API Documentation

> **For Flutter App Development**  
> **Base URL:** `http://YOUR_SERVER_IP/api`  
> **Authentication:** JWT Bearer Token

---

## Server Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    UBUNTU VM / SERVER                           │
│                    (192.168.x.x or domain)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                      NGINX (Port 80)                    │   │
│   │                    Reverse Proxy                        │   │
│   └───────────────────────┬─────────────────────────────────┘   │
│                           │                                     │
│           ┌───────────────┴───────────────┐                     │
│           ▼                               ▼                     │
│   ┌───────────────────┐         ┌───────────────────┐           │
│   │  Django Backend   │         │  Next.js Frontend │           │
│   │  Gunicorn+Uvicorn │         │  (Port 3000)      │           │
│   │  (Port 8000)      │         │                   │           │
│   │                   │         │  (Web Only -      │           │
│   │  ◄── /api/*       │         │   Not for Flutter)│           │
│   │  ◄── /admin/*     │         │                   │           │
│   └─────────┬─────────┘         └───────────────────┘           │
│             │                                                   │
│   ┌─────────┴─────────┐         ┌───────────────────┐           │
│   │      MySQL        │         │      Redis        │           │
│   │   (Database)      │         │   (Exam Timers)   │           │
│   └───────────────────┘         └───────────────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

              ▲                               ▲
              │                               │
    ┌─────────┴─────────┐           ┌─────────┴─────────┐
    │   FLUTTER APP     │           │   WEB BROWSER     │
    │   (Android/iOS)   │           │                   │
    │                   │           │                   │
    │   Calls /api/*    │           │   Full website    │
    └───────────────────┘           └───────────────────┘
```

### Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Django 5.2 + DRF | REST API |
| **ASGI Server** | Gunicorn + Uvicorn | High-performance async server |
| **Database** | MySQL | Data persistence |
| **Cache/Timer** | Redis | Exam timer management |
| **Reverse Proxy** | Nginx | Load balancing, SSL |
| **OS** | Ubuntu Server | Hosting environment |

### Important Notes for Flutter

1. **Flutter app ONLY uses `/api/*` endpoints** - No frontend needed
2. **Backend is stateless** - All state is in JWT tokens and database
3. **Timers use Redis** - Server-side timer prevents cheating
4. **HTTPS recommended** for production deployments

---

## Table of Contents

1. [Authentication Flow](#1-authentication-flow)
2. [API Endpoints](#2-api-endpoints)
3. [Data Models](#3-data-models)
4. [App Flow Diagrams](#4-app-flow-diagrams)
5. [Error Handling](#5-error-handling)

---

## 1. Authentication Flow

### JWT Token System

The backend uses **JWT (JSON Web Tokens)** for authentication.

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. SIGNUP (New User)                                           │
│     ┌──────────────────────────────────────────────────────┐    │
│     │ POST /users/send-signup-otp/  →  { email }           │    │
│     │                    ↓                                 │    │
│     │ POST /users/verify-signup-otp/ → { email, otp }      │    │
│     │                    ↓                                 │    │
│     │ POST /auth/register/ → { username, email, password } │    │
│     │                    ↓                                 │    │
│     │ Returns: { access, refresh, user }                   │    │
│     └──────────────────────────────────────────────────────┘    │
│                                                                 │
│  2. LOGIN (Existing User)                                       │
│     ┌──────────────────────────────────────────────────────┐    │
│     │ POST /auth/login/ → { username/email, password }     │    │
│     │                    ↓                                 │    │
│     │ Returns: { access, refresh, user }                   │    │
│     └──────────────────────────────────────────────────────┘    │
│                                                                 │
│  3. TOKEN REFRESH                                               │
│     ┌──────────────────────────────────────────────────────┐    │
│     │ POST /token/refresh/ → { refresh }                   │    │
│     │                    ↓                                 │    │
│     │ Returns: { access }                                   │    │
│     └──────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Token Storage (Flutter)

```dart
// Store tokens securely using flutter_secure_storage
final storage = FlutterSecureStorage();

// After login
await storage.write(key: 'access_token', value: response.access);
await storage.write(key: 'refresh_token', value: response.refresh);

// For API calls - add header
headers: {
  'Authorization': 'Bearer $accessToken',
  'Content-Type': 'application/json',
}
```

---

## 2. API Endpoints

### 2.1 Authentication & User Management

#### Send Signup OTP
```http
POST /api/users/send-signup-otp/
Content-Type: application/json

Request:
{
  "email": "user@example.com"
}

Response (200):
{
  "message": "OTP sent successfully",
  "email": "user@example.com"
}

Response (400):
{
  "error": "Email already registered"
}
```

#### Verify Signup OTP
```http
POST /api/users/verify-signup-otp/
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "otp": "123456"
}

Response (200):
{
  "message": "OTP verified successfully",
  "email_verified": true
}

Response (400):
{
  "error": "Invalid or expired OTP"
}
```

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

Request:
{
  "username": "john_doe",
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe",
  "mobile": "9876543210"
}

Response (201):
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "user@example.com",
    "current_tier": "FREE"
  }
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

Request:
{
  "username": "john_doe",  // Can be username OR email
  "password": "securepassword123"
}

Response (200):
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "user@example.com",
    "current_tier": "FREE"
  }
}
```

#### Refresh Token
```http
POST /api/token/refresh/
Content-Type: application/json

Request:
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."
}

Response (200):
{
  "access": "new_access_token..."
}
```

#### Get User Profile
```http
GET /api/auth/profile/
Authorization: Bearer <access_token>

Response (200):
{
  "id": 1,
  "username": "john_doe",
  "email": "user@example.com",
  "phone": "9876543210",
  "current_tier": "FREE",
  "email_verified": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### 2.2 Password Reset Flow

```http
# Step 1: Send OTP
POST /api/users/send-password-reset-otp/
{
  "email": "user@example.com"
}

# Step 2: Verify OTP
POST /api/users/verify-password-reset-otp/
{
  "email": "user@example.com",
  "otp": "123456"
}

# Step 3: Reset Password
POST /api/users/reset-password/
{
  "email": "user@example.com",
  "otp": "123456",
  "new_password": "newSecurePassword123"
}
```

---

### 2.3 Exams & Questions

#### List All Exams
```http
GET /api/exams/
Authorization: Bearer <access_token>

Response (200):
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "name": "DCET",
      "year": 2023,
      "title": "DCET 2023",
      "description": "DCET 2023 Mock Test",
      "total_marks": 180,
      "duration_minutes": 180,
      "total_questions": 180,
      "access_tier": "FREE",
      "is_premium": false,
      "is_published": true,
      "is_available": true
    }
  ]
}
```

#### Get Exam Details
```http
GET /api/exams/{exam_id}/
Authorization: Bearer <access_token>

Response (200):
{
  "id": 1,
  "name": "DCET",
  "year": 2023,
  "total_marks": 180,
  "duration_minutes": 180,
  "sections": [
    {
      "id": 1,
      "name": "Engineering Mathematics",
      "order": 1,
      "max_marks": 20,
      "question_count": 20
    },
    {
      "id": 2,
      "name": "Statistics",
      "order": 2,
      "max_marks": 20,
      "question_count": 20
    }
  ]
}

Response (403 - Premium Required):
{
  "success": false,
  "error": "PRO subscription required",
  "requires_pro": true,
  "exam_id": 5
}
```

#### Get Exam Questions
```http
GET /api/exams/{exam_id}/questions/
Authorization: Bearer <access_token>

Response (200):
[
  {
    "id": 1,
    "section_id": 1,
    "section_name": "Engineering Mathematics",
    "question_number": 1,
    "question_text": "What is the derivative of sin(x)?",
    "option_a": "cos(x)",
    "option_b": "-cos(x)",
    "option_c": "sin(x)",
    "option_d": "-sin(x)",
    "marks": 1,
    "diagram_url": null
  }
]
```

#### Get User's Previous Attempts
```http
GET /api/exams/{exam_id}/attempts/
Authorization: Bearer <access_token>

Response (200):
{
  "attempts": [
    {
      "id": 15,
      "attempt_number": 2,
      "exam_name": "DCET 2023",
      "started_at": "2024-01-20T14:30:00Z",
      "score": 145,
      "total_marks": 180,
      "percentage": 80.5,
      "status": "submitted"
    }
  ]
}
```

---

### 2.4 Exam Session (With Redis Timer)

#### Start Exam
```http
POST /api/exam/timer/start/{exam_id}/
Authorization: Bearer <access_token>

Response (200):
{
  "attempt_id": 25,
  "exam_id": 1,
  "exam_name": "DCET 2023",
  "duration_minutes": 180,
  "remaining_seconds": 10800,
  "questions": [
    {
      "id": 1,
      "question_number": 1,
      "question_text": "...",
      "option_a": "...",
      "option_b": "...",
      "option_c": "...",
      "option_d": "...",
      "marks": 1
    }
  ],
  "server_time": "2024-01-20T14:30:00Z"
}
```

#### Get Remaining Time
```http
GET /api/exam/timer/remaining/{attempt_id}/
Authorization: Bearer <access_token>

Response (200):
{
  "remaining_seconds": 9500,
  "status": "in_progress",
  "server_time": "2024-01-20T14:45:00Z"
}
```

#### Submit Answer
```http
POST /api/exam/timer/submit-answer/
Authorization: Bearer <access_token>

Request:
{
  "attempt_id": 25,
  "question_id": 1,
  "selected_option": "A"  // A, B, C, D or null to clear
}

Response (200):
{
  "success": true,
  "message": "Answer saved"
}
```

#### Submit Exam
```http
POST /api/exam/timer/submit/{attempt_id}/
Authorization: Bearer <access_token>

Response (200):
{
  "success": true,
  "attempt_id": 25,
  "score": 145,
  "total_marks": 180,
  "percentage": 80.5,
  "correct_answers": 145,
  "wrong_answers": 25,
  "unattempted": 10
}
```

---

### 2.5 Results & Dashboard

#### Get Attempt Results (Detailed)
```http
GET /api/results/{attempt_id}/
Authorization: Bearer <access_token>

Response (200):
{
  "attempt_id": 25,
  "exam_name": "DCET 2023",
  "score": 145,
  "total_marks": 180,
  "percentage": 80.5,
  "time_taken_seconds": 9000,
  "status": "submitted",
  "sections": [
    {
      "name": "Engineering Mathematics",
      "score": 18,
      "max_marks": 20,
      "correct": 18,
      "wrong": 2,
      "unattempted": 0
    }
  ],
  "answers": [
    {
      "question_id": 1,
      "question_number": 1,
      "selected_option": "A",
      "correct_option": "A",
      "is_correct": true
    }
  ]
}
```

#### User Dashboard
```http
GET /api/dashboard/
Authorization: Bearer <access_token>

Response (200):
{
  "user": {
    "username": "john_doe",
    "current_tier": "FREE"
  },
  "stats": {
    "total_attempts": 15,
    "average_score": 75.5,
    "best_score": 90.2,
    "exams_completed": 8
  },
  "recent_attempts": [...]
}
```

---

### 2.6 Payments (Razorpay)

#### List Plans
```http
GET /api/payments/plans/

Response (200):
[
  {
    "id": 1,
    "key": "pro_yearly",
    "name": "PRO Plan",
    "price_in_paisa": 99900,  // ₹999
    "duration_days": 365,
    "features": [
      "All Mock Tests",
      "Video Solutions",
      "Detailed Analytics"
    ]
  }
]
```

#### Create Payment Order
```http
POST /api/payments/create-order/
Authorization: Bearer <access_token>

Request:
{
  "plan_id": 1
}

Response (200):
{
  "order_id": "order_N1234567890",
  "amount": 99900,
  "currency": "INR",
  "key_id": "rzp_test_xxx",  // Razorpay key for frontend
  "plan_name": "PRO Plan"
}
```

#### Verify Payment
```http
POST /api/payments/verify-payment/
Authorization: Bearer <access_token>

Request:
{
  "razorpay_order_id": "order_N1234567890",
  "razorpay_payment_id": "pay_N1234567890",
  "razorpay_signature": "signature_hash",
  "plan_id": 1
}

Response (200):
{
  "success": true,
  "message": "Payment verified and subscription activated",
  "subscription": {
    "plan": "PRO Plan",
    "start_date": "2024-01-20",
    "end_date": "2025-01-20",
    "days_remaining": 365
  }
}
```

#### Subscription Status
```http
GET /api/payments/subscription-status/
Authorization: Bearer <access_token>

Response (200):
{
  "has_subscription": true,
  "current_tier": "PRO",
  "subscription": {
    "plan_name": "PRO Plan",
    "start_date": "2024-01-20",
    "end_date": "2025-01-20",
    "days_remaining": 300,
    "status": "active"
  }
}
```

---

### 2.7 Content (Notes, PYQs, Videos)

#### List Notes
```http
GET /api/notes/
Authorization: Bearer <access_token>

Response (200):
[
  {
    "id": 1,
    "subject": "Engineering Mathematics",
    "topic": "Matrices",
    "access_tier": "FREE",
    "is_premium": false
  }
]
```

#### View Note PDF
```http
GET /api/notes/{note_id}/view/
Authorization: Bearer <access_token>

Response: PDF file stream
```

#### List PYQs (Previous Year Questions)
```http
GET /api/pyqs/
Authorization: Bearer <access_token>

Response (200):
[
  {
    "id": 1,
    "exam_name": "DCET",
    "year": 2023,
    "access_tier": "FREE",
    "is_premium": false
  }
]
```

#### List Video Solutions
```http
GET /api/videos/
Authorization: Bearer <access_token>

Response (200):
[
  {
    "id": 1,
    "topic": "Calculus",
    "title": "Integration Techniques",
    "video_url": "https://youtube.com/watch?v=xxx",
    "duration_minutes": 15
  }
]
```

#### List Announcements
```http
GET /api/announcements/

Response (200):
[
  {
    "id": 1,
    "title": "New Mock Test Available",
    "message": "DCET 2024 mock test is now live!",
    "created_at": "2024-01-20T10:00:00Z"
  }
]
```

---

### 2.8 Notifications

#### Get Notifications
```http
GET /api/users/notifications/
Authorization: Bearer <access_token>

Response (200):
[
  {
    "id": 1,
    "title": "Payment Successful",
    "message": "Your PRO subscription is now active",
    "is_read": false,
    "created_at": "2024-01-20T10:00:00Z"
  }
]
```

#### Mark Notification as Read
```http
POST /api/users/notifications/{id}/mark_as_read/
Authorization: Bearer <access_token>
```

#### Get Unread Count
```http
GET /api/users/notifications/unread/
Authorization: Bearer <access_token>

Response (200):
{
  "unread_count": 5
}
```

---

### 2.9 Report Question Issue

```http
POST /api/exam/report-issue/
Authorization: Bearer <access_token>

Request:
{
  "question_id": 15,
  "attempt_id": 25,
  "issue_type": "wrong_answer",  // Options: wrong_answer, latex_format, unclear_question, typo, other
  "description": "The correct answer should be B, not A"
}

Response (200):
{
  "success": true,
  "message": "Issue reported successfully"
}
```

---

### 2.10 Contact Form

```http
POST /api/users/submit-query/

Request:
{
  "username": "John Doe",
  "email": "john@example.com",
  "mobile": "9876543210",
  "query": "I have a question about the exam schedule"
}

Response (200):
{
  "success": true,
  "message": "Query submitted successfully"
}
```

---

## 3. Data Models

### User

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| username | string | Unique username |
| email | string | Unique email |
| phone | string | Mobile number |
| email_verified | boolean | Email verification status |
| current_tier | string | "FREE" or "PRO" |
| created_at | datetime | Account creation date |

### Exam

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| name | string | Exam name (e.g., "DCET") |
| year | int | Exam year |
| title | string | Display title |
| total_marks | int | Maximum marks |
| duration_minutes | int | Time limit |
| access_tier | string | "FREE" or "PRO" |
| is_published | boolean | Visibility status |
| instructions | text | Exam instructions |

### Section

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| exam_id | int | Parent exam |
| name | string | Section name |
| order | int | Display order |
| max_marks | int | Section marks |

### Question

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| section_id | int | Parent section |
| question_number | int | Question number |
| question_text | text | Question (supports LaTeX) |
| option_a | text | Option A |
| option_b | text | Option B |
| option_c | text | Option C |
| option_d | text | Option D |
| correct_option | string | A, B, C, or D |
| marks | int | Question marks |
| diagram_url | string | Optional image URL |

### Attempt

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| user_id | int | User who attempted |
| exam_id | int | Exam attempted |
| attempt_number | int | Nth attempt |
| started_at | datetime | Start time |
| finished_at | datetime | End time |
| score | int | Total score |
| status | string | "in_progress", "submitted", "timeout" |

### Subscription

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| user_id | int | Subscriber |
| plan_id | int | Plan purchased |
| status | string | "active", "expired", "cancelled" |
| start_date | datetime | Subscription start |
| end_date | datetime | Subscription end |
| days_remaining | int | Computed field |

---

## 4. App Flow Diagrams

### Complete User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER JOURNEY                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │   SPLASH    │────▶│   ONBOARD   │────▶│   AUTH      │       │
│  │   SCREEN    │     │   SCREENS   │     │   FLOW      │       │
│  └─────────────┘     └─────────────┘     └──────┬──────┘       │
│                                                  │               │
│                                                  ▼               │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │   PROFILE   │◀───▶│    HOME     │◀───▶│   EXAMS     │       │
│  │   SCREEN    │     │  DASHBOARD  │     │    LIST     │       │
│  └─────────────┘     └──────┬──────┘     └──────┬──────┘       │
│                              │                   │               │
│                              ▼                   ▼               │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │   PAYMENT   │     │   NOTES/    │     │   EXAM      │       │
│  │   SCREEN    │     │   VIDEOS    │     │  DETAILS    │       │
│  └─────────────┘     └─────────────┘     └──────┬──────┘       │
│                                                  │               │
│                                                  ▼               │
│                                           ┌─────────────┐       │
│                                           │   EXAM      │       │
│                                           │  SESSION    │       │
│                                           └──────┬──────┘       │
│                                                  │               │
│                                                  ▼               │
│                                           ┌─────────────┐       │
│                                           │  RESULTS    │       │
│                                           │   SCREEN    │       │
│                                           └─────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Exam Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        EXAM FLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. SELECT EXAM                                                 │
│     GET /api/exams/ → List all available exams                  │
│                                                                 │
│  2. VIEW EXAM DETAILS                                           │
│     GET /api/exams/{id}/ → Get exam info + sections             │
│                                                                 │
│  3. CHECK ACCESS                                                │
│     - If FREE exam: Allow                                       │
│     - If PRO exam: Check subscription status                    │
│       - Has PRO: Allow                                          │
│       - No PRO: Show upgrade prompt                             │
│                                                                 │
│  4. START EXAM                                                  │
│     POST /api/exam/timer/start/{exam_id}/                       │
│     → Creates attempt, starts timer, returns questions          │
│                                                                 │
│  5. DURING EXAM                                                 │
│     - Display question one at a time or grid                    │
│     - POST /api/exam/timer/submit-answer/ → Save each answer    │
│     - GET /api/exam/timer/remaining/{attempt_id}/ → Sync timer  │
│                                                                 │
│  6. SUBMIT EXAM                                                 │
│     POST /api/exam/timer/submit/{attempt_id}/                   │
│     → Calculates score, returns summary                         │
│                                                                 │
│  7. VIEW RESULTS                                                │
│     GET /api/results/{attempt_id}/                              │
│     → Detailed breakdown with correct answers                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Payment Flow (Razorpay)

```
┌─────────────────────────────────────────────────────────────────┐
│                     RAZORPAY PAYMENT FLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FLUTTER APP                    BACKEND                         │
│  ───────────                    ───────                         │
│                                                                 │
│  1. List Plans                                                  │
│     GET /api/payments/plans/                                    │
│                                                                 │
│  2. User selects plan                                           │
│     POST /api/payments/create-order/                            │
│     { "plan_id": 1 }                                            │
│                        ───────▶                                 │
│                                   Creates Razorpay order        │
│                        ◀───────                                 │
│     { order_id, amount, key_id }                                │
│                                                                 │
│  3. Open Razorpay checkout                                      │
│     razorpay_flutter package                                    │
│     - User enters card/UPI                                      │
│     - Razorpay processes payment                                │
│                                                                 │
│  4. On success callback                                         │
│     POST /api/payments/verify-payment/                          │
│     {                                                           │
│       razorpay_order_id,                                        │
│       razorpay_payment_id,                                      │
│       razorpay_signature,                                       │
│       plan_id                                                   │
│     }                                                           │
│                        ───────▶                                 │
│                                   Verifies signature            │
│                                   Activates subscription        │
│                        ◀───────                                 │
│     { success: true, subscription: {...} }                      │
│                                                                 │
│  5. Update user tier to PRO                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Error Handling

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 201 | Created | New resource created |
| 400 | Bad Request | Show validation errors |
| 401 | Unauthorized | Refresh token or re-login |
| 403 | Forbidden | Show upgrade prompt if PRO required |
| 404 | Not Found | Show not found message |
| 500 | Server Error | Show generic error, retry |

### Token Refresh Logic

```dart
// Pseudo-code for Flutter
class ApiClient {
  Future<Response> request(String endpoint, {Map? body}) async {
    var response = await http.post(endpoint, body: body, headers: authHeaders);
    
    if (response.statusCode == 401) {
      // Token expired, try refresh
      bool refreshed = await refreshToken();
      if (refreshed) {
        // Retry original request
        return await http.post(endpoint, body: body, headers: authHeaders);
      } else {
        // Refresh failed, logout user
        await logout();
        throw AuthException('Session expired');
      }
    }
    
    return response;
  }
}
```

### Error Response Format

```json
{
  "error": "Error message here",
  "code": "ERROR_CODE",
  "details": {
    "field_name": ["Specific field error"]
  }
}
```

---

## 6. Flutter Package Recommendations

| Purpose | Package |
|---------|---------|
| HTTP Client | `dio` or `http` |
| State Management | `riverpod` or `bloc` |
| Local Storage | `flutter_secure_storage` |
| Payments | `razorpay_flutter` |
| LaTeX Rendering | `flutter_math_fork` |
| PDF Viewer | `pdfx` or `syncfusion_flutter_pdfviewer` |

---

## 7. Environment Setup

### Development
```
BASE_URL = http://192.168.1.17/api
```

### Production
```
BASE_URL = https://yourdomain.com/api
```

---

**Document Version:** 1.0  
**Last Updated:** February 2026  
**Backend Version:** Django 5.2 + DRF + JWT
