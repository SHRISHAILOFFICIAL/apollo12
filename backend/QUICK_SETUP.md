# Quick Setup Guide for New System

This guide will help you set up the Apollo11 backend on a new system in minutes.

## 📋 Prerequisites

- MySQL Server 5.7+ or MariaDB 10.2+
- Python 3.9+
- Redis Server
- Git (optional)

## 🚀 Setup Steps

### 1. Clone/Copy Project Files

Copy the entire `backend` folder to your new system.

### 2. Install Python Dependencies

```bash
cd backend

# For development
pip install -r requirements.txt

# For production
pip install -r requirements-production.txt
```

### 3. Restore Database

**Option A: Command Line (Recommended)**

```bash
mysql -u root -p < dcet_platform_full_backup.sql
```

**Option B: PowerShell (Windows)**

```powershell
Get-Content dcet_platform_full_backup.sql | mysql -u root -p
```

Enter your MySQL password when prompted.

### 4. Update Database Configuration

Edit `config/settings.py` and update the database password:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "dcet_platform",
        "USER": "root",
        "PASSWORD": "your_mysql_password_here",  # ← Update this
        "HOST": "localhost",
        "PORT": "3306",
        # ... rest of config
    }
}
```

### 5. Start Redis Server

**Windows:**
```powershell
# If using WSL
wsl redis-server

# Or using Docker
docker run -d -p 6379:6379 redis:latest
```

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo systemctl start redis

# Mac
brew services start redis
```

**Verify Redis:**
```bash
redis-cli ping
# Should return: PONG
```

### 6. Test Database Connection

```bash
python manage.py check --database default
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

### 8. (Production) Run with Gunicorn

```bash
gunicorn config.wsgi:application -c gunicorn.conf.py
```

## ✅ Verification

Test the API endpoints:

```bash
# Health check
curl http://localhost:8000/api/

# Login test
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"demo5@gmail.com","password":"password"}'
```

## 📊 Database Contents

After restoration, your database will have:

- **Users:** 5 test users (demo2@gmail.com to demo5@gmail.com, test@example.com)
- **Exams:** 1 exam (DCET 2023)
- **Sections:** 5 sections (IT Skills, Engineering Math, etc.)
- **Questions:** 100 questions across all sections
- **Attempts:** Sample exam attempts with answers

**Test Login Credentials:**
- Email: `demo5@gmail.com`
- Password: `password` (default for all demo users)

## 🔧 Configuration Files

### Environment Variables (Optional)

Create `.env` file in `backend/` directory:

```env
DB_NAME=dcet_platform
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

REDIS_URL=redis://127.0.0.1:6379/1

BREVO_API_KEY=your_brevo_api_key
DEFAULT_FROM_EMAIL=noreply@apollo11.com

SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🐛 Common Issues

### "Access denied for user 'root'"
- Check MySQL password in `settings.py`
- Ensure MySQL server is running

### "Unknown database 'dcet_platform'"
- The SQL file should create the database automatically
- If not, run: `CREATE DATABASE dcet_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

### "Redis connection refused"
- Ensure Redis is running: `redis-cli ping`
- Check Redis URL in `settings.py`

### "No module named 'mysqlclient'"
- Install: `pip install mysqlclient`
- On Windows, you may need Visual C++ Build Tools

## 📚 Additional Documentation

- **[DATABASE_RESTORE.md](DATABASE_RESTORE.md)** - Detailed restoration guide
- **[README.md](README.md)** - Full backend documentation
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - API endpoints
- **[QUERY_OPTIMIZATION.md](QUERY_OPTIMIZATION.md)** - Performance optimizations

## 🎯 Next Steps

1. ✅ Database restored
2. ✅ Server running
3. 🔄 Configure frontend to connect to backend
4. 🔄 Set up Nginx (for production)
5. 🔄 Configure SSL certificates (for production)
6. 🔄 Set up automated backups

## 📞 Support

For detailed information, refer to the comprehensive documentation files in the `backend/` directory.

---

**Setup Time:** ~10 minutes  
**Difficulty:** Easy  
**Status:** Production Ready ✅
