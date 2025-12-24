# Authentication API Documentation

## Overview

Complete JWT-based authentication system with user signup, login, and profile management.

---

## Endpoints

### 1. User Signup

**POST** `/api/auth/signup/`

Register a new user account.

**Request Body:**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "name": "John Doe",
  "mobile": "1234567890",
  "password": "password123",
  "confirm_password": "password123"
}
```

**Required Fields:**

- `username` (string, unique)
- `email` (string, unique, valid email format)
- `name` (string)
- `password` (string, min 6 characters)
- `confirm_password` (string, must match password)

**Optional Fields:**

- `mobile` (string)

**Success Response (201):**

```json
{
  "message": "User registered successfully",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe",
    "mobile": "1234567890",
    "role": "student",
    "email_verified": false,
    "mobile_verified": false,
    "is_active": true,
    "last_login": null
  }
}
```

**Error Responses:**

400 - Validation Error (Username exists):

```json
{
  "username": ["Username already exists"]
}
```

400 - Validation Error (Email exists):

```json
{
  "email": ["Email already exists"]
}
```

400 - Validation Error (Password mismatch):

```json
{
  "confirm_password": ["Passwords do not match"]
}
```

---

### 2. User Login

**POST** `/api/auth/login/`

Authenticate user and get JWT tokens.

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "password123"
}
```

**Success Response (200):**

```json
{
  "message": "Login successful",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe",
    "role": "student"
  }
}
```

**Error Responses:**

401 - Invalid Credentials:

```json
{
  "error": "Invalid username or password"
}
```

403 - Account Disabled:

```json
{
  "error": "Account disabled"
}
```

---

### 3. Get Current User

**GET** `/api/auth/me/`

Get authenticated user's profile.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Success Response (200):**

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "name": "John Doe",
  "mobile": "1234567890",
  "role": "student",
  "email_verified": false,
  "mobile_verified": false,
  "is_active": true,
  "last_login": "2025-12-01T10:30:00Z"
}
```

**Error Response:**

401 - Unauthorized:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 4. Refresh Token

**POST** `/api/token/refresh/`

Get new access token using refresh token.

**Request Body:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (200):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Authentication Flow

### 1. Signup Flow

```
Client                              Server
  |                                    |
  |--- POST /api/auth/signup/ -------->|
  |    {username, email, name, ...}    |
  |                                    |
  |                          [Validate data]
  |                          [Check uniqueness]
  |                          [Hash password]
  |                          [Create user]
  |                          [Generate JWT]
  |                                    |
  |<---- 201 Created ------------------|
  |    {access, refresh, user}         |
  |                                    |
  |--- Store tokens in localStorage ---|
```

### 2. Login Flow

```
Client                              Server
  |                                    |
  |--- POST /api/auth/login/ --------->|
  |    {username, password}            |
  |                                    |
  |                          [Find user]
  |                          [Check password]
  |                          [Verify active]
  |                          [Update last_login]
  |                          [Generate JWT]
  |                                    |
  |<---- 200 OK -----------------------|
  |    {access, refresh, user}         |
  |                                    |
  |--- Store tokens in localStorage ---|
```

### 3. Authenticated Request Flow

```
Client                              Server
  |                                    |
  |--- GET /api/auth/me/ ------------->|
  |    Authorization: Bearer <token>   |
  |                                    |
  |                          [Verify JWT]
  |                          [Get user]
  |                                    |
  |<---- 200 OK -----------------------|
  |    {user data}                     |
```

---

## Security Features

1. **Password Hashing**

   - Uses Django's `make_password()` with PBKDF2
   - Passwords stored in `password_hash` field
   - Never returns passwords in responses

2. **JWT Tokens**

   - Access token expires in 60 minutes
   - Refresh token expires in 7 days
   - Tokens include user_id, username, and role claims

3. **Validation**

   - Username uniqueness enforced
   - Email uniqueness enforced
   - Password minimum length: 6 characters
   - Password confirmation required

4. **Error Messages**
   - Generic error for invalid login (prevents username enumeration)
   - Specific errors for validation issues during signup

---

## Database Schema

### User Model (`users` table)

```python
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=150, unique=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    password_hash = models.CharField(max_length=255)
    name = models.CharField(max_length=150)

    email_verified = models.BooleanField(default=False)
    mobile_verified = models.BooleanField(default=False)

    role = models.CharField(max_length=10, default='student')
    # Choices: 'student', 'admin'

    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

---

## Testing

Run the test suite:

```bash
cd backend
python test_auth_flow.py
```

This will test:

- User signup
- Password validation
- User login
- Invalid credentials handling
- /auth/me/ endpoint

---

## Frontend Integration

### Install axios:

```bash
npm install axios
```

### Example Usage:

```typescript
// Signup
const signupData = {
  username: "johndoe",
  email: "john@example.com",
  name: "John Doe",
  mobile: "1234567890",
  password: "password123",
  confirm_password: "password123",
};

const response = await axios.post("/api/auth/signup/", signupData);
localStorage.setItem("access_token", response.data.access);
localStorage.setItem("refresh_token", response.data.refresh);

// Login
const loginData = {
  username: "johndoe",
  password: "password123",
};

const response = await axios.post("/api/auth/login/", loginData);
localStorage.setItem("access_token", response.data.access);

// Authenticated request
const config = {
  headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
};

const profile = await axios.get("/api/auth/me/", config);
```

---

## Configuration

### settings.py

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'users',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

---

## Complete Code Files

### 1. serializers.py

See: `backend/users/serializers.py`

### 2. views.py

See: `backend/users/views.py`

### 3. urls.py

See: `backend/users/urls.py`

### 4. tokens.py

See: `backend/users/tokens.py`

### 5. models.py

See: `backend/users/models.py`

---

**Last Updated:** December 2025
