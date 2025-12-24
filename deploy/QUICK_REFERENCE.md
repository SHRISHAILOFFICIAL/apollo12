# DCET Platform - Production Deployment Quick Reference

## 🚀 Quick Start

### On Your Ubuntu VM (192.168.54.75)

```bash
# 1. Clone from GitHub (run once)
ssh user@192.168.1.18
cd /var/www
sudo git clone https://github.com/YOUR_USERNAME/apollo12.git dcet-platform
sudo chown -R $USER:$USER dcet-platform

# 2. Initial setup
cd dcet-platform
chmod +x deploy/*.sh
sudo ./deploy/setup_server.sh

# 3. Configure database
sudo mysql -u root -p
CREATE DATABASE dcet_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dcet_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON dcet_platform.* TO 'dcet_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 4. Configure environment
cd backend
cp .env.example .env
nano .env  # Update SECRET_KEY, DB_PASSWORD, API keys

# 5. Deploy
cd ..
sudo ./deploy/deploy.sh

# 5. Create admin user
cd backend
source ../venv/bin/activate
python manage.py createsuperuser
```

## 📋 Essential Commands

### Service Management
```bash
# Restart backend
sudo systemctl restart dcet-backend

# Restart nginx
sudo systemctl restart nginx

# Check status
sudo systemctl status dcet-backend
sudo systemctl status nginx
```

### View Logs
```bash
# Backend logs
sudo journalctl -u dcet-backend -f

# Nginx logs
sudo tail -f /var/log/nginx/dcet-error.log
```

### Update Application
```bash
# After pushing to GitHub
cd /var/www/dcet-platform
git pull origin main
sudo ./deploy/deploy.sh
```

## 🔧 File Structure

```
/var/www/dcet-platform/
├── backend/
│   ├── .env                    # Environment variables (create from .env.example)
│   ├── config/settings.py      # Django settings
│   ├── gunicorn.conf.py        # Gunicorn configuration
│   ├── requirements-prod.txt   # Python dependencies
│   ├── staticfiles/            # Collected static files
│   └── media/                  # User uploads
├── frontend/
│   ├── .env.production         # Frontend environment
│   ├── out/                    # Built static files
│   └── package.json
├── deploy/
│   ├── setup_server.sh         # Initial server setup
│   ├── deploy.sh               # Deployment script
│   └── dcet-backend.service    # Systemd service
├── nginx.conf                  # Nginx configuration
├── DEPLOYMENT.md               # Full deployment guide
└── ENV_VARIABLES.md            # Environment variables docs
```

## 🌐 Access Points

- **Frontend**: http://192.168.1.18
- **Admin Panel**: http://192.168.1.18/admin/
- **API**: http://192.168.1.18/api/
- **Health Check**: http://192.168.1.18/health

## ⚙️ Configuration Files

### Backend (.env)
```bash
SECRET_KEY=<generate-new-key>
DEBUG=False
ALLOWED_HOSTS=192.168.1.18,localhost,127.0.0.1
DB_USER=dcet_user
DB_PASSWORD=<your-password>
CORS_ALLOWED_ORIGINS=http://192.168.1.18
```

### Frontend (.env.production)
```bash
NEXT_PUBLIC_API_URL=http://192.168.1.18/api
NEXT_PUBLIC_DEBUG=false
```

## 🔒 Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] Strong database password
- [ ] Firewall enabled (UFW)
- [ ] Services run as `www-data`
- [ ] `.env` files not in git

## 🐛 Common Issues

### 502 Bad Gateway
```bash
# Check if backend is running
sudo systemctl status dcet-backend
sudo systemctl restart dcet-backend
```

### Static files not loading
```bash
cd /var/www/dcet-platform/backend
source ../venv/bin/activate
python manage.py collectstatic --clear --noinput
sudo chown -R www-data:www-data staticfiles/
```

### Database connection error
```bash
# Test connection
mysql -u dcet_user -p dcet_platform

# Check .env file
cat /var/www/dcet-platform/backend/.env
```

## 📚 Documentation

- **Full Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Environment Variables**: [ENV_VARIABLES.md](./ENV_VARIABLES.md)
- **Backend Schema**: [backend_schema.md](./backend_schema.md)

## 🎯 Next Steps (Real VPS)

1. Get domain name
2. Update DNS A record
3. Update `.env` files with domain
4. Install SSL: `sudo certbot --nginx -d yourdomain.com`
5. Redeploy: `sudo ./deploy/deploy.sh`
