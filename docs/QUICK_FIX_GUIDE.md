# Quick Fix Guide for Current Errors

## Errors You're Seeing

### 1. AxiosError: Request aborted

**Cause:** Authentication token issue or browser aborting the request

### 2. Failed to load chunk (HMR error)

**Cause:** Next.js Hot Module Replacement issue (development only)

---

## Quick Fixes

### Fix 1: Restart Next.js Dev Server

**Option A: Stop and Restart (Recommended)**

```powershell
# In the terminal running npm run dev, press Ctrl+C
# Then restart:
cd d:\quiz\frontend
npm run dev
```

**Option B: Hard Restart**

```powershell
# Kill the process
taskkill /F /IM node.exe
# Or find and kill specific port:
netstat -ano | findstr :3000
taskkill /F /PID <PID_NUMBER>

# Clean and restart
cd d:\quiz\frontend
Remove-Item -Recurse -Force .next
npm run dev
```

---

### Fix 2: Clear Browser Cache

1. Open DevTools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"
4. Or just press: **Ctrl + Shift + R**

---

### Fix 3: Verify Authentication

**Check if you're logged in:**

1. Open browser console (F12)
2. Run:

```javascript
console.log(localStorage.getItem("access_token"));
```

**If it returns `null`:**

- You're not logged in
- Go to http://localhost:3000/auth/login
- Login first, then try starting exam

**If it returns a token:**

- Token might be expired
- Try logging out and logging in again

---

### Fix 4: Check Backend is Running

```powershell
# Check if backend is responding
curl http://localhost:8000/api/

# Should return DRF browsable API page
```

If backend isn't running:

```powershell
cd d:\quiz\backend
python manage.py runserver
```

---

## Step-by-Step Test

### 1. Ensure Everything is Running

**Terminal 1: Backend**

```powershell
cd d:\quiz\backend
python manage.py runserver
# Should show: Starting development server at http://127.0.0.1:8000/
```

**Terminal 2: Frontend**

```powershell
cd d:\quiz\frontend
npm run dev
# Should show: Ready on http://localhost:3000
```

**Terminal 3: Redis (WSL)**

```bash
sudo service redis-server start
redis-cli ping
# Should return: PONG
```

---

### 2. Login First

1. Go to http://localhost:3000
2. Click "Login" (or go to /auth/login)
3. Enter credentials
4. Verify you see dashboard

---

### 3. Check Network Tab

1. Open DevTools (F12)
2. Go to Network tab
3. Click "Start Exam"
4. Look for POST request to `/api/exam/timer/start/1/`

**Expected Response:**

- Status: **200 OK**
- Response body:

```json
{
  "attempt_id": 1,
  "exam_id": 1,
  "exam_title": "Test Exam",
  "duration_minutes": 10,
  "remaining_seconds": 600,
  ...
}
```

**If you see 401 Unauthorized:**

- Token is missing or invalid
- Check Request Headers → Should have: `Authorization: Bearer <token>`
- If missing, you're not logged in properly

---

### 4. Check Request Headers

In Network tab, click the failed request:

- **Headers tab**
- **Request Headers** section
- Should see:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**If Authorization header is missing:**

- Token not in localStorage
- Login again

---

## Common Issues & Solutions

### Issue: "Request aborted" immediately

**Cause:** Browser is blocking the request or endpoint doesn't exist

**Fix:**

1. Check browser console for CORS errors
2. Verify endpoint in Network tab
3. Confirm backend URLs are correct

---

### Issue: HMR chunk loading error keeps appearing

**Cause:** Next.js development server cache corruption

**Fix:**

```powershell
cd d:\quiz\frontend
Remove-Item -Recurse -Force .next
Remove-Item -Recurse -Force node_modules/.cache
npm run dev
```

---

### Issue: 401 Unauthorized on /exam/timer/start/

**Cause:** Not logged in or token expired

**Fix:**

1. Logout: `localStorage.clear()`
2. Go to /auth/login
3. Login again
4. Try starting exam again

---

### Issue: Duplicate requests in Network tab

**Cause:** React Strict Mode (development only, not a problem)

**Fix:** Ignore it, or disable Strict Mode in `app/layout.tsx` (not recommended)

---

## Verify Redis Timer Creation

After successfully starting exam:

```bash
# In WSL
redis-cli
SELECT 1
KEYS exam:timer:*
# Should show: 1) "exam:timer:1"

TTL exam:timer:1
# Should show remaining seconds (e.g., 599)
```

---

## Backend Logs to Watch

When you start an exam, you should see in backend terminal:

```
[02/Dec/2025 01:24:18] "POST /api/exam/timer/start/1/ HTTP/1.1" 200 181
[02/Dec/2025 01:24:18] "GET /api/exam/timer/questions/1/ HTTP/1.1" 200 75
[02/Dec/2025 01:24:18] "GET /api/exam/timer/remaining/1/ HTTP/1.1" 200 45
```

**If you see:**

```
Unauthorized: /api/exam/timer/start/1/
[02/Dec/2025 01:24:51] "GET /api/exam/timer/start/1/ HTTP/1.1" 401 8824
```

→ You're not authenticated (no token or invalid token)

---

## Quick Test Commands

### Test Authentication

```javascript
// In browser console
fetch("http://localhost:8000/api/exams/?is_published=true", {
  headers: {
    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
  },
})
  .then((r) => r.json())
  .then(console.log);
```

### Test Timer Endpoint Directly

```javascript
// In browser console (after logging in)
fetch("http://localhost:8000/api/exam/timer/start/1/", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
    "Content-Type": "application/json",
  },
})
  .then((r) => r.json())
  .then(console.log);
```

---

## Still Not Working?

### Detailed Debugging

**1. Check localStorage:**

```javascript
console.log({
  access: localStorage.getItem("access_token"),
  refresh: localStorage.getItem("refresh_token"),
});
```

**2. Check API client:**

```javascript
import api from "@/lib/api";
api
  .get("/exams/?is_published=true")
  .then((r) => console.log("API works:", r.data))
  .catch((e) => console.error("API failed:", e));
```

**3. Check exam timer service:**

```javascript
import { examTimerService } from "@/lib/services/exam-timer.service";
examTimerService
  .startExam(1)
  .then((r) => console.log("Timer started:", r))
  .catch((e) => console.error("Timer failed:", e));
```

---

## Most Likely Solution

Based on the errors, the most likely fix is:

1. **Clear browser cache** (Ctrl + Shift + R)
2. **Ensure you're logged in** (check localStorage)
3. **Restart Next.js dev server** (Ctrl+C, then `npm run dev`)

The HMR error is harmless and will go away after restart. The AxiosError is likely authentication - make sure you login before starting an exam.

---

## Expected Workflow

```
1. Login → Token saved to localStorage
2. Go to Dashboard → Sees list of exams
3. Click "Start Exam" → POST /api/exam/timer/start/1/
4. Backend creates Redis timer → Returns attempt_id
5. Frontend loads questions → GET /api/exam/timer/questions/1/
6. Timer starts counting down
7. Server polls every 10 seconds → GET /api/exam/timer/remaining/1/
```

If any step fails, check that step specifically using Network tab in DevTools.
