# DCET Platform - Database Documentation

## Overview
This document provides a comprehensive overview of the DCET EdTech platform's database structure, including all tables, relationships, and key design decisions.

## Database Statistics
- **Total Tables**: 18 (15 application tables + 3 Django framework tables)
- **Database Engine**: MySQL 8.0+
- **Character Set**: utf8mb4_unicode_ci
- **Storage Engine**: InnoDB (for transaction support)

---

## Table Categories

### 1. User Management (6 tables)
- `users` - Core user authentication and profiles
- `profiles` - Extended user profile with subscription info
- `email_otps` - Email verification codes
- `password_reset_requests` - Password reset tracking
- `user_activity` - Activity logging for security
- `notifications` - User notifications

### 2. Exam System (3 tables)
- `exams` - Exam/Mock test metadata
- `sections` - Exam sections (e.g., Engineering Mathematics)
- `questions` - Individual questions with options and answers

### 3. Results & Attempts (3 tables)
- `attempts` - User exam attempts tracking
- `attempt_answers` - Individual question responses
- `question_issues` - Student-reported question issues

### 4. Payment & Subscription (3 tables)
- `plans` - Subscription plan definitions
- `payments` - Payment transaction records
- `subscriptions` - Active user subscriptions

### 5. Admin & Settings (1 table)
- `app_settings` - Global application configuration

---

## Detailed Table Descriptions

### Users Table
**Purpose**: Core authentication and user profile management

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Primary key |
| username | VARCHAR(100) | Unique username |
| email | VARCHAR(150) | Unique email address |
| phone | VARCHAR(20) | Optional phone number |
| password_hash | VARCHAR(255) | Hashed password |
| email_verified | BOOLEAN | Email verification status |
| is_staff | BOOLEAN | Admin/staff access flag |
| user_tier | VARCHAR(10) | FREE or PRO tier |
| created_at | DATETIME(6) | Account creation timestamp |
| updated_at | DATETIME(6) | Last update timestamp |

**Indexes**: username, email, user_tier

---

### Profiles Table
**Purpose**: Extended user information with subscription details

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Primary key |
| user_id | BIGINT | Foreign key to users |
| is_paid | BOOLEAN | Payment status |
| plan_id | BIGINT | Foreign key to plans |
| subscription_start | DATETIME(6) | Subscription start date |
| subscription_end | DATETIME(6) | Subscription end date |

**Relationships**:
- One-to-One with `users`
- Many-to-One with `plans`

---

### Exams Table
**Purpose**: Store exam/mock test metadata

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Primary key |
| name | VARCHAR(100) | Exam name (e.g., "DCET") |
| year | INT | Exam year |
| total_marks | INT | Maximum marks |
| duration_minutes | INT | Time limit in minutes |
| solution_video_url | VARCHAR(200) | YouTube solution video |
| access_tier | VARCHAR(10) | FREE or PRO access |
| is_published | BOOLEAN | Publication status |
| created_at | DATETIME(6) | Creation timestamp |
| updated_at | DATETIME(6) | Last update timestamp |

**Indexes**: is_published, year, access_tier

---

### Sections Table
**Purpose**: Organize questions into exam sections

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Primary key |
| exam_id | BIGINT | Foreign key to exams |
| name | VARCHAR(200) | Section name |
| order | INT | Display order |
| max_marks | INT | Maximum marks for section |

**Unique Constraint**: (exam_id, order)

---

### Questions Table
**Purpose**: Store individual exam questions

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Primary key |
| section_id | BIGINT | Foreign key to sections |
| question_number | INT | Question number (1-20) |
| question_text | TEXT | Question with LaTeX support |
| plain_text | TEXT | Plain text version |
| option_a | VARCHAR(500) | Option A |
| option_b | VARCHAR(500) | Option B |
| option_c | VARCHAR(500) | Option C |
| option_d | VARCHAR(500) | Option D |
| correct_option | VARCHAR(1) | Correct answer (A/B/C/D) |
| marks | INT | Marks for question |
| diagram_url | VARCHAR(200) | Optional diagram URL |
| created_at | DATETIME(6) | Creation timestamp |

