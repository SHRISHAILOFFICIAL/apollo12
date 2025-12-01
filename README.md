# 🎓 Quiz Platform - Full Stack Application

A complete online examination platform built with Django REST Framework (backend) and Next.js (frontend).

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)

---

## ✨ Features

### For Students

- ✅ User registration and authentication (JWT)
- ✅ Browse available exams
- ✅ Take exams with real-time timer
- ✅ Auto-save answers
- ✅ View exam results and history
- ✅ Track performance over time

### For Admins

- ✅ Create and manage exams
- ✅ Add questions with multiple difficulty levels
- ✅ Publish/unpublish exams
- ✅ View exam statistics
- ✅ Manage users

### Platform Features

- ✅ Multiple choice questions (MCQ)
- ✅ Auto-grading system
- ✅ Subject categorization
- ✅ Difficulty levels (Easy, Medium, Hard)
- ✅ Detailed analytics and results
- ✅ Responsive design

---

## 🛠️ Tech Stack

### Backend

- **Framework:** Django 4.2.7
- **API:** Django REST Framework
- **Database:** MySQL
- **Authentication:** JWT (djangorestframework-simplejwt)
- **CORS:** django-cors-headers
- **Language:** Python 3.12

### Frontend

- **Framework:** Next.js 16.0.3
- **Library:** React 19.2.0
- **HTTP Client:** Axios
- **Styling:** Tailwind CSS
- **Language:** TypeScript 5

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- MySQL (via XAMPP or standalone)
- Git

### Backend Setup

1. **Navigate to backend directory**

   ```powershell
   cd d:\quiz\backend
   ```

2. **Install Python dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

3. **Start MySQL server** (XAMPP or MySQL service)

4. **Configure database**

   - Database: `dcet_platform`
   - User: `root`
   - Password: `password`

5. **Run migrations**

   ```powershell
   python manage.py migrate
   ```

6. **Create sample data** (Optional but recommended)

   ```powershell
   python create_sample_data.py
   ```

7. **Start development server**

   ```powershell
   python manage.py runserver
   ```

   Backend will be available at: **http://localhost:8000**

### Frontend Setup

1. **Navigate to frontend directory**

   ```powershell
   cd d:\quiz\frontend
   ```

2. **Install dependencies**

   ```powershell
   npm install
   ```

3. **Create environment file**

   ```powershell
   # Create .env.local with:
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

4. **Start development server**

   ```powershell
   npm run dev
   ```

   Frontend will be available at: **http://localhost:3000**

---

## 📁 Project Structure

```
d:\quiz\
├── backend/                    # Django backend
│   ├── config/                 # Project settings
│   │   ├── settings.py         # Django configuration
│   │   └── urls.py             # Main URL routing
│   ├── core/                   # Core models (User, Test)
│   │   └── models.py           # User and basic models
│   ├── users/                  # User management
│   │   ├── models.py           # Extended user models
│   │   ├── serializers.py      # User serializers
│   │   ├── views.py            # User API views
│   │   └── urls.py             # User routes
│   ├── exams/                  # Exam management
│   │   ├── models.py           # Exam, Question, Option models
│   │   ├── serializers.py      # Exam serializers
│   │   ├── views.py            # Exam API views
│   │   └── urls.py             # Exam routes
│   ├── results/                # Exam attempts & results
│   │   ├── models.py           # ExamAttempt, Response models
│   │   ├── serializers.py      # Result serializers
│   │   ├── views.py            # Result API views
│   │   └── urls.py             # Result routes
│   ├── manage.py               # Django management script
│   ├── requirements.txt        # Python dependencies
│   ├── create_sample_data.py   # Sample data generator
│   └── API_DOCUMENTATION.md    # Complete API docs
│
└── frontend/                   # Next.js frontend
    ├── app/                    # Next.js app directory
    │   ├── auth/               # Authentication pages
    │   │   ├── login/          # Login page
    │   │   └── signup/         # Signup page
    │   ├── dashboard/          # Dashboard page
    │   ├── exam/               # Exam taking page
    │   │   └── [id]/           # Dynamic exam route
    │   ├── layout.tsx          # Root layout
    │   └── page.tsx            # Home page
    ├── lib/                    # Utilities and services
    │   ├── api.ts              # Axios configuration
    │   └── services/           # API services
    │       ├── auth.service.ts      # Auth operations
    │       ├── exam.service.ts      # Exam operations
    │       ├── attempt.service.ts   # Attempt operations
    │       └── notification.service.ts
    ├── package.json            # Node dependencies
    ├── next.config.ts          # Next.js configuration
    ├── tailwind.config.ts      # Tailwind configuration
    └── INTEGRATION_GUIDE.md    # Frontend integration docs
