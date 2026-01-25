#!/bin/bash
# ASGI/Uvicorn Deployment Verification Script
# Run this after deployment to verify everything is configured correctly

set -e

echo "========================================"
echo "DCET Platform - ASGI Verification"
echo "========================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_DIR="/var/www/dcet-platform"
BACKEND_DIR="$PROJECT_DIR/backend"
VENV_DIR="$PROJECT_DIR/venv"

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

# 1. Check Uvicorn installation
echo "1. Checking Uvicorn installation..."
cd $BACKEND_DIR
source $VENV_DIR/bin/activate

if python -c "import uvicorn" 2>/dev/null; then
    VERSION=$(python -c "import uvicorn; print(uvicorn.__version__)")
    print_status 0 "Uvicorn installed (version: $VERSION)"
else
    print_status 1 "Uvicorn NOT installed"
    exit 1
fi

# 2. Check uvloop (performance optimization)
if python -c "import uvloop" 2>/dev/null; then
    print_status 0 "uvloop installed (async event loop)"
else
    print_status 1 "uvloop NOT installed (run: pip install uvicorn[standard])"
fi

# 3. Check httptools (performance optimization)
if python -c "import httptools" 2>/dev/null; then
    print_status 0 "httptools installed (HTTP parser)"
else
    print_status 1 "httptools NOT installed"
fi

echo ""

# 4. Verify ASGI application
echo "2. Verifying ASGI application..."
if python -c "from config.asgi import application; assert application is not None" 2>/dev/null; then
    APP_TYPE=$(python -c "from config.asgi import application; print(type(application).__name__)")
    print_status 0 "ASGI application found (type: $APP_TYPE)"
else
    print_status 1 "ASGI application FAILED to load"
    exit 1
fi

echo ""

# 5. Check Gunicorn configuration
echo "3. Checking Gunicorn configuration..."
if [ -f "$BACKEND_DIR/gunicorn.conf.py" ]; then
    print_status 0 "gunicorn.conf.py exists"
    
    # Check worker class
    if grep -q "uvicorn.workers.UvicornWorker" "$BACKEND_DIR/gunicorn.conf.py"; then
        print_status 0 "Worker class: UvicornWorker"
    else
        print_status 1 "Worker class NOT set to UvicornWorker"
    fi
    
    # Check workers count
    WORKERS=$(grep "^workers = " "$BACKEND_DIR/gunicorn.conf.py" | awk '{print $3}')
    print_status 0 "Workers configured: $WORKERS"
else
    print_status 1 "gunicorn.conf.py NOT found"
fi

echo ""

# 6. Check systemd service
echo "4. Checking systemd service..."
if [ -f "/etc/systemd/system/dcet-backend.service" ]; then
    print_status 0 "dcet-backend.service exists"
    
    # Check if using ASGI
    if grep -q "config.asgi:application" "/etc/systemd/system/dcet-backend.service"; then
        print_status 0 "Service configured for ASGI"
    else
        print_status 1 "Service NOT configured for ASGI (using WSGI)"
    fi
else
    print_status 1 "dcet-backend.service NOT found"
fi

echo ""

# 7. Check service status
echo "5. Checking service status..."
if systemctl is-active --quiet dcet-backend; then
    print_status 0 "dcet-backend service is RUNNING"
    
    # Count worker processes
    WORKER_COUNT=$(ps aux | grep "gunicorn" | grep -v grep | wc -l)
    print_status 0 "Active worker processes: $WORKER_COUNT"
    
    # Show worker details
    echo -e "${YELLOW}Worker processes:${NC}"
    ps aux | grep "gunicorn" | grep -v grep | awk '{print "  PID: " $2 " | CPU: " $3 "% | MEM: " $4 "% | " $11 " " $12 " " $13}'
else
    print_status 1 "dcet-backend service is NOT running"
    echo "Start with: sudo systemctl start dcet-backend"
fi

echo ""

# 8. Test configuration
echo "6. Testing Gunicorn configuration..."
if gunicorn --check-config -c gunicorn.conf.py config.asgi:application; then
    print_status 0 "Gunicorn configuration is VALID"
else
    print_status 1 "Gunicorn configuration has ERRORS"
fi

echo ""

# 9. Check database connection
echo "7. Checking database connection..."
if python manage.py check --database default 2>/dev/null; then
    print_status 0 "Database connection OK"
else
    print_status 1 "Database connection FAILED"
fi

echo ""

# 10. Check Redis connection
echo "8. Checking Redis connection..."
if python -c "from django.core.cache import cache; cache.set('test', 'ok'); assert cache.get('test') == 'ok'" 2>/dev/null; then
    print_status 0 "Redis cache connection OK"
else
    print_status 1 "Redis cache connection FAILED"
fi

echo ""

# 11. Memory usage
echo "9. Checking resource usage..."
TOTAL_MEM=$(free -m | awk 'NR==2{print $2}')
USED_MEM=$(free -m | awk 'NR==2{print $3}')
MEM_PERCENT=$((USED_MEM * 100 / TOTAL_MEM))

echo -e "Memory: ${USED_MEM}MB / ${TOTAL_MEM}MB (${MEM_PERCENT}%)"

if [ $MEM_PERCENT -gt 80 ]; then
    echo -e "${RED}Warning: High memory usage!${NC}"
else
    print_status 0 "Memory usage normal"
fi

echo ""

# 12. Port check
echo "10. Checking port availability..."
if netstat -tuln | grep -q ":8000"; then
    print_status 0 "Port 8000 is LISTENING"
else
    print_status 1 "Port 8000 NOT listening"
fi

echo ""
echo "========================================"
echo "Verification Complete!"
echo "========================================"

# Summary
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Monitor logs: sudo journalctl -u dcet-backend -f"
echo "2. Test API: curl http://localhost:8000/api/"
echo "3. Check performance: ps aux | grep gunicorn"
echo "4. Monitor connections: sudo netstat -an | grep :8000 | wc -l"
echo ""
