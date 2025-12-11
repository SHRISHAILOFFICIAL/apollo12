# Baseline Performance Testing Guide

## Tools Installed ✅
- **Django Debug Toolbar**: See query count and execution time
- **Locust**: Load testing with virtual users
- **Test Scripts**: Automated baseline measurement

## How to Run Baseline Tests

### **Option 1: Quick Baseline Test** (5 minutes)

```bash
cd e:\apollo11\apollo11\backend

# Make sure Django server is running
python manage.py runserver

# In another terminal, run baseline test
python test_baseline.py
```

**This will show:**
- Average exam load time
- Concurrent user capacity
- Where system starts failing

---

### **Option 2: Full Load Test with Locust** (Recommended)

**Step 1: Start Django Server**
```bash
cd e:\apollo11\apollo11\backend
python manage.py runserver
```

**Step 2: Start Locust** (in new terminal)
```bash
cd e:\apollo11\apollo11\backend
locust -f locustfile.py --host=http://localhost:8000
```

**Step 3: Open Browser**
- Go to: http://localhost:8089
- Enter number of users: Start with **100**
- Spawn rate: **10** users/second
- Click "Start Swarming"

**Step 4: Gradually Increase**
- Test with: 100 → 200 → 500 → 1000 users
- Watch for:
  - Response time (should be < 1000ms)
  - Failure rate (should be < 5%)
  - Requests per second

**When to stop:** When failure rate > 10% or response time > 3000ms

---

## Metrics to Record

Create this table:

| Metric | Current Value |
|--------|---------------|
| Max concurrent users (90% success) | ? |
| Average response time | ? ms |
| Requests per second | ? |
| Database queries per page | ? |
| Failure rate at 1000 users | ? % |

---

## Next Steps After Baseline

1. **Record current capacity** (e.g., "Can handle 250 users")
2. **Identify bottlenecks** (slow queries, high CPU, etc.)
3. **Implement optimizations** (Redis, query optimization)
4. **Re-test and compare**

---

## Need Help?

Run into issues? Common fixes:
- **Server not responding**: Restart Django server
- **Locust errors**: Check if endpoints exist
- **Connection refused**: Make sure server is on port 8000
