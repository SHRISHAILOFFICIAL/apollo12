# Quiz Platform API Documentation

## Base URL

```
http://127.0.0.1:8000/api
```

## Authentication

The API uses JWT (JSON Web Token) authentication. Most endpoints require authentication.

### Obtain Token

- **POST** `/token/`
- **POST** `/token/refresh/`

---

## User Endpoints

### 1. User Registration

- **POST** `/users/register/`
- **Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "mobile_number": "9876543210"
}
```

- **Response:** User object + JWT tokens

### 2. User Login

- **POST** `/users/login/`
- **Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

- **Response:** User object + JWT tokens

### 3. Get User Profile

- **GET** `/users/profile/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** User profile with notification counts

### 4. Update User Profile

- **PUT/PATCH** `/users/profile/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:** Fields to update
- **Response:** Updated user object

### 5. Request Password Reset

- **POST** `/users/request_password_reset/`
- **Body:**

```json
{
  "email": "user@example.com"
}
```

- **Response:** Success message + reset token

### 6. Reset Password

- **POST** `/users/reset_password/`
- **Body:**

```json
{
  "token": "reset_token_here",
  "new_password": "newsecurepassword"
}
```

- **Response:** Success message

### 7. Notifications

- **GET** `/notifications/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** List of notifications

### 8. Mark Notification as Read

- **POST** `/notifications/{id}/mark_read/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** Updated notification

### 9. Mark All Notifications as Read

- **POST** `/notifications/mark_all_read/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** Success message

### 10. User Activity

- **GET** `/activities/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** List of user activities

---

## Exam Management Endpoints

### 11. List Subjects

- **GET** `/subjects/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** List of subjects

### 12. Create Subject (Admin only)

- **POST** `/subjects/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "name": "Mathematics",
  "code": "MATH101",
  "description": "Basic Mathematics"
}
```

- **Response:** Created subject

### 13. List Exams

- **GET** `/exams/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Query Params:**
  - `is_published=true` - Filter published exams
  - `is_active=true` - Filter active exams
- **Response:** List of exams

### 14. Get Exam Details

- **GET** `/exams/{id}/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** Detailed exam with questions

### 15. Create Exam (Admin only)

- **POST** `/exams/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "title": "Math Final Exam",
  "description": "Final examination for Math 101",
  "duration": 60,
  "total_marks": 100,
  "passing_marks": 40,
  "exam_date": "2025-12-15T10:00:00Z",
  "start_time": "10:00:00",
  "end_time": "11:00:00",
  "negative_marking": 0.25,
  "is_published": false
}
```

- **Response:** Created exam

### 16. Take Exam (Student view)

- **GET** `/exams/{id}/take_exam/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** Exam with questions (without correct answers)

### 17. Publish Exam (Admin only)

- **POST** `/exams/{id}/publish/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** Updated exam

### 18. Unpublish Exam (Admin only)

- **POST** `/exams/{id}/unpublish/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** Updated exam

### 19. Exam Statistics (Admin only)

- **GET** `/exams/{id}/statistics/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**

```json
{
  "total_attempts": 50,
  "completed_attempts": 45,
  "in_progress_attempts": 5,
  "average_score": 75.5,
  "pass_rate": 85.0
}
```

### 20. List Questions

- **GET** `/questions/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Query Params:**
  - `exam={exam_id}` - Filter by exam
  - `difficulty=easy|medium|hard` - Filter by difficulty
- **Response:** List of questions

### 21. Create Question (Admin only)

- **POST** `/questions/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "exam": 1,
  "question_text": "What is 2+2?",
  "marks": 1,
  "difficulty": "easy",
  "options": [
    { "option_text": "3", "is_correct": false },
    { "option_text": "4", "is_correct": true },
    { "option_text": "5", "is_correct": false },
    { "option_text": "6", "is_correct": false }
  ]
}
```

- **Response:** Created question with options

---

## Exam Attempt Endpoints

### 22. Start Exam

- **POST** `/attempts/start_exam/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "exam": 1
}
```

- **Response:** Created attempt with empty responses

### 23. Submit Answer

- **POST** `/attempts/submit_answer/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "attempt": 1,
  "question": 5,
  "option": 3
}
```

- **Response:** Updated response with correctness

### 24. Submit Exam

- **POST** `/attempts/{id}/submit_exam/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** Final score and exam details

### 25. Get Exam Result

- **GET** `/attempts/{id}/result/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** Detailed result with analytics

```json
{
  "attempt": {...},
  "total_score": 85,
  "percentage": 85.0,
  "result": "Pass",
  "rank": 5,
  "total_questions": 50,
  "correct_answers": 42,
  "incorrect_answers": 5,
  "unanswered": 3
}
```

### 26. My Attempts

- **GET** `/attempts/my_attempts/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** List of user's exam attempts

### 27. Attempt Responses

- **GET** `/responses/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Query Params:**
  - `attempt={attempt_id}` - Filter by attempt
- **Response:** List of responses

---

## Response Formats

### Success Response

```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2"
}
```

### Error Response

```json
{
  "error": "Error message here"
}
```

### Validation Error Response

```json
{
  "field_name": ["Error message for this field"]
}
```

---

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Notes

1. All datetime fields use ISO 8601 format: `2025-12-15T10:00:00Z`
2. JWT tokens expire after 60 minutes (access) and 7 days (refresh)
3. Admin-only endpoints require `is_staff=True` or `is_superuser=True`
4. Pagination is available on list endpoints (default: 100 items per page)
5. Use `Accept: application/json` header for all requests
