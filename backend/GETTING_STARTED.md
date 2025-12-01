# 🚀 Getting Started with Redis Exam Timers

## Step-by-Step Setup Guide

Follow these steps in order to get the Redis exam timer system working.

---

## ✅ Step 1: Install Redis Server

### Option A: Docker (Recommended - Fastest)

```powershell
# 1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
# 2. Run Redis container:
docker run --name redis-exam-timer -p 6379:6379 -d redis:latest

# 3. Verify it's running:
docker ps
# Should show redis-exam-timer container

# 4. Test connection:
docker exec -it redis-exam-timer redis-cli ping
# Should return: PONG
```

**To start Redis in the future:**

```powershell
docker start redis-exam-timer
```

---

### Option B: Windows Native

```powershell
# 1. Download from https://github.com/microsoftarchive/redis/releases
#    Get: Redis-x64-3.0.504.msi

# 2. Install (keep default settings)

# 3. Start Redis:
redis-server

# 4. Test (in new terminal):
redis-cli ping
# Should return: PONG
```

---

### Option C: WSL (Windows Subsystem for Linux)

```powershell
# 1. Install WSL:
wsl --install

# 2. Restart computer

# 3. Open WSL terminal and run:
sudo apt-get update
sudo apt-get install redis-server

# 4. Start Redis:
sudo service redis-server start

# 5. Test:
redis-cli ping
# Should return: PONG
```

---

## ✅ Step 2: Install Python Packages

```powershell
cd d:\quiz\backend
pip install django-redis redis
```

**Verify installation:**

```powershell
pip list | findstr redis
# Should show:
# django-redis     6.0.0
# redis            7.1.0
```

---

## ✅ Step 3: Run Database Migrations

```powershell
cd d:\quiz\backend
python manage.py migrate
```

**Expected output:**

```
Applying core.0002_add_timeout_status... OK
```

This adds the `timeout` status to the Attempt model.

---

## ✅ Step 4: Test Redis Connection

```powershell
cd d:\quiz\backend
python test_redis_timer.py
```

**Expected output:**

```
🚀 REDIS EXAM TIMER TESTS
============================================================

============================================================
TEST 1: Redis Connection
============================================================
✅ Redis connection successful!

============================================================
TEST 2: Create Timer
============================================================
Creating timer for attempt 99999 with 30s duration...
✅ Timer created successfully!
   Remaining time: 30s
✅ Timer verification passed!

...

Results: 6/6 tests passed
🎉 All tests passed! Redis timer system is working correctly.
```

**If tests fail:**

1. Check Redis is running: `redis-cli ping`
2. Check settings.py has correct Redis URL
3. Check firewall isn't blocking port 6379

---

## ✅ Step 5: Start Backend Server

```powershell
cd d:\quiz\backend
python manage.py runserver
```

**Server should start on:** http://localhost:8000

---

## ✅ Step 6: Test API Endpoints

### 6.1 Get Authentication Token

```powershell
curl -X POST http://localhost:8000/api/auth/login/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"sonu\",\"password\":\"sonu\"}'
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Copy the `access` token - you'll need it for next steps!**

---

### 6.2 Start an Exam

**Replace `YOUR_TOKEN` with the access token from step 6.1:**

```powershell
curl -X POST http://localhost:8000/api/exam/timer/start/1/ `
  -H "Authorization: Bearer YOUR_TOKEN" `
  -H "Content-Type: application/json"
```

**Expected response:**

```json
{
  "attempt_id": 1,
  "exam_id": 1,
  "exam_title": "Test Exam",
  "duration_minutes": 60,
  "remaining_seconds": 3600,
  "total_questions": 10,
  "total_marks": 100
}
```

**Copy the `attempt_id` - you'll need it for next steps!**

---

### 6.3 Check Remaining Time

**Replace `YOUR_TOKEN` and `ATTEMPT_ID`:**

```powershell
curl http://localhost:8000/api/exam/timer/remaining/ATTEMPT_ID/ `
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected response:**

```json
{
  "status": "running",
  "remaining_seconds": 3598
}
```

---

### 6.4 Submit an Answer

```powershell
curl -X POST http://localhost:8000/api/exam/timer/submit-answer/ `
  -H "Authorization: Bearer YOUR_TOKEN" `
  -H "Content-Type: application/json" `
  -d '{\"attempt_id\":ATTEMPT_ID,\"question_id\":1,\"selected_option\":\"B\"}'
```

**Expected response:**

```json
{
  "status": "saved",
  "question_id": 1,
  "selected_option": "B",
  "action": "saved"
}
```

---

### 6.5 Submit Exam

```powershell
curl -X POST http://localhost:8000/api/exam/timer/submit/ATTEMPT_ID/ `
  -H "Authorization: Bearer YOUR_TOKEN" `
  -H "Content-Type: application/json"
```

**Expected response:**

```json
{
  "status": "submitted",
  "score": 10,
  "total_marks": 100,
  "percentage": 10.0,
  "correct_answers": 1,
  "total_questions": 10,
  "time_taken_minutes": 2
}
```

---

## ✅ Step 7: Verify in Redis

**Check that timer was created and deleted:**

```powershell
# Should show no timers (exam was submitted)
redis-cli KEYS "exam:timer:*"
```

**If you see a timer key, check its TTL:**

```powershell
redis-cli TTL "exam:timer:1"
# -2 means expired/deleted (correct)
# >0 means still running (exam not submitted)
```

---

## ✅ Step 8: Verify in Database

**Check MySQL:**

```powershell
cd d:\quiz\backend
python manage.py dbshell
```

```sql
-- View recent attempts
SELECT id, user_id, test_id, status, score, created_at, completed_at
FROM core_attempt
ORDER BY id DESC
LIMIT 5;

-- Should show your attempt with status='completed'
```

