# Installing Redis on Windows

## ⚠️ IMPORTANT: Redis Installation Required

The Redis timer system requires Redis server to be running. Currently, Redis is **NOT installed** on your system.

---

## 🪟 Option 1: Redis for Windows (Recommended for Development)

### Download and Install

1. **Download Redis for Windows:**

   - Visit: https://github.com/microsoftarchive/redis/releases
   - Download: `Redis-x64-3.0.504.msi` (or latest version)

2. **Install:**

   - Run the MSI installer
   - Keep default installation path: `C:\Program Files\Redis`
   - Check "Add to PATH" option

3. **Start Redis:**

   ```powershell
   redis-server
   ```

4. **Verify (in new terminal):**
   ```powershell
   redis-cli ping
   # Should return: PONG
   ```

---

## 🐧 Option 2: WSL (Windows Subsystem for Linux)

### Install WSL and Redis

```powershell
# Install WSL
wsl --install

# Restart computer, then open WSL terminal and run:
sudo apt-get update
sudo apt-get install redis-server

# Start Redis
sudo service redis-server start

# Verify
redis-cli ping
# Should return: PONG
```

### Running Redis in WSL

**Every time you restart computer:**

```bash
# In WSL terminal:
sudo service redis-server start
```

**Keep Redis running in background:**

```bash
# In WSL terminal:
redis-server --daemonize yes
```

---

## 🐳 Option 3: Docker (Recommended for Production-like Setup)

### Install Docker Desktop

1. Download: https://www.docker.com/products/docker-desktop
2. Install and restart computer

### Run Redis Container

```powershell
# Pull Redis image
docker pull redis:latest

# Run Redis container
docker run --name redis-exam-timer -p 6379:6379 -d redis:latest

# Verify
docker exec -it redis-exam-timer redis-cli ping
# Should return: PONG
```

### Useful Docker Commands

```powershell
# Start Redis container
docker start redis-exam-timer

# Stop Redis container
docker stop redis-exam-timer

# View Redis logs
docker logs redis-exam-timer

# Access Redis CLI
docker exec -it redis-exam-timer redis-cli
```

---

## ⚙️ Configuration After Installation

### Test Django Connection

```powershell
cd d:\quiz\backend
python test_redis_timer.py
```

### Expected Output:

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

---

## 🔧 Troubleshooting

### Issue: "redis-cli not recognized"

**Windows PATH issue:**

1. Open System Properties → Environment Variables
2. Add to PATH: `C:\Program Files\Redis`
3. Restart PowerShell

### Issue: "Connection refused" in Django

**Redis not running:**

```powershell
# Start Redis server
redis-server

# Or if using Docker:
docker start redis-exam-timer

# Or if using WSL:
wsl sudo service redis-server start
```

### Issue: Port 6379 already in use

**Find what's using the port:**

```powershell
netstat -ano | findstr :6379
```

**Kill the process:**

```powershell
taskkill /PID <process_id> /F
```

---

## 🎯 Quick Start After Installation

1. **Start Redis:**

   ```powershell
   # Windows:
   redis-server

   # Docker:
   docker start redis-exam-timer

   # WSL:
   wsl sudo service redis-server start
   ```

2. **Test Connection:**

   ```powershell
   redis-cli ping
   ```

3. **Run Django Tests:**

   ```powershell
   cd d:\quiz\backend
   python test_redis_timer.py
   ```

4. **Start Django Server:**
   ```powershell
   python manage.py runserver
   ```

---

## 📊 Redis Configuration for Production

### Enable Persistence

Edit `redis.conf` (location varies by installation):

```conf
# Save DB to disk
save 900 1      # Save if 1 key changed in 15 minutes
save 300 10     # Save if 10 keys changed in 5 minutes
save 60 10000   # Save if 10000 keys changed in 1 minute

# DB filename
dbfilename dump.rdb

# Working directory
dir ./
```

### Enable Authentication

```conf
# Set password
requirepass your_secure_password_here
```

**Update Django settings.py:**

```python
CACHES = {
    "default": {
        "LOCATION": "redis://:your_secure_password_here@127.0.0.1:6379/1",
    }
}
```

---

## 🚀 Recommended Setup by Environment

### Development (Local PC)

✅ **Redis for Windows MSI** - Easiest setup

### Testing (Team Collaboration)

✅ **Docker** - Consistent across all machines

### Production (Server)

✅ **Linux Server with Redis** - Best performance

---

## 📝 Next Steps

After installing Redis:

1. ✅ Start Redis server
2. ✅ Run `redis-cli ping` to verify
3. ✅ Run `python test_redis_timer.py`
4. ✅ Start Django: `python manage.py runserver`
5. ✅ Test API endpoints (see REDIS_QUICK_REFERENCE.md)
6. ✅ Update frontend to use `/api/exam/timer/` endpoints

---

## 💡 Tips

- **Auto-start Redis on boot (Windows):**
  Use Task Scheduler to run `redis-server` at startup

- **Monitor Redis in real-time:**

  ```powershell
  redis-cli MONITOR
  ```

- **Check Redis memory usage:**

  ```powershell
  redis-cli INFO memory
  ```

- **Flush all Redis data (DANGER!):**
  ```powershell
  redis-cli FLUSHALL
  ```

---

**Need Help?**

1. Check Redis is running: `redis-cli ping`
2. Check Django can connect: `python test_redis_timer.py`
3. Review logs: `redis-cli INFO server`
4. Check firewall isn't blocking port 6379

---

**Last Updated:** December 2, 2024