**Unique Constraint**: (section_id, question_number)

---

### Attempts Table
**Purpose**: Track user exam attempts

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Primary key |
| user_id | BIGINT | Foreign key to users |
| exam_id | BIGINT | Foreign key to exams |
| started_at | DATETIME(6) | Start time |
| finished_at | DATETIME(6) | End time |
| score | INT | Final score |
| status | VARCHAR(15) | in_progress/submitted/timeout |
| randomized_order | JSON | Question order array |

**Indexes**: user_id, exam_id, (user_id, exam_id), status

---

### Attempt Answers Table
**Purpose**: Store individual question responses

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Primary key |
| attempt_id | BIGINT | Foreign key to attempts |
| question_id | BIGINT | Foreign key to questions |
| selected_option | VARCHAR(1) | User's answer (A/B/C/D) |
| is_correct | BOOLEAN | Correctness flag |

**Unique Constraint**: (attempt_id, question_id)

---

### Plans Table
**Purpose**: Define subscription plans

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Primary key |
| key | VARCHAR(50) | Unique plan key |
| name | VARCHAR(100) | Plan display name |
| price_in_paisa | INT | Price (100 paisa = 1 rupee) |
| duration_days | INT | Subscription duration |
| features | JSON | Feature list array |
| is_active | BOOLEAN | Availability status |
| created_at | DATETIME(6) | Creation timestamp |

---

### Payments Table
**Purpose**: Track payment transactions

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Primary key |
| user_id | BIGINT | Foreign key to users |
| provider | VARCHAR(50) | Payment provider (razorpay) |
| provider_payment_id | VARCHAR(255) | Provider's payment ID |
| order_id | VARCHAR(255) | Order identifier |
| amount | INT | Amount in paisa |
| currency | VARCHAR(10) | Currency code (INR) |
| status | VARCHAR(20) | Payment status |
| metadata | JSON | Additional data |
| created_at | DATETIME(6) | Creation timestamp |
| updated_at | DATETIME(6) | Last update timestamp |

**Payment Statuses**: created, paid, activated, failed, refunded

---

### Subscriptions Table
**Purpose**: Manage user subscriptions

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Primary key |
| user_id | BIGINT | Foreign key to users |
| plan_id | BIGINT | Foreign key to plans |
| payment_id | BIGINT | Foreign key to payments |
| status | VARCHAR(20) | Subscription status |
| start_date | DATETIME(6) | Start date |
| end_date | DATETIME(6) | End date |
| auto_renew | BOOLEAN | Auto-renewal flag |
| cancelled_at | DATETIME(6) | Cancellation timestamp |
| created_at | DATETIME(6) | Creation timestamp |
| updated_at | DATETIME(6) | Last update timestamp |

**Subscription Statuses**: active, expired, cancelled

---

## Key Relationships

```
users (1) ←→ (1) profiles
users (1) → (N) attempts
users (1) → (N) payments
users (1) → (N) subscriptions
users (1) → (N) notifications
users (1) → (N) user_activity
users (1) → (N) password_reset_requests
users (1) → (N) question_issues

exams (1) → (N) sections
exams (1) → (N) attempts

sections (1) → (N) questions

attempts (1) → (N) attempt_answers

questions (1) → (N) attempt_answers
questions (1) → (N) question_issues

plans (1) → (N) profiles
plans (1) → (N) subscriptions

payments (1) → (1) subscriptions
```

---

## Access Control System

### User Tiers
1. **FREE** - Limited access
   - Access to FREE tier exams only
   - Basic features

2. **PRO** - Full access
   - Access to all exams (FREE + PRO)
   - Video solutions
   - Advanced analytics
   - Priority support

