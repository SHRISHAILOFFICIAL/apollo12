# Redis Timer Quick Reference

## 🚀 Quick Start (5 Minutes)

### 1. Start Redis Server

```bash
# Windows (download from GitHub first)
redis-server

# Linux/Mac
sudo systemctl start redis-server

# Verify
redis-cli ping  # Should return: PONG
```

### 2. Install Python Packages

```bash
cd backend
pip install django-redis redis
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Test Redis Connection

```bash
python test_redis_timer.py
```

### 5. Start Django Server

```bash
python manage.py runserver
```

---

## 📍 API Endpoints

| Method | Endpoint                                  | Purpose                  |
| ------ | ----------------------------------------- | ------------------------ |
| POST   | `/api/exam/timer/start/<exam_id>/`        | Start exam, create timer |
| GET    | `/api/exam/timer/remaining/<attempt_id>/` | Check remaining time     |
| POST   | `/api/exam/timer/submit-answer/`          | Save answer              |
| POST   | `/api/exam/timer/submit/<attempt_id>/`    | Submit exam              |
| GET    | `/api/exam/timer/questions/<attempt_id>/` | Get questions            |

---

## 🔑 Key Differences: Old vs New

| Feature  | Old (views_exam.py)     | New (views_exam_timer.py)       |
| -------- | ----------------------- | ------------------------------- |
| Timer    | ❌ No automatic timeout | ✅ Redis TTL auto-expires       |
| Endpoint | `/api/exam/start/`      | `/api/exam/timer/start/`        |
| Timeout  | ❌ Not enforced         | ✅ Automatic via Redis          |
| Resume   | ❌ Not supported        | ✅ Can resume if timer active   |
| Status   | ongoing, completed      | ongoing, completed, **timeout** |

---

## 💻 Code Examples

### Start Exam (Python)

```python
import requests

response = requests.post(
    'http://localhost:8000/api/exam/timer/start/1/',
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)
data = response.json()
# {'attempt_id': 123, 'remaining_seconds': 3600, ...}
```

### Check Time (JavaScript)

```javascript
const response = await fetch(
  `http://localhost:8000/api/exam/timer/remaining/${attemptId}/`,
  {
    headers: { Authorization: `Bearer ${token}` },
  }
);
const data = await response.json();
// {status: 'running', remaining_seconds: 2847}
```

### Submit Answer (curl)

```bash
curl -X POST http://localhost:8000/api/exam/timer/submit-answer/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "attempt_id": 123,
    "question_id": 1,
    "selected_option": "B"
  }'
```

---

## 🔧 Redis Commands

```bash
# View all timers
redis-cli KEYS "exam:timer:*"

# Check specific timer
redis-cli TTL "exam:timer:123"

# Get timer value
redis-cli GET "exam:timer:123"

# Delete specific timer
redis-cli DEL "exam:timer:123"

# Delete ALL timers (DANGER!)
redis-cli FLUSHDB
```

---

## ⚠️ Common Issues

### Issue: `ConnectionRefusedError`

**Solution:**

```bash
redis-server  # Start Redis first
```

### Issue: `NOAUTH Authentication required`

**Solution:** Add password to settings.py:

```python
"LOCATION": "redis://:yourpassword@127.0.0.1:6379/1"
```

### Issue: Timer not expiring

**Check TTL:**

```bash
redis-cli TTL "exam:timer:123"
# -2 = expired/missing
# -1 = no expiration set (error!)
# >0 = seconds remaining
```

---

## 📊 Status Codes

| Code | Meaning      | Action               |
| ---- | ------------ | -------------------- |
| 200  | Success      | Continue             |
| 201  | Exam started | Timer created        |
| 400  | Bad request  | Check validation     |
| 403  | Forbidden    | Not your attempt     |
| 404  | Not found    | Invalid attempt/exam |
| 410  | Gone         | Timer expired        |
| 500  | Server error | Check logs           |

---

## 🎯 Frontend Integration Checklist

- [ ] Update API base URL to use `/timer/` endpoints
- [ ] Add timer display component
- [ ] Poll `/remaining/` every 10 seconds
- [ ] Show warning at 5 minutes remaining
- [ ] Auto-submit when timer reaches 0
- [ ] Handle timeout status (410 response)
- [ ] Disable answer submission after timeout
- [ ] Show "Time Expired" message

---

## 📁 Files Created

```
backend/
├── api/
│   ├── redis_utils.py              # Timer manager
│   ├── serializers_exam_timer.py   # Serializers
│   ├── views_exam_timer.py         # Views with Redis
│   └── urls.py                     # Updated routes
├── config/
│   └── settings.py                 # Redis config added
├── core/
│   └── models.py                   # Added 'timeout' status
├── test_redis_timer.py             # Test script
├── REDIS_TIMER_DOCUMENTATION.md    # Full docs
└── requirements.txt                # Added redis packages
```

---

## 🧪 Testing Workflow

1. **Test Redis:**

   ```bash
   python test_redis_timer.py
   ```

2. **Test API with Postman/curl:**

   - Start exam → Get attempt_id
   - Check remaining → Should decrease
   - Submit answer → Should save
   - Wait for timeout → Should auto-expire
   - Submit exam → Should calculate score

3. **Test Frontend:**
   - Start exam → Timer displays
   - Timer counts down locally
   - Poll every 10s updates from server
   - Timeout shows alert
   - Submit works before timeout

---

## 🚀 Production Deployment

1. **Set environment variables:**

   ```bash
   export REDIS_HOST=your-redis-host.com
   export REDIS_PASSWORD=your-secure-password
   ```

2. **Update settings.py:**

   ```python
   REDIS_URL = f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:6379/1"
   ```

3. **Enable Redis persistence:**
   Edit `redis.conf`:

   ```conf
   save 900 1
   save 300 10
   ```

4. **Monitor Redis:**
   ```bash
   redis-cli INFO stats
   redis-cli MONITOR
   ```

---

## 📞 Support

**Before asking for help:**

1. ✅ Check Redis is running: `redis-cli ping`
2. ✅ Run test script: `python test_redis_timer.py`
3. ✅ Check Django logs for errors
4. ✅ Review REDIS_TIMER_DOCUMENTATION.md

**Common Questions:**

**Q: Can I use the old endpoints?**  
A: Yes! Old endpoints (`/api/exam/start/`) still work. New ones are at `/api/exam/timer/start/`.

**Q: Do I need to migrate existing data?**  
A: No. New attempts will use Redis. Old completed attempts are unaffected.

**Q: What happens if Redis crashes?**  
A: Ongoing exams will be marked as timeout when students try to continue. No data loss in MySQL.

---

**Last Updated:** December 2, 2024