```

---

## 🔐 Test Credentials

### Student Account

```
Username: student
Password: student123
Email: student@quiz.com
```

### Admin Account

```
Username: admin
Password: admin123
Email: admin@quiz.com
```

### Superuser Account

```
Username: shri
Email: shrishailkone.21@gmail.com
```

---

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api
```

### Authentication Endpoints

| Method | Endpoint           | Description            |
| ------ | ------------------ | ---------------------- |
| POST   | `/users/register/` | Register new user      |
| POST   | `/users/login/`    | Login with credentials |
| POST   | `/token/refresh/`  | Refresh JWT token      |
| GET    | `/users/profile/`  | Get user profile       |

### Exam Endpoints

| Method | Endpoint                 | Description         |
| ------ | ------------------------ | ------------------- |
| GET    | `/exams/`                | List all exams      |
| GET    | `/exams/{id}/`           | Get exam details    |
| GET    | `/exams/{id}/take_exam/` | Get exam for taking |
| GET    | `/subjects/`             | List subjects       |

### Attempt Endpoints

| Method | Endpoint                      | Description        |
| ------ | ----------------------------- | ------------------ |
| POST   | `/attempts/start_exam/`       | Start exam attempt |
| POST   | `/attempts/submit_answer/`    | Submit answer      |
| POST   | `/attempts/{id}/submit_exam/` | Submit exam        |
| GET    | `/attempts/{id}/result/`      | Get result         |
| GET    | `/attempts/my_attempts/`      | My attempts        |

**Complete documentation:** `backend/API_DOCUMENTATION.md`

---

## 🧪 Testing

### Backend Tests

```powershell
cd d:\quiz\backend
python test_complete_flow.py
```

### Test Sample Data

```powershell
python create_sample_data.py
```

This creates:

- 2 users (admin and student)
- 5 subjects
- 2 exams (Math and Physics)
- 8 questions with options

---

## 🎯 Key Features Implementation

### Authentication Flow

1. User registers/logs in
2. Backend returns JWT access & refresh tokens
3. Frontend stores tokens in localStorage
4. All API requests include token in Authorization header
5. Automatic token refresh on 401 errors

### Exam Taking Flow

1. Student starts exam → Creates ExamAttempt
2. Fetches questions (without correct answers)
3. Timer starts counting down
4. Each answer auto-saves to backend
5. On submit → Calculates score
6. Shows detailed results

### Security Features

- ✅ JWT authentication
- ✅ Password hashing
- ✅ CORS protection
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection
- ✅ CSRF protection

---

## 📊 Database Schema

### Core Tables

- `core_user` - User accounts
- `subjects` - Subject categories
- `exams` - Exam metadata
- `questions` - Exam questions
- `options` - Question options
- `exam_attempts` - Student attempts
- `attempt_responses` - Individual answers

**Total Tables:** 26 (including Django's built-in tables)

---

## 🚢 Deployment Checklist

### Backend

- [ ] Update `ALLOWED_HOSTS` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up static files serving
- [ ] Configure CORS for production domain
- [ ] Set environment variables
- [ ] Run `python manage.py collectstatic`
- [ ] Set up Gunicorn/uWSGI
- [ ] Configure Nginx/Apache

### Frontend

- [ ] Update API URL in `.env.production`
- [ ] Build production bundle: `npm run build`
- [ ] Configure environment variables
- [ ] Set up hosting (Vercel recommended)
- [ ] Configure custom domain
- [ ] Enable HTTPS

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is developed for educational purposes.

---

## 🆘 Troubleshooting

### Backend Issues

**MySQL Connection Error**

```powershell
# Start XAMPP MySQL or run:
net start MySQL
```

**Port 8000 Already in Use**

```powershell
# Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Migration Errors**

```powershell
# Reset migrations
python manage.py migrate --fake
python manage.py migrate --fake-initial
```

### Frontend Issues

**Module Not Found**

```powershell
# Reinstall dependencies
rm -rf node_modules
npm install
```

**API Connection Refused**

- Ensure backend is running on port 8000
- Check `.env.local` has correct API URL
- Verify CORS configuration

---

## 📞 Support

For issues or questions:

- Check `backend/API_DOCUMENTATION.md`
- Check `frontend/INTEGRATION_GUIDE.md`
- Review `PROJECT_SETUP_COMPLETE.md`

---

## 🎉 Project Status

**Status:** ✅ Fully Functional

### Completed

- ✅ Backend API (100%)
- ✅ Frontend Integration (95%)
- ✅ Authentication System (100%)
- ✅ Exam Management (100%)
- ✅ Exam Taking (100%)
- ✅ Results System (100%)

### In Progress

- ⏳ Admin Dashboard UI
- ⏳ Analytics Dashboard
- ⏳ Payment Integration

### Planned

- 📋 Email Notifications
- 📋 PDF Result Export
- 📋 Mobile App

---

**Built with ❤️ by Your Team**

Last Updated: December 2025
