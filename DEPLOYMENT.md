# DCET Platform - Production Deployment Guide

Complete guide for deploying the DCET Platform on Ubuntu server (VM or VPS).

## Prerequisites

- Ubuntu 20.04 or later
- Root or sudo access
- VM/Server IP: `192.168.1.18`
- Minimum 2GB RAM, 2 CPU cores

---

## Initial Server Setup

### 1. Clone Repository from GitHub

First, push your `apollo12` code to GitHub (if not already done):

```bash
# On your local machine (Windows)
cd e:\apollo12\apollo12
git init
git add .
git commit -m "Initial commit - production ready"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/apollo12.git
git push -u origin main
```

Then, on your Ubuntu VM:

```bash
# SSH into the server
ssh user@192.168.1.18

# Install git if not already installed
sudo apt update
sudo apt install -y git

# Clone repository to /var/www
sudo mkdir -p /var/www
cd /var/www
sudo git clone https://github.com/YOUR_USERNAME/apollo12.git dcet-platform

# Set ownership
sudo chown -R $USER:$USER dcet-platform

# Run setup script
cd dcet-platform
chmod +x deploy/setup_server.sh
sudo ./deploy/setup_server.sh
```

This installs:
- Python 3, pip, venv
- MySQL server
- Redis server
- Nginx web server
- Node.js 20.x
- Configures firewall (UFW)

### 2. Configure MySQL Database

```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p

# In MySQL shell:
CREATE DATABASE dcet_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dcet_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON dcet_platform.* TO 'dcet_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Configure Environment Variables

```bash
cd /var/www/dcet-platform/backend

# Copy example to .env
cp .env.example .env

# Edit .env file
nano .env
```

**Update these values in `.env`:**

```bash
# Generate a new secret key
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Set to False for production
DEBUG=False

# Already configured
ALLOWED_HOSTS=192.168.1.18,localhost,127.0.0.1

# Update database credentials
DB_USER=dcet_user
DB_PASSWORD=your_strong_password

# Add your API keys
BREVO_API_KEY=your_actual_brevo_key
RAZORPAY_KEY_ID=your_actual_razorpay_key_id
RAZORPAY_KEY_SECRET=your_actual_razorpay_key_secret
RAZORPAY_WEBHOOK_SECRET=your_actual_webhook_secret
```

---

## Deployment

### Run the Deployment Script

```bash
cd /var/www/dcet-platform
chmod +x deploy/deploy.sh
sudo ./deploy/deploy.sh
```

This script will:
1. Install Python dependencies
2. Run database migrations
3. Collect Django static files
4. Build Next.js frontend
5. Configure Nginx
6. Set up systemd service
7. Start all services

---

## Service Management

### Check Service Status

```bash
# Check backend service
sudo systemctl status dcet-backend

# Check Nginx
sudo systemctl status nginx

# Check Redis
sudo systemctl status redis
```

### Restart Services

```bash
# Restart backend
sudo systemctl restart dcet-backend

# Restart Nginx
sudo systemctl restart nginx
```

### View Logs

```bash
# Backend logs
sudo journalctl -u dcet-backend -f

# Nginx access logs
sudo tail -f /var/log/nginx/dcet-access.log

# Nginx error logs
sudo tail -f /var/log/nginx/dcet-error.log
```

---

## Testing the Deployment

### 1. Test Backend API

```bash
# Health check
curl http://192.168.1.18/health

# API endpoint
curl http://192.168.1.18/api/
```

### 2. Test Frontend

Open browser and navigate to:
```
http://192.168.1.18
```

### 3. Test Admin Panel

```bash
# Create superuser
cd /var/www/dcet-platform/backend
source ../venv/bin/activate
python manage.py createsuperuser
```

Access admin at: `http://192.168.1.18/admin/`

---

## Troubleshooting

### Backend Not Starting

```bash
# Check logs
sudo journalctl -u dcet-backend -n 50

# Test Gunicorn manually
cd /var/www/dcet-platform/backend
source ../venv/bin/activate
gunicorn -c gunicorn.conf.py config.wsgi:application
```

### Nginx 502 Bad Gateway

```bash
# Check if backend is running
sudo systemctl status dcet-backend

# Check Nginx error logs
sudo tail -f /var/log/nginx/dcet-error.log

# Test Nginx config
sudo nginx -t
```

### Database Connection Issues

```bash
# Test MySQL connection
mysql -u dcet_user -p dcet_platform

# Check Django database settings
cd /var/www/dcet-platform/backend
source ../venv/bin/activate
python manage.py check --database default
```

### Static Files Not Loading

```bash
# Recollect static files
cd /var/www/dcet-platform/backend
source ../venv/bin/activate
python manage.py collectstatic --clear --noinput

# Check permissions
ls -la staticfiles/
sudo chown -R www-data:www-data staticfiles/
```

---

## Updating the Application

After pushing changes to GitHub:

```bash
# On Ubuntu VM
cd /var/www/dcet-platform

# Pull latest code from GitHub
git pull origin main

# Run deployment script
sudo ./deploy/deploy.sh
```

**Workflow:**
1. Make changes locally in `apollo12`
2. Commit and push to GitHub: `git push origin main`
3. SSH to VM and pull changes: `git pull origin main`
4. Run deployment script: `sudo ./deploy/deploy.sh`

---

## Security Checklist

- [x] `DEBUG=False` in production
- [x] Strong `SECRET_KEY` generated
- [x] Database credentials secured
- [x] Firewall configured (UFW)
- [x] Services run as `www-data` user
- [ ] Regular backups configured
- [ ] SSL/HTTPS (when domain available)
- [ ] Fail2ban installed (optional)

---

## Next Steps (When Moving to Real VPS)

1. **Get a domain name**
2. **Point DNS to VPS IP**
3. **Update configuration:**
   ```bash
   # Update .env
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   CORS_ALLOWED_ORIGINS=https://yourdomain.com
   
   # Update frontend/.env.production
   NEXT_PUBLIC_API_URL=https://yourdomain.com/api
   ```
4. **Install SSL certificate:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```
5. **Redeploy:**
   ```bash
   sudo ./deploy/deploy.sh
   ```

---

## Support

For issues, check:
- Backend logs: `sudo journalctl -u dcet-backend -f`
- Nginx logs: `/var/log/nginx/dcet-error.log`
- Django check: `python manage.py check --deploy`
