# Redis Exam Timer System - Complete Documentation

## 🎯 Overview

This is a **production-ready Redis timer implementation** for a Django REST Framework exam platform. Redis handles **ONLY countdown timers** with automatic expiration (TTL), while MySQL stores all permanent exam data.

---

## 📋 Table of Contents

1. [Architecture](#architecture)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [API Endpoints](#api-endpoints)
5. [Redis Key Structure](#redis-key-structure)
6. [Error Handling](#error-handling)
7. [Testing](#testing)
8. [Frontend Integration](#frontend-integration)

---

## 🏗️ Architecture

### Data Storage Strategy

| Data Type         | Storage     | Reason                                 |
| ----------------- | ----------- | -------------------------------------- |
| **Timers**        | Redis (TTL) | Automatic expiration, high performance |
| **Exam Attempts** | MySQL       | Permanent records, relationships       |
| **Questions**     | MySQL       | Permanent data                         |
| **Answers**       | MySQL       | Permanent records                      |
| **Scores**        | MySQL       | Permanent results                      |

### Flow Diagram

```
START EXAM
    ↓
[MySQL] Create Attempt (status=ongoing)
    ↓
[Redis] Create Timer (TTL = duration * 60)
    ↓
Return attempt_id + remaining_seconds

DURING EXAM
    ↓
[Frontend] Check remaining time every 10s
    ↓
[Redis] TTL still exists? → return seconds
         TTL expired (-2)? → mark timeout in MySQL

SUBMIT EXAM
    ↓
[Redis] Timer exists? → Delete timer
        Timer missing? → Already timed out
    ↓
[MySQL] Calculate score, mark completed
    ↓
Return results
```

---

## 📦 Installation

### 1. Install Redis Server

**Windows:**

```powershell
# Download from: https://github.com/microsoftarchive/redis/releases
# Or use WSL:
wsl --install
wsl
sudo apt-get update
sudo apt-get install redis-server
redis-server
```

**Linux:**

```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**macOS:**

```bash
brew install redis
brew services start redis
```

### 2. Install Python Packages

```bash
cd backend
pip install -r requirements.txt
```

**requirements.txt includes:**

```
django
djangorestframework
djangorestframework-simplejwt
mysqlclient
django-cors-headers
pandas
django-redis
redis
```

### 3. Verify Redis is Running

```bash
redis-cli ping
# Should return: PONG
```

---

## ⚙️ Configuration

### settings.py

```python
# Redis Cache Configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # Database 1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
```

**Connection String Format:**

```
redis://[username:password@]host:port/database
```

**Examples:**

```python
# Local development (no auth)
"LOCATION": "redis://127.0.0.1:6379/1"

# Production with password
"LOCATION": "redis://:mypassword@redis.example.com:6379/1"

# Production with username and password
"LOCATION": "redis://user:pass@redis.example.com:6379/1"
```

### Database Migration

Add `timeout` status to Attempt model:

```python
# core/models.py
class Attempt(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('timeout', 'Timeout'),  # NEW
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
```

Run migration:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🔌 API Endpoints

### 1. Start Exam

**Endpoint:** `POST /api/exam/timer/start/<exam_id>/`

**Authentication:** Required (JWT)

**Request:**

```http
POST /api/exam/timer/start/45/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (Success):**

```json
{
  "attempt_id": 123,
  "exam_id": 45,
  "exam_title": "Python Fundamentals",
  "duration_minutes": 60,
  "remaining_seconds": 3600,
  "total_questions": 50,
  "total_marks": 100
}
```

**Response (Resume Existing):**

```json
{
  "attempt_id": 123,
  "exam_id": 45,
  "exam_title": "Python Fundamentals",
  "duration_minutes": 60,
  "remaining_seconds": 2847,
  "total_questions": 50,
  "total_marks": 100,
  "message": "Resuming existing exam attempt"
}
```

**Error Responses:**

```json
// 400 - Exam not published
{
    "error": "This exam is not published yet."
}

// 400 - Previous attempt timed out
{
    "error": "Your previous attempt has timed out. Please start a new attempt."
}

// 404 - Exam not found
{
    "detail": "Not found."
}

// 500 - Redis connection failed
{
    "error": "Failed to start exam timer. Please try again."
}
```

---

### 2. Get Remaining Time

**Endpoint:** `GET /api/exam/timer/remaining/<attempt_id>/`

**Authentication:** Required (JWT)

**Request:**

```http
GET /api/exam/timer/remaining/123/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (Running):**

```json
{
  "status": "running",
  "remaining_seconds": 2847
}
```

**Response (Timeout):**

```json
{
  "status": "timeout",
  "remaining_seconds": 0,
  "message": "Exam time has expired"
}
```

**Response (Completed):**

```json
{
  "status": "completed",
  "remaining_seconds": 0,
  "message": "Exam already submitted"
}
```

**Error Responses:**

```json
// 403 - Not your attempt
{
    "error": "This exam attempt does not belong to you."
}

// 404 - Attempt not found
{
    "detail": "Not found."
}
```

---

### 3. Submit Answer

**Endpoint:** `POST /api/exam/timer/submit-answer/`

**Authentication:** Required (JWT)

**Request:**

```json
{
  "attempt_id": 123,
  "question_id": 456,
  "selected_option": "B"
}
```

**Response (Success):**

```json
{
  "status": "saved",
  "question_id": 456,
  "selected_option": "B",
  "action": "saved" // or "updated"
}
```

**Error Responses:**

```json
// 400 - Exam already completed
{
    "error": "Exam already submitted. Cannot modify answers."
}

// 400 - Invalid question for this exam
{
    "error": "This question does not belong to this exam."
}

// 403 - Not your attempt
{
    "error": "This exam attempt does not belong to you."
}

// 410 - Time expired
{
    "error": "Exam time has expired. Cannot submit answers."
}
```

---

### 4. Submit Exam

**Endpoint:** `POST /api/exam/timer/submit/<attempt_id>/`

**Authentication:** Required (JWT)

**Request:**

```http
POST /api/exam/timer/submit/123/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (Success):**

```json
{
  "status": "submitted",
  "score": 75,
  "total_marks": 100,
  "percentage": 75.0,
  "correct_answers": 15,
  "total_questions": 20,
  "time_taken_minutes": 45
}
```

**Response (Timeout Submission):**

```json
{
  "status": "timeout",
  "score": 60,
  "total_marks": 100,
  "percentage": 60.0,
  "correct_answers": 12,
  "total_questions": 20,
  "time_taken_minutes": 61,
  "message": "Exam submitted after time expired"
}
```

**Response (Already Completed):**

```json
{
  "status": "already_completed",
  "score": 75,
  "total_marks": 100,
  "percentage": 75.0,
  "message": "Exam was already submitted"
}
```

**Error Responses:**

```json
// 403 - Not your attempt
{
    "error": "This exam attempt does not belong to you."
}

// 404 - Attempt not found
{
    "detail": "Not found."
}
```

---

### 5. Get Exam Questions

**Endpoint:** `GET /api/exam/timer/questions/<attempt_id>/`

**Authentication:** Required (JWT)

**Request:**

```http
GET /api/exam/timer/questions/123/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response:**

```json
{
  "attempt_id": 123,
  "exam_title": "Python Fundamentals",
  "questions": [
    {
      "id": 1,
      "text": "What is Python?",
      "option_a": "A snake",
      "option_b": "A programming language",
      "option_c": "A framework",
      "option_d": "A database",
      "marks": 2
    },
    {
      "id": 2,
      "text": "What is PEP 8?",
      "option_a": "A Python version",
      "option_b": "Style guide",
      "option_c": "A library",
      "option_d": "An IDE",
      "marks": 1
    }
  ],
  "saved_answers": {
    "1": "B",
    "2": "B"
  }
}
```

**Note:** Correct answers are **NOT** included in the response for security.

---

## 🔑 Redis Key Structure

### Key Format

```
exam:timer:{attempt_id}
```

### Examples

```
exam:timer:123
exam:timer:456
exam:timer:789
```

### Key Operations

**Create Timer:**

```python
redis.setex("exam:timer:123", 3600, 3600)
# Key: exam:timer:123
# Value: 3600 (initial seconds)
# TTL: 3600 seconds (auto-expires)
```

**Check TTL:**

```python
ttl = redis.ttl("exam:timer:123")
# Returns:
#   >= 0  : Remaining seconds
#   -2    : Key doesn't exist (expired)
#   -1    : Key exists but no TTL (error)
```

**Delete Timer:**

```python
redis.delete("exam:timer:123")
```

### Redis CLI Commands

```bash
# View all exam timers
redis-cli KEYS "exam:timer:*"

# Check specific timer
redis-cli TTL "exam:timer:123"

# Get timer value
redis-cli GET "exam:timer:123"

# Delete timer
redis-cli DEL "exam:timer:123"

# Delete all exam timers (DANGER!)
redis-cli --scan --pattern "exam:timer:*" | xargs redis-cli DEL
```

---

## 🛡️ Error Handling

### Connection Errors

**Problem:** Redis server not running

**Symptoms:**

```python
redis.exceptions.ConnectionError: Error 111 connecting to 127.0.0.1:6379. Connection refused.
```

**Solution:**

```bash
# Start Redis server
redis-server

# Or as a service
sudo systemctl start redis-server
```

---

### Authentication Errors

**Problem:** Redis requires password

**Symptoms:**

```python
redis.exceptions.ResponseError: NOAUTH Authentication required.
```

**Solution:**

```python
# Update settings.py
CACHES = {
    "default": {
        "LOCATION": "redis://:yourpassword@127.0.0.1:6379/1",
    }
}
```

---

### TTL = -1 Error

**Problem:** Key exists but has no expiration

**Symptoms:**

```python
ttl = redis.ttl("exam:timer:123")  # Returns -1
```

**Cause:** Data corruption or manual key creation without TTL

**Solution:**

```python
# Delete corrupted key
redis.delete("exam:timer:123")

# Or set expiration
redis.expire("exam:timer:123", 3600)
```

---

## 🧪 Testing

### Manual Testing with curl

**1. Start Exam:**

```bash
curl -X POST http://localhost:8000/api/exam/timer/start/1/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

**2. Check Remaining Time:**

```bash
curl -X GET http://localhost:8000/api/exam/timer/remaining/123/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**3. Submit Answer:**

```bash
curl -X POST http://localhost:8000/api/exam/timer/submit-answer/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "attempt_id": 123,
    "question_id": 1,
    "selected_option": "B"
  }'
```

**4. Submit Exam:**

```bash
curl -X POST http://localhost:8000/api/exam/timer/submit/123/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

---

### Python Testing Script

Create `test_redis_timer.py`:

```python
import requests
import time

BASE_URL = "http://localhost:8000/api"
TOKEN = "YOUR_JWT_TOKEN_HERE"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 1. Start exam
print("Starting exam...")
response = requests.post(f"{BASE_URL}/exam/timer/start/1/", headers=headers)
print(response.json())
attempt_id = response.json()["attempt_id"]

# 2. Check remaining time
print("\nChecking remaining time...")
response = requests.get(f"{BASE_URL}/exam/timer/remaining/{attempt_id}/", headers=headers)
print(response.json())

# 3. Submit answer
print("\nSubmitting answer...")
response = requests.post(
    f"{BASE_URL}/exam/timer/submit-answer/",
    headers=headers,
    json={
        "attempt_id": attempt_id,
        "question_id": 1,
        "selected_option": "B"
    }
)
print(response.json())

# 4. Wait a bit
print("\nWaiting 5 seconds...")
time.sleep(5)

# 5. Check remaining time again
print("\nChecking remaining time again...")
response = requests.get(f"{BASE_URL}/exam/timer/remaining/{attempt_id}/", headers=headers)
print(response.json())

# 6. Submit exam
print("\nSubmitting exam...")
response = requests.post(f"{BASE_URL}/exam/timer/submit/{attempt_id}/", headers=headers)
print(response.json())
```

Run:

```bash
python test_redis_timer.py
```

---

### Redis Monitoring

**Monitor all Redis commands in real-time:**

```bash
redis-cli MONITOR
```

**Check memory usage:**

```bash
redis-cli INFO memory
```

**Count exam timers:**

```bash
redis-cli --scan --pattern "exam:timer:*" | wc -l
```

---

## 🌐 Frontend Integration

### React/Next.js Example

```typescript
// lib/services/exam-timer.service.ts

import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export interface StartExamResponse {
  attempt_id: number;
  exam_id: number;
  exam_title: string;
  duration_minutes: number;
  remaining_seconds: number;
  total_questions: number;
  total_marks: number;
}

export interface RemainingTimeResponse {
  status: "running" | "timeout" | "completed";
  remaining_seconds: number;
  message?: string;
}

export interface SubmitExamResponse {
  status: "submitted" | "timeout" | "already_completed";
  score: number;
  total_marks: number;
  percentage: number;
  correct_answers: number;
  total_questions: number;
  time_taken_minutes?: number;
  message?: string;
}

class ExamTimerService {
  private getHeaders() {
    const token = localStorage.getItem("access_token");
    return {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    };
  }

  async startExam(examId: number): Promise<StartExamResponse> {
    const response = await axios.post(
      `${API_BASE}/exam/timer/start/${examId}/`,
      {},
      { headers: this.getHeaders() }
    );
    return response.data;
  }

  async getRemainingTime(attemptId: number): Promise<RemainingTimeResponse> {
    const response = await axios.get(
      `${API_BASE}/exam/timer/remaining/${attemptId}/`,
      { headers: this.getHeaders() }
    );
    return response.data;
  }

  async submitAnswer(
    attemptId: number,
    questionId: number,
    selectedOption: string
  ) {
    const response = await axios.post(
      `${API_BASE}/exam/timer/submit-answer/`,
      {
        attempt_id: attemptId,
        question_id: questionId,
        selected_option: selectedOption,
      },
      { headers: this.getHeaders() }
    );
    return response.data;
  }

  async submitExam(attemptId: number): Promise<SubmitExamResponse> {
    const response = await axios.post(
      `${API_BASE}/exam/timer/submit/${attemptId}/`,
      {},
      { headers: this.getHeaders() }
    );
    return response.data;
  }
}

export const examTimerService = new ExamTimerService();
```

### React Component with Timer

```typescript
"use client";

import { useState, useEffect, useRef } from "react";
import { examTimerService } from "@/lib/services/exam-timer.service";

export default function ExamPage({ params }: { params: { id: string } }) {
  const [attemptId, setAttemptId] = useState<number | null>(null);
  const [remainingSeconds, setRemainingSeconds] = useState<number>(0);
  const [status, setStatus] = useState<
    "loading" | "running" | "timeout" | "completed"
  >("loading");

  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // Start exam on mount
  useEffect(() => {
    const startExam = async () => {
      try {
        const data = await examTimerService.startExam(parseInt(params.id));
        setAttemptId(data.attempt_id);
        setRemainingSeconds(data.remaining_seconds);
        setStatus("running");
      } catch (error) {
        console.error("Failed to start exam:", error);
      }
    };

    startExam();
  }, [params.id]);

  // Poll remaining time every 10 seconds
  useEffect(() => {
    if (!attemptId || status !== "running") return;

    const checkRemainingTime = async () => {
      try {
        const data = await examTimerService.getRemainingTime(attemptId);

        if (data.status === "timeout") {
          setStatus("timeout");
          setRemainingSeconds(0);
          alert("Exam time has expired!");
        } else if (data.status === "completed") {
          setStatus("completed");
        } else {
          setRemainingSeconds(data.remaining_seconds);
        }
      } catch (error) {
        console.error("Failed to get remaining time:", error);
      }
    };

    // Check every 10 seconds
    timerRef.current = setInterval(checkRemainingTime, 10000);

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [attemptId, status]);

  // Local countdown (UI only, server is source of truth)
  useEffect(() => {
    if (remainingSeconds <= 0 || status !== "running") return;

    const countdown = setInterval(() => {
      setRemainingSeconds((prev) => Math.max(0, prev - 1));
    }, 1000);

    return () => clearInterval(countdown);
  }, [remainingSeconds, status]);

  const formatTime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, "0")}:${minutes
      .toString()
      .padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const handleSubmitExam = async () => {
    if (!attemptId) return;

    try {
      const result = await examTimerService.submitExam(attemptId);
      setStatus("completed");
      alert(
        `Exam submitted! Score: ${result.score}/${result.total_marks} (${result.percentage}%)`
      );
    } catch (error) {
      console.error("Failed to submit exam:", error);
    }
  };

  return (
    <div className="p-8">
      {/* Timer Display */}
      <div className="fixed top-4 right-4 bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg">
        <div className="text-2xl font-bold">{formatTime(remainingSeconds)}</div>
        <div className="text-sm">Time Remaining</div>
      </div>

      {/* Exam Content */}
      {status === "timeout" && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          Exam time has expired!
        </div>
      )}

      {status === "running" && (
        <div>
          {/* Render questions here */}
          <button
            onClick={handleSubmitExam}
            className="mt-4 bg-green-600 text-white px-6 py-2 rounded"
          >
            Submit Exam
          </button>
        </div>
      )}
    </div>
  );
}
```

---

## 🚀 Production Deployment

### Environment Variables

Create `.env` file:

```env
# Redis Configuration
REDIS_HOST=redis.example.com
REDIS_PORT=6379
REDIS_PASSWORD=your_secure_password
REDIS_DB=1

# Django Settings
DEBUG=False
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### settings.py for Production

```python
import os
from pathlib import Path

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
REDIS_DB = os.getenv('REDIS_DB', '1')

# Build Redis URL
if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 50,
                "retry_on_timeout": True,
            },
        },
    }
}
```

### Redis Security

**Enable authentication:**

Edit `/etc/redis/redis.conf`:

```conf
requirepass your_secure_password_here
```

**Restrict network access:**

```conf
bind 127.0.0.1 ::1
```

**Restart Redis:**

```bash
sudo systemctl restart redis-server
```

---

## 📊 Performance Considerations

### Redis Memory Usage

Each timer uses approximately **100 bytes**:

- Key: ~25 bytes (`exam:timer:123`)
- Value: ~10 bytes (integer)
- TTL metadata: ~65 bytes

**1000 concurrent exams = ~100 KB**

### Scaling

**Single Redis instance can handle:**

- 10,000+ concurrent timers
- 100,000+ operations/second
- Sub-millisecond latency

**For larger scale:**

- Use Redis Cluster
- Implement Redis Sentinel for failover
- Consider Redis Enterprise

---

## 🐛 Troubleshooting

### Issue: Timer not expiring

**Check:**

```bash
redis-cli TTL "exam:timer:123"
# Should return seconds remaining or -2 if expired
```

**Solution:** Ensure `setex` is used (not `set` + `expire`)

---

### Issue: Multiple timers for same attempt

**Check:**

```bash
redis-cli KEYS "exam:timer:*"
```

**Solution:** Ensure unique attempt IDs, implement transaction locking

---

### Issue: Redis connection timeout

**Check Redis logs:**

```bash
tail -f /var/log/redis/redis-server.log
```

**Increase timeout in settings.py:**

```python
"SOCKET_CONNECT_TIMEOUT": 10,  # Increase from 5
"SOCKET_TIMEOUT": 10,
```

---

## 📝 Summary

✅ **Redis stores ONLY timers** with automatic TTL expiration  
✅ **MySQL stores all permanent data** (attempts, questions, answers)  
✅ **Production-ready error handling** for all edge cases  
✅ **Secure JWT authentication** on all endpoints  
✅ **Comprehensive logging** for debugging  
✅ **Frontend-friendly API** with clear responses

---

## 📞 Support

For issues or questions:

1. Check Redis connection: `redis-cli ping`
2. Check Django logs: `python manage.py runserver`
3. Review API error responses
4. Test with curl/Postman before frontend integration

---

**Last Updated:** December 2, 2024  
**Version:** 1.0.0  
**License:** MIT
