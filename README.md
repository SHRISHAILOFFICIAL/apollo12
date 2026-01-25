# DCET Mock Test Platform

A comprehensive EdTech platform for DCET exam preparation with mock tests, previous year questions, and detailed analytics.

## Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript, TailwindCSS
- **Backend**: Django 5.2, Django REST Framework
- **Database**: MySQL
- **Cache**: Redis
- **Payment**: Razorpay
- **Email**: Brevo (Anymail)
- **Server**: Nginx + Gunicorn + Uvicorn (ASGI)

## Features

- 🎯 Mock Tests & Previous Year Questions
- 📊 Detailed Performance Analytics
- 💳 Payment Integration (FREE & PRO tiers)
- 📧 Email Notifications (OTP, Results)
- 🔐 JWT Authentication
- ⚡ Redis Caching for Performance
- 📱 Responsive Design
- 🎨 LaTeX Math Rendering

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your environment
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Production Deployment

**For Ubuntu Server/VPS deployment**, see:

- 📖 **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Complete deployment guide
- ⚡ **[deploy/QUICK_REFERENCE.md](./deploy/QUICK_REFERENCE.md)** - Quick reference
- 🔧 **[ENV_VARIABLES.md](./ENV_VARIABLES.md)** - Environment variables documentation

### Quick Deploy (Ubuntu VM)

```bash
# 1. Run initial setup
sudo ./deploy/setup_server.sh

# 2. Configure .env files
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials

# 3. Deploy
sudo ./deploy/deploy.sh

# Access at: http://192.168.54.75
```

## Project Structure

```
apollo12/
├── backend/          # Django REST API
├── frontend/         # Next.js application
├── deploy/           # Deployment scripts & configs
├── docs/             # Documentation
├── nginx.conf        # Nginx configuration
└── DEPLOYMENT.md     # Deployment guide
```

## Documentation

- [Backend Schema](./backend_schema.md)
- [Database Documentation](./backend/DATABASE_DOCUMENTATION.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Environment Variables](./ENV_VARIABLES.md)

## License

Private - All Rights Reserved
