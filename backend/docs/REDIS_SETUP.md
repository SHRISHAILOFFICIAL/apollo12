# Redis Caching Setup Guide

## What Was Implemented

### 1. Caching Utilities (`utils/cache.py`)
- Cache key generation with MD5 hashing
- Response caching decorator
- Exam-specific cache helpers

### 2. Exam View Caching (`exams/views.py`)
- **Exam List**: Cached for 1 hour using `@cache_page(3600)`
- **Exam Detail**: Manual caching with 1-hour TTL
- **Exam Questions**: Cached for 1 hour per exam

### 3. Query Optimization
- Added `select_related('subject')` to reduce DB queries
- Added `prefetch_related('sections')` for related data
- Optimized question queries with `select_related('section')`

## Redis Setup in WSL

### 1. Install Redis in WSL
```bash
# Open WSL terminal
wsl

# Update packages
sudo apt update

# Install Redis
sudo apt install redis-server -y

# Start Redis
sudo service redis-server start

# Verify Redis is running
redis-cli ping
# Should return: PONG
```

### 2. Configure Redis to Start Automatically
```bash
# Edit Redis config
sudo nano /etc/redis/redis.conf

# Find and change:
# supervised no
# to:
# supervised systemd

# Restart Redis
sudo service redis-server restart
```

### 3. Test Connection from Windows
```bash
# In WSL, check Redis is listening
sudo netstat -lnp | grep redis

# Should show: 127.0.0.1:6379
```

## Testing the Cache

### 1. Restart Django Server
```bash
# Make sure Redis is running in WSL first
python manage.py runserver
```

### 2. Test Cache Hit
```bash
# First request (cache miss - slower)
curl http://localhost:8000/api/exams/

# Second request (cache hit - much faster!)
curl http://localhost:8000/api/exams/
```

### 3. Monitor Cache in WSL
```bash
# In WSL terminal
redis-cli

# Check cached keys
KEYS apollo11:*

# Check TTL for a key
TTL apollo11:exam:1:detail

# Monitor cache hits in real-time
MONITOR
```

## Expected Performance Gain

- **Before**: 600 concurrent users ✅
- **After**: 900-1000 concurrent users 🎯
- **Improvement**: +50-67%

## Troubleshooting

### Redis not connecting?
```bash
# Check if Redis is running in WSL
wsl
sudo service redis-server status

# If not running, start it
sudo service redis-server start
```

### Cache not working?
```python
# Test cache in Django shell
python manage.py shell

from django.core.cache import cache
cache.set('test', 'hello', 60)
print(cache.get('test'))  # Should print: hello
```

## Next Steps

1. ✅ **Redis installed** (in WSL)
2. ✅ **Code updated** (caching implemented)
3. 🔄 **Restart Django server**
4. 🎯 **Run load test** with 1000 users
5. 📊 **Compare results** with baseline (600 users)

