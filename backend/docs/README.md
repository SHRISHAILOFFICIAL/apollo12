# DCET Platform - Backend Setup Guide

## 🆕 NEW: Redis Exam Timer System

**Production-ready server-enforced exam timers with automatic expiration!**

✅ Redis stores countdown timers with TTL (auto-delete on expiration)  
✅ MySQL stores all permanent exam data  
✅ Automatic timeout detection and enforcement  
✅ Resume functionality for interrupted exams

📚 **Complete Documentation:**

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - ⭐ Start here for setup
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - What was built
- **[REDIS_QUICK_REFERENCE.md](REDIS_QUICK_REFERENCE.md)** - Quick reference
- **[REDIS_TIMER_DOCUMENTATION.md](REDIS_TIMER_DOCUMENTATION.md)** - Full docs
- **[INSTALL_REDIS.md](INSTALL_REDIS.md)** - Redis installation

---

## Project Structure

```
backend/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings (MySQL, REST, JWT)
│   ├── urls.py            # Project URLs
│   └── wsgi.py
├── core/                  # Core app with custom User model
├── api/                   # API endpoints
├── users/                 # User management app
├── exams/                 # Exam management app
├── results/               # Results management app
├── payments/              # Payments processing app
├── analytics/             # Analytics and reporting app
├── adminpanel/            # Admin panel functionality app
├── manage.py
├── requirements.txt
└── setup_database.py      # Database setup helper script
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**

- Django
- djangorestframework
- djangorestframework-simplejwt
- mysqlclient
- django-cors-headers
- pandas
- **django-redis** ⭐ NEW
- **redis** ⭐ NEW

### 2. Database Setup (MySQL)

**Option A: Using the setup script**

```bash
python setup_database.py
```

**Option B: Manual MySQL setup**

```sql
CREATE DATABASE dcet_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Database Configuration:**

- Database Name: `dcet_platform`
- User: `root`
- Password: (update in `config/settings.py`)
- Host: `localhost`
- Port: `3306`

### 3. Update Settings

Edit `backend/config/settings.py` and update the MySQL password:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "dcet_platform",
        "USER": "root",
        "PASSWORD": "your_mysql_password_here",  # Update this
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000`

## Configuration Details

### Installed Apps

- **Django Built-in:**

  - django.contrib.admin
  - django.contrib.auth
  - django.contrib.contenttypes
  - django.contrib.sessions
  - django.contrib.messages
  - django.contrib.staticfiles

- **Third-party:**

  - rest_framework
  - rest_framework_simplejwt
  - corsheaders

- **Custom Apps:**
  - core (Custom User model)
  - api (API endpoints)
  - users (User management)
  - exams (Exam management)
  - results (Results tracking)
  - payments (Payment processing)
  - analytics (Analytics & reporting)
  - adminpanel (Admin functionality)

### Middleware

```python
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS support
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

### REST Framework & JWT Configuration

**REST Framework:**

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}
```

**Simple JWT Settings:**

- Access Token Lifetime: 60 minutes
- Refresh Token Lifetime: 7 days
- Algorithm: HS256
- Auth Header Type: Bearer

### CORS Configuration

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Frontend Next.js app
]
```

## Custom User Model

The project uses a custom user model defined in the `core` app:

```python
AUTH_USER_MODEL = "core.User"
```

## Development Tips

1. **Switch to SQLite for development** (if MySQL not available):

   - Uncomment the SQLite configuration in `settings.py`
   - Comment out the MySQL configuration

2. **Check database connection:**

   ```bash
   python manage.py check --database default
   ```

3. **View all migrations:**

   ```bash
   python manage.py showmigrations
   ```

4. **Create migrations for specific app:**
   ```bash
   python manage.py makemigrations app_name
   ```

## Next Steps

1. Define models in each app (`models.py`)
2. Create serializers for API endpoints (`serializers.py`)
3. Implement views for business logic (`views.py`)
4. Configure URL routing (`urls.py`)
5. Set up admin interface (`admin.py`)
6. Write tests (`tests.py`)

## API Endpoints

After implementation, your API endpoints will be available at:

- `/api/auth/` - Authentication endpoints
- `/api/users/` - User management
- `/api/exams/` - Exam operations
- `/api/results/` - Results management
- `/api/payments/` - Payment processing
- `/api/analytics/` - Analytics data
- `/api/admin/` - Admin operations

## Troubleshooting

### MySQL Connection Issues

- Ensure MySQL server is running
- Check credentials in `settings.py`
- Verify database exists: `SHOW DATABASES;`

### mysqlclient Installation Issues (Windows)

- Download unofficial Windows binaries if needed
- Or use alternative: `pip install pymysql` and add to `settings.py`:
  ```python
  import pymysql
  pymysql.install_as_MySQLdb()
  ```

### Migration Errors

- Reset migrations: `python manage.py migrate --fake-initial`
- Clear migration files and recreate
- Check database exists and is accessible

## Support

For issues or questions, refer to:

- Django documentation: https://docs.djangoproject.com/
- DRF documentation: https://www.django-rest-framework.org/
- Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/
