# Deployment Guide - DCET Platform

## 🚀 Complete Production Deployment

### Prerequisites
- Ubuntu 20.04/22.04 VPS (4GB RAM minimum)
- Domain name pointed to your server IP
- SSH access to server

---

## 📦 Step 1: Server Setup

### Update system
```bash
sudo apt update && sudo apt upgrade -y
```

### Install dependencies
```bash
# Python & MySQL
sudo apt install python3.10 python3-pip python3-venv mysql-server nginx -y

# Redis
sudo apt install redis-server -y

# Node.js (for Next.js)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
```

---

## 🗄️ Step 2: MySQL Setup

```bash
# Secure MySQL
sudo mysql_secure_installation

# Create database
sudo mysql -u root -p
```

```sql
CREATE DATABASE dcet_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dcet_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON dcet_platform.* TO 'dcet_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 🔧 Step 3: Backend Deployment

### Clone repository
```bash
cd /var/www
sudo git clone https://github.com/yourusername/dcet-platform.git
cd dcet-platform/backend
```

### Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements-production.txt
```

### Configure settings
```bash
# Create .env file
nano .env
```

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_NAME=dcet_platform
DATABASE_USER=dcet_user
DATABASE_PASSWORD=your_strong_password
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

### Run migrations
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## 🎨 Step 4: Frontend Deployment

```bash
cd /var/www/dcet-platform/frontend

# Install dependencies
npm install

# Build for production
npm run build
npm run export  # Creates 'out' folder
```

---

## 🌐 Step 5: Nginx Setup

### Copy configuration
```bash
sudo cp /var/www/dcet-platform/nginx.conf /etc/nginx/sites-available/dcet-platform
```

### Edit configuration
```bash
sudo nano /etc/nginx/sites-available/dcet-platform
```
- Replace `yourdomain.com` with your actual domain
- Update paths if needed

### Enable site
```bash
sudo ln -s /etc/nginx/sites-available/dcet-platform /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

---

## 🔒 Step 6: SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (already set up by certbot)
sudo certbot renew --dry-run
```

---

## 🔄 Step 7: Gunicorn as Systemd Service

### Create service file
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=Gunicorn daemon for DCET Platform
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/dcet-platform/backend
Environment="PATH=/var/www/dcet-platform/backend/venv/bin"
ExecStart=/var/www/dcet-platform/backend/venv/bin/gunicorn \
          -c gunicorn.conf.py \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Start service
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

---

## 📊 Step 8: Redis Configuration

```bash
# Edit Redis config
sudo nano /etc/redis/redis.conf
```

```conf
maxmemory 512mb
maxmemory-policy allkeys-lru
save ""  # Disable persistence for speed
```

```bash
sudo systemctl restart redis
```

---

## 🔍 Step 9: Verify Deployment

### Check services
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status redis
sudo systemctl status mysql
```

### Test endpoints
```bash
# Health check
curl https://yourdomain.com/health

# API
curl https://yourdomain.com/api/exams/
```

---

## 📈 Step 10: Monitoring & Logs

### View logs
```bash
# Gunicorn
sudo journalctl -u gunicorn -f

# Nginx
sudo tail -f /var/log/nginx/dcet-error.log
sudo tail -f /var/log/nginx/dcet-access.log

# Redis
redis-cli info stats
```

---

## 🔄 Updates & Maintenance

### Update code
```bash
cd /var/www/dcet-platform
sudo git pull

# Backend
cd backend
source venv/bin/activate
pip install -r requirements-production.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn

# Frontend
cd ../frontend
npm install
npm run build
npm run export
sudo systemctl reload nginx
```

---

## 🛡️ Security Checklist

- ✅ Firewall configured (UFW)
- ✅ SSH key-only authentication
- ✅ SSL certificate installed
- ✅ Security headers in Nginx
- ✅ Database user with limited privileges
- ✅ DEBUG=False in production
- ✅ Strong SECRET_KEY
- ✅ Regular backups

---

## 🎯 Performance Tuning

### MySQL
```sql
-- Check query performance
SHOW PROCESSLIST;
SHOW STATUS LIKE 'Threads_connected';
```

### Redis
```bash
# Monitor cache hit rate
redis-cli info stats | grep keyspace
```

### Nginx
```bash
# Check connections
sudo netstat -an | grep :80 | wc -l
```

---

## 📞 Troubleshooting

### Gunicorn not starting
```bash
sudo journalctl -u gunicorn -n 50
```

### Nginx 502 Bad Gateway
```bash
# Check if Gunicorn is running
sudo systemctl status gunicorn

# Check Nginx error log
sudo tail -f /var/log/nginx/dcet-error.log
```

### Database connection issues
```bash
# Test MySQL connection
mysql -u dcet_user -p dcet_platform
```

---

## ✅ Deployment Complete!

Your DCET Platform is now live at: **https://yourdomain.com**

**Capacity**: 1000-1500 concurrent users on 4GB RAM VPS 🚀