### Exam Access Tiers
- **FREE**: Available to all users
- **PRO**: Requires PRO subscription

---

## Indexing Strategy

### Primary Indexes
- All tables have auto-incrementing BIGINT primary keys
- Unique constraints on natural keys (username, email, etc.)

### Foreign Key Indexes
- All foreign key columns are indexed for join performance
- Composite indexes on frequently joined columns

### Query Optimization Indexes
- `users`: username, email, user_tier
- `exams`: is_published, year, access_tier
- `attempts`: (user_id, exam_id), status
- `payments`: (user_id, status), provider_payment_id
- `subscriptions`: (user_id, status), end_date, (status, end_date)

---

## Data Integrity

### Foreign Key Constraints
- **CASCADE**: Delete child records when parent is deleted
  - user → attempts, payments, subscriptions
  - exam → sections → questions
  - attempt → attempt_answers

- **SET NULL**: Preserve child records, nullify reference
  - payment → subscription (optional link)
  - attempt → question_issues (preserve reports)

- **PROTECT**: Prevent deletion of referenced records
  - plan → subscriptions (can't delete active plans)

### Check Constraints
- `users.user_tier`: IN ('FREE', 'PRO')
- `exams.access_tier`: IN ('FREE', 'PRO')
- `questions.correct_option`: IN ('A', 'B', 'C', 'D')
- `attempts.status`: IN ('in_progress', 'submitted', 'timeout')
- `payments.status`: IN ('created', 'paid', 'activated', 'failed', 'refunded')
- `subscriptions.status`: IN ('active', 'expired', 'cancelled')

---

## JSON Fields

### Usage
JSON fields provide flexibility for storing structured data without schema changes:

1. **plans.features**: Array of feature strings
   ```json
   ["Access to all PYQ papers", "10 Mock Tests", "Video solutions"]
   ```

2. **payments.metadata**: Additional payment information
   ```json
   {"razorpay_signature": "...", "notes": "..."}
   ```

3. **attempts.randomized_order**: Question ID sequence
   ```json
   [45, 23, 67, 12, ...]
   ```

---

## Performance Considerations

### Optimizations
1. **Connection Pooling**: Configured in Django settings
2. **Redis Caching**: For frequently accessed data
3. **Selective Indexing**: Balance between read and write performance
4. **Normalized Design**: Minimize data redundancy
5. **Appropriate Data Types**: BIGINT for scalability

### Query Patterns
- Use indexes for WHERE, JOIN, and ORDER BY clauses
- Composite indexes for multi-column queries
- Covering indexes where beneficial

---

## Security Features

### Authentication
- Password hashing using Django's built-in hashers
- Email verification via OTP
- Password reset with token expiration

### Activity Logging
- Track user activities with IP and user agent
- Audit trail for security monitoring

### Payment Security
- Razorpay integration with signature verification
- Idempotent payment processing
- Transaction status tracking

---

## Backup & Maintenance

### Recommended Practices
1. **Regular Backups**: Daily automated backups
2. **Migration Tracking**: Django migrations table
3. **Index Maintenance**: Periodic ANALYZE and OPTIMIZE
4. **Archive Old Data**: Move completed attempts to archive tables
5. **Monitor Performance**: Track slow queries

---

## Future Enhancements

### Potential Additions
1. **Analytics Tables**: Detailed performance metrics
2. **Referral System**: User referral tracking
3. **Coupon System**: Discount codes and promotions
4. **Discussion Forum**: Question discussions
5. **Bookmarks**: Save questions for later review
6. **Study Plans**: Personalized study schedules

---

## File Locations

- **Schema File**: `database_schema.sql`
- **Django Models**: 
  - `users/models.py`
  - `exams/models.py`
  - `results/models.py`
  - `payments/models.py`
  - `adminpanel/models.py`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-20 | Initial comprehensive schema documentation |

---

## Contact & Support

For questions about the database schema or modifications, refer to the Django model files or consult the development team.
