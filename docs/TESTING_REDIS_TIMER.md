# Testing Redis Timer Integration

## ✅ Complete Implementation Status

### Backend (Complete)

- ✅ Redis timer utilities (`api/redis_utils.py`)
- ✅ Timer API endpoints (`api/views_exam_timer.py`)
- ✅ URL routing (`api/urls.py`)
- ✅ Redis cache configuration (`config/settings.py`)
- ✅ Database migrations applied
- ✅ Redis connection verified

### Frontend (Complete)

- ✅ Timer service (`lib/services/exam-timer.service.ts`)
- ✅ Exam page updated (`app/exam/[id]/page.tsx`)
- ✅ TypeScript compilation successful

---

## 🧪 Testing Workflow

### 1. Start Redis (if not running)

```bash
# In WSL
sudo service redis-server start

# Verify
redis-cli ping
# Should return: PONG
```

### 2. Start Django Backend

```powershell
cd d:\quiz\backend
python manage.py runserver
```

### 3. Start Next.js Frontend

```powershell
cd d:\quiz\frontend
npm run dev
```

### 4. Monitor Redis Keys

```bash
# In WSL, open a new terminal
redis-cli

# Select database 1 (where timers are stored)
SELECT 1

# Watch for keys (run this before starting exam)
KEYS exam:timer:*

# Monitor TTL of a specific timer
TTL exam:timer:5  # Replace 5 with your attempt_id
```

---

## 📋 Test Scenarios

### Scenario 1: Normal Exam Flow

**Steps:**

