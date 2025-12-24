# DCET Platform - Backend

Django REST Framework backend for the DCET Mock Test platform.

## 📚 Documentation

All documentation has been moved to the **[docs/](docs/)** folder.

### Quick Links

- **[Quick Setup Guide](docs/QUICK_SETUP.md)** - Get started in 10 minutes
- **[Database Restore](docs/DATABASE_RESTORE.md)** - Deploy database on new system
- **[Email Setup](docs/EMAIL_SETUP_GUIDE.md)** - Configure email service
- **[API Documentation](docs/API_DOCUMENTATION.md)** - API endpoints reference
- **[Full Documentation Index](docs/INDEX.md)** - Complete documentation list

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up database
python manage.py migrate

# 3. Run server
python manage.py runserver
```

## 📦 Project Structure

```
backend/
├── config/          # Django settings
├── users/           # User management
├── exams/           # Exam management
├── results/         # Results & analytics
├── docs/            # 📚 All documentation
├── manage.py
└── requirements.txt
```

## ✅ Features

- ✅ JWT Authentication
- ✅ Email OTP verification (Brevo)
- ✅ Redis caching (1000+ concurrent users)
- ✅ Query optimization (95% reduction)
- ✅ Exam timer system
- ✅ RESTful API

## 🔧 Configuration

See **[docs/QUICK_SETUP.md](docs/QUICK_SETUP.md)** for detailed configuration.

## 📖 More Information

Visit the **[docs/](docs/)** folder for comprehensive documentation.
