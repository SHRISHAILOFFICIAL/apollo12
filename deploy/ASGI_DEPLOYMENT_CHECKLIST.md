# ASGI Deployment Checklist

## Pre-Deployment

- [ ] Backup current deployment
  ```bash
  cd /var/www/dcet-platform
  git stash  # Save any local changes
  git branch backup-wsgi  # Create backup branch
  ```

- [ ] Review changes
  - [ ] `requirements-prod.txt` - Uvicorn added, gevent removed
  - [ ] `gunicorn.conf.py` - 4 workers, UvicornWorker class
  - [ ] `dcet-backend.service` - config.asgi:application

## Deployment Steps

### 1. Push Changes to GitHub

```bash
# On local machine (Windows)
cd d:\apollo12
git add .
git commit -m "feat: migrate to ASGI with Gunicorn + Uvicorn Workers"
git push origin main
```

### 2. Pull Changes on Server

```bash
# SSH into server
ssh user@192.168.54.75

# Navigate to project
cd /var/www/dcet-platform

# Pull latest code
git pull origin main
```

### 3. Update Dependencies

```bash
cd /var/www/dcet-platform/backend
source ../venv/bin/activate

# Install new dependencies
pip install --upgrade -r requirements-prod.txt

# Verify installations
python -c "import uvicorn; print('Uvicorn:', uvicorn.__version__)"
python -c "import uvloop; print('uvloop:', uvloop.__version__)"
python -c "import httptools; print('httptools installed')"

# Remove old gevent if present
pip uninstall gevent greenlet -y
```

### 4. Update Systemd Service

```bash
# Copy new service file
sudo cp /var/www/dcet-platform/deploy/dcet-backend.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Verify service file
cat /etc/systemd/system/dcet-backend.service | grep "config.asgi"
# Should show: ExecStart=.../gunicorn -c gunicorn.conf.py config.asgi:application
```

### 5. Test Configuration

```bash
cd /var/www/dcet-platform/backend
source ../venv/bin/activate

# Test ASGI app loads
python -c "from config.asgi import application; print('ASGI OK')"

# Test Gunicorn config
gunicorn --check-config -c gunicorn.conf.py config.asgi:application
# Should exit with no errors
```

### 6. Restart Services

```bash
# Stop backend service
sudo systemctl stop dcet-backend

# Wait 5 seconds
sleep 5

# Start with new ASGI configuration
sudo systemctl start dcet-backend

# Check status
sudo systemctl status dcet-backend
```

### 7. Verify Deployment

```bash
# Run verification script
cd /var/www/dcet-platform/deploy
chmod +x verify_asgi.sh
sudo ./verify_asgi.sh

# Check worker processes (should see 4 workers)
ps aux | grep gunicorn

# Monitor logs for errors
sudo journalctl -u dcet-backend -f --lines=50
```

### 8. Test API Endpoints

```bash
# Test health check
curl http://192.168.54.75/health

# Test API root
curl http://192.168.54.75/api/

# Test authentication (if setup)
curl -X POST http://192.168.54.75/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

## Post-Deployment Verification

### Monitor Performance

- [ ] CPU usage stable (30-50% under load)
  ```bash
  htop
  ```

- [ ] Memory usage acceptable (<2GB for 4 workers)
  ```bash
  free -h
  watch -n 5 'free -h'
  ```

- [ ] All 4 workers running
  ```bash
  ps aux | grep gunicorn | wc -l
  # Should show 5 (1 master + 4 workers)
  ```

- [ ] Response times improved
  ```bash
  # Test response time
  time curl http://192.168.54.75/api/
  ```

### Load Testing (Optional)

```bash
cd /var/www/dcet-platform/backend
source ../venv/bin/activate

# Install locust if not present
pip install locust

# Run load test
locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5

# Monitor in browser at http://192.168.54.75:8089
```

### Check Logs

- [ ] No errors in service logs
  ```bash
  sudo journalctl -u dcet-backend --since "5 minutes ago"
  ```

- [ ] No errors in Nginx logs
  ```bash
  sudo tail -n 50 /var/log/nginx/dcet-error.log
  ```

- [ ] Access logs showing traffic
  ```bash
  sudo tail -f /var/log/nginx/dcet-access.log
  ```

## Rollback Plan (If Issues Occur)

### Quick Rollback

```bash
# 1. Restore old service file
sudo cp /var/www/dcet-platform/deploy/dcet-backend.service.backup /etc/systemd/system/dcet-backend.service

# OR manually edit to use WSGI
sudo nano /etc/systemd/system/dcet-backend.service
# Change: config.asgi:application -> config.wsgi:application

# 2. Restore old gunicorn config
cd /var/www/dcet-platform/backend
git checkout HEAD~1 -- gunicorn.conf.py

# 3. Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart dcet-backend
sudo systemctl status dcet-backend
```

### Full Rollback

```bash
# Revert to backup branch
cd /var/www/dcet-platform
git checkout backup-wsgi

# Reinstall old dependencies
cd backend
source ../venv/bin/activate
pip install --upgrade -r requirements-prod.txt

# Restart services
sudo systemctl daemon-reload
sudo systemctl restart dcet-backend
```

## Success Criteria

✅ All workers started successfully (1 master + 4 workers)  
✅ No errors in logs (journalctl, nginx)  
✅ API endpoints responding correctly  
✅ Response times < 500ms  
✅ Memory usage < 2GB  
✅ Database connections stable  
✅ Redis cache working  

## Performance Benchmarks

### Expected Improvements

| Metric | Before (WSGI) | After (ASGI) | Status |
|--------|--------------|--------------|--------|
| Workers | 2 | 4 | ✅ |
| Concurrent Requests | 2-4 | 200-400 | Test |
| Active Users | 25-40 | 150-250 | Test |
| Response Time | 800ms | 400ms | Test |
| Memory Usage | 800MB | 1-1.5GB | Monitor |

## Monitoring Commands

```bash
# Real-time worker monitoring
watch -n 2 'ps aux | grep gunicorn'

# Memory monitoring
watch -n 5 'free -h'

# Connection count
watch -n 5 'sudo netstat -an | grep :8000 | wc -l'

# Live logs
sudo journalctl -u dcet-backend -f

# Response time test
while true; do time curl -s http://localhost:8000/api/ > /dev/null; sleep 2; done
```

## Notes

- First deployment may take 30-60 seconds for workers to fully start
- Monitor logs for the first 10 minutes after deployment
- If memory usage exceeds 80%, reduce workers to 3 in `gunicorn.conf.py`
- Keep an eye on database connection count: `SHOW PROCESSLIST;` in MySQL

## Contact & Support

If issues arise:
1. Check logs: `sudo journalctl -u dcet-backend -f`
2. Run verification: `sudo ./deploy/verify_asgi.sh`
3. Review this checklist
4. Consider rollback if critical issues persist
