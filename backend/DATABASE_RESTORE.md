# Database Restore Guide

## 📦 Files Required

- `dcet_platform_full_backup.sql` - Complete database dump (schema + data)
- `requirements.txt` or `requirements-production.txt` - Python dependencies
- `.env` file - Environment variables (create from `.env.example`)

## 🚀 Quick Restore (New System)

### Step 1: Install MySQL

Ensure MySQL Server is installed and running on the target system.

### Step 2: Restore Database

**Option A: Using MySQL Command Line**

```bash
mysql -u root -p < dcet_platform_full_backup.sql
```

**Option B: Using PowerShell (Windows)**

```powershell
Get-Content dcet_platform_full_backup.sql | mysql -u root -p
```

**Option C: Using MySQL Workbench**

1. Open MySQL Workbench
2. Go to **Server** → **Data Import**
3. Select **Import from Self-Contained File**
4. Choose `dcet_platform_full_backup.sql`
5. Click **Start Import**

### Step 3: Verify Database

```sql
USE dcet_platform;
SHOW TABLES;
```

You should see all tables including:
- `users_user`
- `exams_exam`
- `exams_section`
- `exams_question`
- `results_attempt`
- `results_answer`
- And more...

### Step 4: Update Django Settings

Edit `backend/config/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "dcet_platform",
        "USER": "root",
        "PASSWORD": "your_mysql_password",  # Update this
        "HOST": "localhost",
        "PORT": "3306",
        "CONN_MAX_AGE": 600,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
            "connect_timeout": 10,
        },
    }
}
```

### Step 5: Install Python Dependencies

```bash
# For development
pip install -r requirements.txt

# For production
pip install -r requirements-production.txt
```

### Step 6: Install and Configure Redis

**Windows:**
```powershell
# Download Redis for Windows or use WSL
# Or use Docker:
docker run -d -p 6379:6379 redis:latest
```

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Mac
brew install redis
brew services start redis
```

**Verify Redis:**
```bash
redis-cli ping
# Should return: PONG
```

### Step 7: Run Django Server

```bash
# Development
python manage.py runserver

# Production (with Gunicorn)
gunicorn config.wsgi:application -c gunicorn.conf.py
```

## 🔧 Advanced Options

### Create New Backup

```bash
# Full backup (schema + data)
mysqldump -u root -p --databases dcet_platform --add-drop-database --complete-insert --routines --triggers --events | Out-File -FilePath "dcet_platform_full_backup.sql" -Encoding utf8

# Schema only (no data)
mysqldump -u root -p --no-data dcet_platform > dcet_platform_schema.sql

# Data only (no schema)
mysqldump -u root -p --no-create-info dcet_platform > dcet_platform_data.sql
```

### Restore to Different Database Name

```bash
# Edit the SQL file and replace database name
(Get-Content dcet_platform_full_backup.sql) -replace 'dcet_platform', 'new_database_name' | Set-Content new_backup.sql

# Then restore
mysql -u root -p < new_backup.sql
```

### Restore Specific Tables Only

```bash
# Extract specific table
mysqldump -u root -p dcet_platform users_user > users_table.sql

# Restore specific table
mysql -u root -p dcet_platform < users_table.sql
```

## ✅ Post-Restore Checklist

- [ ] Database restored successfully
- [ ] All tables present
- [ ] Django settings updated
- [ ] Python dependencies installed
- [ ] Redis installed and running
- [ ] `.env` file configured
- [ ] Django migrations applied (if needed): `python manage.py migrate`
- [ ] Server starts without errors
- [ ] API endpoints accessible

## 🔐 Environment Variables

Create `.env` file in `backend/` directory:

```env
# Database
DB_NAME=dcet_platform
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Redis
REDIS_URL=redis://127.0.0.1:6379/1

# Email (Brevo)
BREVO_API_KEY=your_brevo_api_key
DEFAULT_FROM_EMAIL=noreply@apollo11.com

# Django
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🐛 Troubleshooting

### "Access denied for user 'root'"
- Check MySQL password
- Verify user has permissions: `GRANT ALL PRIVILEGES ON dcet_platform.* TO 'root'@'localhost';`

### "Unknown database 'dcet_platform'"
- The backup file should create the database automatically
- If not, create manually: `CREATE DATABASE dcet_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

### "Table doesn't exist" errors
- Ensure backup was restored completely
- Check for errors during import
- Verify: `SHOW TABLES;`

### Redis connection errors
- Ensure Redis is running: `redis-cli ping`
- Check Redis URL in settings
- Verify port 6379 is not blocked

### Migration errors
- The backup includes all data, migrations should not be needed
- If Django complains, run: `python manage.py migrate --fake`

## 📊 Database Statistics

After restore, verify data:

```sql
USE dcet_platform;

-- Count users
SELECT COUNT(*) FROM users_user;

-- Count exams
SELECT COUNT(*) FROM exams_exam;

-- Count questions
SELECT COUNT(*) FROM exams_question;

-- Count attempts
SELECT COUNT(*) FROM results_attempt;
```

## 🚀 Production Deployment

For production deployment, also ensure:

1. **Nginx** configured (see `nginx.conf` in project root)
2. **Gunicorn** configured (see `gunicorn.conf.py`)
3. **SSL certificates** installed
4. **Firewall** rules configured
5. **Backup strategy** in place (automated daily backups)

## 📝 Notes

- The SQL dump includes **complete schema and all data**
- Database will be **dropped and recreated** during restore
- All **triggers, routines, and events** are included
- File size: ~64 KB (will grow with more data)
- Compatible with MySQL 5.7+ and MariaDB 10.2+