1. Login to frontend (http://localhost:3000)
2. Navigate to dashboard
3. Click "Start Exam" on any exam
4. **Verify in Redis:**

   ```bash
   KEYS exam:timer:*
   # Should show: exam:timer:X (where X is attempt_id)

   TTL exam:timer:X
   # Should show remaining seconds (e.g., 599 for 10 min exam)
   ```

5. Answer some questions
6. Check timer updates every 10 seconds
7. Submit exam
8. **Verify in Redis:**
   ```bash
   KEYS exam:timer:*
   # Timer key should be deleted after submission
   ```

**Expected Results:**

- ✅ Timer displays in header (format: "09:59")
- ✅ Timer turns orange when < 5 minutes
- ✅ Timer turns red and pulses when < 1 minute
- ✅ Server polls every 10 seconds
- ✅ Local countdown updates every second
- ✅ Answers save successfully
- ✅ Redis timer deleted on submit
- ✅ Score calculated correctly

---

### Scenario 2: Exam Timeout (Auto-Submit)

**Steps:**

1. Start an exam with SHORT duration (2-3 minutes)
2. Wait for timer to expire
3. Observe auto-submission

**Expected Results:**

- ✅ Alert shows "Exam time has expired! Submitting automatically..."
- ✅ Exam submits without user action
- ✅ Score displayed in alert
- ✅ Redirect to dashboard
- ✅ Attempt status = "timeout" in database

**Verify in Database:**

```python
python manage.py shell

from core.models import Attempt
a = Attempt.objects.last()
print(a.status)  # Should be 'timeout'
print(a.score)   # Calculated score
```

---

### Scenario 3: Answer Submission with Timer Check

**Steps:**

1. Start exam
2. Answer questions
3. Try to answer after timer expires

**Expected Results:**

- ✅ Each answer triggers `POST /api/exam/timer/submit-answer/`
- ✅ If timer expired, returns **410 Gone**
- ✅ Frontend shows timeout alert
- ✅ Exam auto-submits

**Check Network Tab:**

- Status 200 = answer saved
- Status 410 = timer expired (triggers auto-submit)

---

### Scenario 4: Multiple Users

**Steps:**

1. Open two browsers (e.g., Chrome + Firefox)
2. Login with different users
3. Both start the SAME exam
4. Monitor Redis keys

**Expected Results:**

```bash
KEYS exam:timer:*
# Should show two keys:
# exam:timer:1
# exam:timer:2

# Each has independent TTL
TTL exam:timer:1
TTL exam:timer:2
```

- ✅ Timers independent per user
- ✅ No interference between users
- ✅ Both can submit separately

---

## 🔍 Debugging

### Check Redis Connection

```python
# In Django shell
python manage.py shell

from django_redis import get_redis_connection
redis_conn = get_redis_connection("default")
redis_conn.ping()  # True = working
redis_conn.dbsize()  # Number of keys
```

### Check Timer Details

```bash
# In redis-cli (SELECT 1 first)
GET exam:timer:5
# Returns: remaining seconds

TTL exam:timer:5
# Returns: -2 if expired, -1 if no expiry, >0 if active

# Force delete timer
DEL exam:timer:5
```

### Common Issues

**Problem:** Redis returns empty on `KEYS *`

- **Cause:** Using wrong database
- **Fix:** Run `SELECT 1` in redis-cli

**Problem:** Timer shows expired but exam continues

- **Cause:** Server polling not running
- **Fix:** Check browser console for errors in `getRemainingTime()` calls

**Problem:** 410 Gone error on answer submit

- **Cause:** Timer expired
- **Fix:** This is expected behavior - exam should auto-submit

**Problem:** Timer not deleted after submit

- **Cause:** Error in submit handler
- **Fix:** Check backend logs for errors in `SubmitExamView`

---

## 📊 API Endpoints

### New Redis Timer Endpoints (Use These!)

```
POST   /api/exam/timer/start/{exam_id}/      - Start exam + create Redis timer
GET    /api/exam/timer/remaining/{attempt_id}/ - Check remaining time
POST   /api/exam/timer/submit-answer/         - Submit answer (timer validated)
POST   /api/exam/timer/submit/{attempt_id}/   - Submit exam + delete timer
GET    /api/exam/timer/questions/{attempt_id}/ - Get questions + saved answers
```

### Legacy Endpoints (Do NOT use for timer testing)

```
POST   /api/attempts/start_exam/      - Old endpoint (no Redis)
POST   /api/attempts/{id}/submit_answer/ - Old endpoint (no timer check)
```

---

## 🎯 Success Criteria

### Backend Verification

- [ ] Redis ping successful
- [ ] `KEYS exam:timer:*` shows active timers
- [ ] TTL decreases over time
- [ ] POST `/api/exam/timer/start/1/` returns 201
- [ ] GET `/api/exam/timer/remaining/{id}/` returns correct seconds
- [ ] POST `/api/exam/timer/submit/{id}/` calculates score
- [ ] Timer deleted after submit

### Frontend Verification

- [ ] Timer displays in MM:SS format
- [ ] Timer color changes (green → orange → red)
- [ ] Local countdown smooth (1/sec)
- [ ] Server sync every 10 seconds
- [ ] Timeout triggers auto-submit
- [ ] Score alert shows after submit

### Database Verification

```python
from core.models import Attempt, Response

# Check attempt
a = Attempt.objects.last()
print(f"Status: {a.status}")  # 'completed' or 'timeout'
print(f"Score: {a.score}")
print(f"Submitted: {a.submitted_at}")

# Check responses
Response.objects.filter(attempt=a).count()  # Number of answers
```

---

## 🚀 Quick Test Script

Run this to verify complete flow:

```bash
# Terminal 1: Redis monitor
redis-cli
SELECT 1
MONITOR

# Terminal 2: Django
cd d:\quiz\backend
python manage.py runserver

# Terminal 3: Frontend
cd d:\quiz\frontend
npm run dev

# Browser: http://localhost:3000
# 1. Login
# 2. Start exam
# 3. Watch Redis monitor show timer creation
# 4. Answer questions
# 5. Submit
# 6. Watch Redis monitor show timer deletion
```

---

## 📝 Test Checklist

- [ ] Redis running on WSL
- [ ] Backend running (port 8000)
- [ ] Frontend running (port 3000)
- [ ] Login successful
- [ ] Exam starts (Redis timer created)
- [ ] Timer displays correctly
- [ ] Timer color changes work
- [ ] Server polling every 10 seconds
- [ ] Answers save successfully
- [ ] Submit works (timer deleted)
- [ ] Score calculated
- [ ] Timeout auto-submit works
- [ ] 410 error handled correctly

---

## 🔗 Related Documentation

- **REDIS_TIMER_DOCUMENTATION.md** - Complete technical docs (37 pages)
- **REDIS_QUICK_REFERENCE.md** - Quick API reference
- **TROUBLESHOOTING_REDIS_TIMER.md** - Detailed debugging guide
- **GETTING_STARTED.md** - Setup instructions
