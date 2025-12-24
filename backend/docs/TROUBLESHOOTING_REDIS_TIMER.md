# Redis Timer Test - Manual Steps

## Current Situation

✅ Redis is running on WSL  
✅ Django can connect to Redis (verified with `debug_redis.py`)  
❌ Timer keys not being created in Redis when using API

---

## Diagnosis

The issue is likely that the **old exam endpoints** are being used instead of the **new timer endpoints**.

### Old Endpoints (No Redis Timer):

- `POST /api/exam/start/<test_id>/` ❌ No timer
- `POST /api/exam/submit-answer/` ❌ No timer
- `POST /api/exam/submit/` ❌ No timer

### New Timer Endpoints (With Redis):

- `POST /api/exam/timer/start/<exam_id>/` ✅ Creates timer
- `GET /api/exam/timer/remaining/<attempt_id>/` ✅ Checks timer
- `POST /api/exam/timer/submit-answer/` ✅ Validates timer
- `POST /api/exam/timer/submit/<attempt_id>/` ✅ Deletes timer

---

## Solution: Use the Correct Endpoints

### Step 1: Make sure Django server is running

```powershell
# In terminal 1:
cd d:\quiz\backend
python manage.py runserver
```

### Step 2: Test with curl (PowerShell)

**Login:**

```powershell
$loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"username":"sonu","password":"sonu"}'

$token = $loginResponse.access
Write-Host "Token: $token"
```

**Start Exam WITH TIMER (correct endpoint):**

```powershell
$headers = @{
  "Authorization" = "Bearer $token"
  "Content-Type" = "application/json"
}

$startResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/exam/timer/start/1/" `
  -Method POST `
  -Headers $headers

Write-Host "Response:"
$startResponse | ConvertTo-Json
$attemptId = $startResponse.attempt_id
Write-Host "Attempt ID: $attemptId"
```

**Check in Redis (WSL terminal):**

```bash
redis-cli
SELECT 1
KEYS exam:timer:*
TTL exam:timer:<attempt_id>  # Replace with actual attempt ID
GET exam:timer:<attempt_id>
```

---

## Quick Verification Script

Run this in PowerShell to test the timer endpoint:

```powershell
# Login
$login = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -ContentType "application/json" -Body '{"username":"sonu","password":"sonu"}'
$token = $login.access

# Start exam with timer
$headers = @{"Authorization" = "Bearer $token"; "Content-Type" = "application/json"}
$exam = Invoke-RestMethod -Uri "http://localhost:8000/api/exam/timer/start/1/" -Method POST -Headers $headers

Write-Host "✅ Exam started! Attempt ID: $($exam.attempt_id)"
Write-Host "Remaining: $($exam.remaining_seconds) seconds"

# Check remaining time
$timer = Invoke-RestMethod -Uri "http://localhost:8000/api/exam/timer/remaining/$($exam.attempt_id)/" -Method GET -Headers $headers

Write-Host "Timer status: $($timer.status)"
Write-Host "Time left: $($timer.remaining_seconds) seconds"

Write-Host "`nNow check in WSL:"
Write-Host "  redis-cli"
Write-Host "  SELECT 1"
Write-Host "  KEYS exam:timer:*"
Write-Host "  TTL exam:timer:$($exam.attempt_id)"
```

---

## Frontend Fix

If your frontend is using the old endpoints, update:

**Before (No Timer):**

```typescript
await axios.post("/api/exam/start/1/"); // ❌ Old
```

**After (With Timer):**

```typescript
await axios.post("/api/exam/timer/start/1/"); // ✅ New
```

---

## Verification Checklist

- [ ] Django server running on port 8000
- [ ] Redis running in WSL (check with `redis-cli ping` in WSL)
- [ ] Using `/api/exam/timer/start/` endpoint (NOT `/api/exam/start/`)
- [ ] Redis database 1 selected (settings.py has `/1` in LOCATION)
- [ ] Check Redis keys after starting exam: `redis-cli` → `SELECT 1` → `KEYS exam:timer:*`

---

## Expected Redis Output After Starting Exam

```bash
127.0.0.1:6379> SELECT 1
OK
127.0.0.1:6379[1]> KEYS exam:timer:*
1) "exam:timer:47"  # Your attempt ID here
127.0.0.1:6379[1]> TTL exam:timer:47
(integer) 3594  # Seconds remaining
127.0.0.1:6379[1]> GET exam:timer:47
"3600"  # Initial duration in seconds
```

---

## Common Mistakes

1. ❌ Using `/api/exam/start/` instead of `/api/exam/timer/start/`
2. ❌ Checking database 0 instead of database 1 in Redis
3. ❌ Django server not running
4. ❌ Redis not running in WSL
5. ❌ Using wrong exam ID (use an existing, published exam)

---

## Next Steps

1. Make sure you're using the **NEW** timer endpoints
2. Run the PowerShell verification script above
3. Check Redis immediately after starting the exam
4. If still not working, check Django server logs for errors

The system is working correctly - you just need to use the right endpoints! 🎯
