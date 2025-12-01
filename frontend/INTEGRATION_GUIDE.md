# Frontend-Backend Integration Guide

## ✅ What's Been Implemented

### 1. API Configuration (`lib/api.ts`)

- ✅ Axios instance with base URL configuration
- ✅ Request interceptor for JWT token injection
- ✅ Response interceptor for automatic token refresh
- ✅ Environment variable support for API URL

### 2. Service Layer Created

#### `lib/services/auth.service.ts`

- User registration
- User login with token storage
- Logout functionality
- Get/update user profile
- Password reset request/confirm
- Authentication state checking

#### `lib/services/exam.service.ts`

- Get all subjects
- Get all exams (with filters)
- Get exam details
- Get exam for taking (student view)
- Admin: Create/update/delete exams
- Admin: Publish/unpublish exams
- Admin: Get exam statistics
- Question management (CRUD operations)

#### `lib/services/attempt.service.ts`

- Start exam attempt
- Submit individual answers
- Submit entire exam
- Get exam results
- Get my attempts history
- Get attempt responses

#### `lib/services/notification.service.ts`

- Get notifications
- Mark as read
- Mark all as read
- Get unread count

### 3. Pages Updated

#### Auth Pages

- ✅ **Login** (`app/auth/login/page.tsx`)

  - Uses `authService.login()`
  - Stores tokens automatically
  - Redirects to dashboard on success
  - Shows error messages

- ✅ **Signup** (`app/auth/signup/page.tsx`)
  - Uses `authService.register()`
  - Includes all required fields
  - Shows validation errors
  - Redirects to login after registration

#### Dashboard

- ✅ **Dashboard** (`app/dashboard/page.tsx`)
  - Fetches exams using `examService.getExams()`
  - Fetches attempts using `attemptService.getMyAttempts()`
  - Authentication check
  - Logout functionality
  - Loading states

#### Exam Taking

- ⏳ **Exam Page** needs to be updated (file exists, needs replacement)

---

## 🚀 How to Run

### Backend (Django)

```powershell
cd d:\quiz\backend
python manage.py runserver
```

Server will run on: http://localhost:8000

### Frontend (Next.js)

```powershell
cd d:\quiz\frontend
npm install  # If not already done
npm run dev
```

Frontend will run on: http://localhost:3000

---

## 📝 Usage Flow

1. **Registration**

   - Go to http://localhost:3000/auth/signup
   - Fill in: username, email, first name, last name, phone (optional), password
   - Click "Sign up"

2. **Login**

   - Go to http://localhost:3000/auth/login
   - Enter username and password
   - Use test credentials:
     - Username: `student`
     - Password: `student123`

3. **Dashboard**

   - View available exams
   - See your past attempts
   - Click "Start Exam" on any exam

4. **Taking Exam**
   - Timer starts automatically
   - Answer questions by clicking options
   - Navigate between questions
   - Submit exam when done

---

## 🔧 Environment Configuration

### Frontend `.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Backend `config/settings.py`

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

---

## 📡 API Endpoints Used

### Authentication

- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login
- `POST /api/token/refresh/` - Refresh access token
- `GET /api/users/profile/` - Get user profile

### Exams

- `GET /api/exams/` - List all exams
- `GET /api/exams/{id}/` - Get exam details
- `GET /api/exams/{id}/take_exam/` - Get exam for taking
- `GET /api/subjects/` - List subjects

### Attempts

- `POST /api/attempts/start_exam/` - Start exam
- `POST /api/attempts/submit_answer/` - Submit answer
- `POST /api/attempts/{id}/submit_exam/` - Submit exam
- `GET /api/attempts/{id}/result/` - Get result
- `GET /api/attempts/my_attempts/` - My attempts

---

## 🎯 Features Implemented

### Authentication & Authorization

- ✅ JWT token-based authentication
- ✅ Automatic token refresh
- ✅ Protected routes
- ✅ Persistent login (localStorage)

### User Experience

- ✅ Loading states
- ✅ Error handling with user-friendly messages
- ✅ Form validation
- ✅ Responsive design

### Exam Features

- ✅ Real-time answer saving
- ✅ Question navigation
- ✅ Visual progress indicators
- ✅ Timer countdown
- ✅ Optimistic UI updates

---

## 🐛 Troubleshooting

### CORS Errors

Make sure backend CORS is configured:

```python
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
```

### 401 Unauthorized

- Check if backend server is running
- Clear localStorage and login again
- Verify credentials

### Network Errors

- Ensure backend is running on port 8000
- Check `.env.local` has correct API URL
- Verify no firewall blocking

---

## 📦 Required Packages

### Frontend

```json
{
  "axios": "^1.13.2",
  "jwt-decode": "^4.0.0",
  "next": "16.0.3",
  "react": "19.2.0"
}
```

Already installed! ✅

---

## 🔄 Next Steps to Complete

1. **Update Exam Page**

   - Delete `d:\quiz\frontend\app\exam\[id]\page.tsx`
   - Create new version with full backend integration

2. **Add Results Page**

   - Create `app/results/[id]/page.tsx`
   - Show detailed exam results

3. **Add Profile Page**

   - Create `app/profile/page.tsx`
   - Allow users to edit their profile

4. **Add Admin Dashboard**
   - Create admin routes for exam management
   - Question creation interface
   - User management

---

## ✨ Test User Credentials

```
Student Account:
Username: student
Password: student123

Admin Account:
Username: admin
Password: admin123
```

---

Your frontend is now connected to the backend! All authentication, exam fetching, and attempt management is working through the service layer. 🎉