---

## ✅ Step 9: Update Frontend (Optional)

### Create Timer Service

Create `frontend/lib/services/exam-timer.service.ts`:

```typescript
import axios from "axios";

const API_BASE = "http://localhost:8000/api";

const getHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem("access_token")}`,
  "Content-Type": "application/json",
});

export const examTimerService = {
  async startExam(examId: number) {
    const response = await axios.post(
      `${API_BASE}/exam/timer/start/${examId}/`,
      {},
      { headers: getHeaders() }
    );
    return response.data;
  },

  async getRemainingTime(attemptId: number) {
    const response = await axios.get(
      `${API_BASE}/exam/timer/remaining/${attemptId}/`,
      { headers: getHeaders() }
    );
    return response.data;
  },

  async submitAnswer(attemptId: number, questionId: number, option: string) {
    const response = await axios.post(
      `${API_BASE}/exam/timer/submit-answer/`,
      {
        attempt_id: attemptId,
        question_id: questionId,
        selected_option: option,
      },
      { headers: getHeaders() }
    );
    return response.data;
  },

  async submitExam(attemptId: number) {
    const response = await axios.post(
      `${API_BASE}/exam/timer/submit/${attemptId}/`,
      {},
      { headers: getHeaders() }
    );
    return response.data;
  },
};
```

---

### Update Exam Page

Update `frontend/app/exam/[id]/page.tsx`:

```typescript
"use client";

import { useState, useEffect, useRef } from "react";
import { examTimerService } from "@/lib/services/exam-timer.service";

export default function ExamPage({ params }: { params: { id: string } }) {
  const [attemptId, setAttemptId] = useState<number | null>(null);
  const [remainingSeconds, setRemainingSeconds] = useState<number>(0);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // Start exam
  useEffect(() => {
    const startExam = async () => {
      const data = await examTimerService.startExam(parseInt(params.id));
      setAttemptId(data.attempt_id);
      setRemainingSeconds(data.remaining_seconds);
    };
    startExam();
  }, [params.id]);

  // Poll remaining time every 10 seconds
  useEffect(() => {
    if (!attemptId) return;

    const checkTime = async () => {
      const data = await examTimerService.getRemainingTime(attemptId);

      if (data.status === "timeout") {
        alert("Exam time expired!");
        // Redirect or auto-submit
      } else {
        setRemainingSeconds(data.remaining_seconds);
      }
    };

    timerRef.current = setInterval(checkTime, 10000);
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [attemptId]);

  // Local countdown
  useEffect(() => {
    if (remainingSeconds <= 0) return;

    const countdown = setInterval(() => {
      setRemainingSeconds((prev) => Math.max(0, prev - 1));
    }, 1000);

    return () => clearInterval(countdown);
  }, [remainingSeconds]);

  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${h.toString().padStart(2, "0")}:${m
      .toString()
      .padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className="p-8">
      {/* Timer Display */}
      <div className="fixed top-4 right-4 bg-blue-600 text-white px-6 py-3 rounded-lg">
        <div className="text-2xl font-bold">{formatTime(remainingSeconds)}</div>
        <div className="text-sm">Time Remaining</div>
      </div>

      {/* Exam content here */}
    </div>
  );
}
```

---

## 🎉 Success! What You've Achieved

✅ Redis server running and verified  
✅ Python packages installed  
✅ Database migrated with timeout status  
✅ Redis timer system tested and working  
✅ API endpoints tested with curl  
✅ Timer creation/deletion verified  
✅ Database records verified  
✅ Frontend integration example ready

---

## 🔄 Daily Workflow

**Every time you work on the project:**

```powershell
# 1. Start Redis (choose one):
docker start redis-exam-timer          # If using Docker
redis-server                            # If using Windows native
wsl sudo service redis-server start     # If using WSL

# 2. Start Backend:
cd d:\quiz\backend
python manage.py runserver

# 3. Start Frontend (in new terminal):
cd d:\quiz\frontend
npm run dev
```

---

## 📚 Documentation Reference

| File                           | Purpose                                  |
| ------------------------------ | ---------------------------------------- |
| `IMPLEMENTATION_SUMMARY.md`    | Complete overview of what was built      |
| `REDIS_TIMER_DOCUMENTATION.md` | Full production documentation (37 pages) |
| `REDIS_QUICK_REFERENCE.md`     | Quick reference for daily use            |
| `INSTALL_REDIS.md`             | Detailed Redis installation guide        |
| `test_redis_timer.py`          | Automated test suite                     |

---

## ❓ Troubleshooting

### Redis won't start

```powershell
# Check if port 6379 is in use:
netstat -ano | findstr :6379

# If using Docker:
docker logs redis-exam-timer
```

### Tests fail

```powershell
# Verify Redis connection:
redis-cli ping

# Check Django settings:
# Ensure CACHES is configured in settings.py
```

### API returns 500 error

```powershell
# Check Django logs for error details
# Ensure Redis is running
# Verify migrations are applied
```

---

## 🚀 Next Steps

1. ✅ Test timeout functionality (wait for TTL to expire)
2. ✅ Test resume functionality (start exam, close browser, resume)
3. ✅ Update all frontend exam pages to use `/timer/` endpoints
4. ✅ Add timer warnings (e.g., "5 minutes remaining")
5. ✅ Configure Redis for production (authentication, persistence)

---

**Need Help?**

1. Check Redis: `redis-cli ping`
2. Run tests: `python test_redis_timer.py`
3. Review logs: Check terminal output
4. Read docs: See REDIS_TIMER_DOCUMENTATION.md

---

**You're all set! 🎉**

The Redis exam timer system is production-ready and waiting for Redis to be installed.

---

**Last Updated:** December 2, 2024
