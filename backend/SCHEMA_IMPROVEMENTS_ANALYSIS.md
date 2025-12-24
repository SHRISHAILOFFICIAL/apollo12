# Database Schema Improvements - Analysis & Recommendations

## Overview
This document analyzes the suggested database improvements from `imp_check.md` and provides recommendations on implementation priority and approach.

---

## ✅ CRITICAL - Implement Immediately

### 1. Remove Duplicated Subscription State ⭐⭐⭐
**Status**: **AGREE - CRITICAL**

**Problem**: 
- Three sources of truth for subscription status:
  - `users.user_tier` (FREE/PRO)
  - `profiles.is_paid` (boolean)
  - `subscriptions` table (complete subscription data)

**Impact**: 
- Data inconsistency bugs
- Complex sync logic
- Race conditions during payment processing

**Recommendation**: 
```sql
-- Phase 1: Add migration to compute user_tier from subscriptions
-- Phase 2: Remove these columns:
ALTER TABLE users DROP COLUMN user_tier;
ALTER TABLE profiles DROP COLUMN is_paid;
ALTER TABLE profiles DROP COLUMN plan_id;
ALTER TABLE profiles DROP COLUMN subscription_start;
ALTER TABLE profiles DROP COLUMN subscription_end;
```

**Implementation Notes**:
- Create a database view or property method to compute current tier
- Update all queries to use subscriptions table
- Add index: `CREATE INDEX idx_active_subs ON subscriptions (user_id, status, end_date);`

**Code Changes Required**:
- `users/models.py`: Remove `user_tier` field, add `@property current_tier()`
- `profiles/models.py`: Remove subscription fields
- All API endpoints: Update tier checking logic
- Payment verification: Update to only modify subscriptions table

---

### 2. Fix Circular Foreign Key Dependency ⭐⭐⭐
**Status**: **AGREE - CRITICAL**

**Problem**: 
- `profiles.plan_id → plans.id` creates unnecessary coupling
- Already tracked in `subscriptions.plan_id`

**Recommendation**: 
```sql
ALTER TABLE profiles DROP FOREIGN KEY profiles_plan_id_fkey;
ALTER TABLE profiles DROP COLUMN plan_id;
```

**Note**: This is resolved by implementing suggestion #1.

---

### 3. Do Not Store Derived Correctness ⭐⭐
**Status**: **PARTIALLY AGREE**

**Problem**: 
- `attempt_answers.is_correct` is redundant
- Can be computed: `selected_option == question.correct_option`

**Counter-argument**:
- ✅ **Keep it for performance**: Computing correctness on every query is expensive
- ✅ **Historical accuracy**: If admin fixes a wrong answer, old attempts remain unchanged
- ✅ **Analytics queries**: Much faster with pre-computed correctness

**Recommendation**: 
**KEEP `is_correct` but add a trigger/constraint to ensure consistency**

```sql
-- Add a database trigger to auto-compute is_correct on INSERT/UPDATE
DELIMITER $$
CREATE TRIGGER before_attempt_answer_insert
BEFORE INSERT ON attempt_answers
FOR EACH ROW
BEGIN
    DECLARE correct_ans VARCHAR(1);
    SELECT correct_option INTO correct_ans 
    FROM questions 
    WHERE id = NEW.question_id;
    
    SET NEW.is_correct = (NEW.selected_option = correct_ans);
END$$
DELIMITER ;
```

**Alternative**: Add a computed column (MySQL 5.7+):
```sql
-- This is read-only and always accurate
ALTER TABLE attempt_answers 
ADD COLUMN is_correct BOOLEAN AS (
    selected_option = (SELECT correct_option FROM questions WHERE id = question_id)
) STORED;
```

---

## ⚠️ HIGH PRIORITY - Implement Soon

### 4. Add Negative Marking Support ⭐⭐⭐
**Status**: **AGREE - HIGH PRIORITY**

**Recommendation**: 
```sql
ALTER TABLE questions
ADD COLUMN negative_marks DECIMAL(4,2) DEFAULT 0 COMMENT 'Marks deducted for wrong answer';

-- Also add to exams table for global negative marking
ALTER TABLE exams
ADD COLUMN negative_marking_enabled BOOLEAN DEFAULT FALSE,
ADD COLUMN negative_marks_per_question DECIMAL(4,2) DEFAULT 0.25;
```

**Implementation**:
- Update score calculation logic in `results/views.py`
- Add negative marking toggle in admin panel
- Display negative marking info on exam start page

---

### 5. Restrict Multiple Attempts Per Exam ⭐⭐
**Status**: **CONDITIONAL AGREE**

**Analysis**:
- **For PYQ papers**: Usually single attempt only
- **For mock tests**: May allow multiple attempts for practice

**Recommendation**: 
```sql
-- Add attempt limit to exams table
ALTER TABLE exams
ADD COLUMN max_attempts INT DEFAULT 1 COMMENT 'Maximum attempts allowed per user, 0 = unlimited';

-- Add attempt counter
ALTER TABLE attempts
ADD COLUMN attempt_number INT DEFAULT 1;

-- Add composite index for checking
CREATE INDEX idx_user_exam_attempts ON attempts (user_id, exam_id, attempt_number);
```

**Business Logic** (in Django):
```python
def can_start_exam(user, exam):
    if exam.max_attempts == 0:
        return True  # Unlimited
    
    attempt_count = Attempt.objects.filter(
        user=user, 
        exam=exam,
        status__in=['submitted', 'timeout']
    ).count()
    
    return attempt_count < exam.max_attempts
```

---

### 6. Secure OTP Storage ⭐⭐⭐
**Status**: **PARTIALLY AGREE**

**Analysis**:
- OTPs are short-lived (10 minutes)
- Need to compare user input with stored OTP
- Hashing makes comparison harder (can't use simple equality)

**Current Implementation**: Already has `created_at` for expiry checking

**Recommendation**: 
**Add explicit expiry but KEEP plaintext OTP** (it's already short-lived)

```sql
ALTER TABLE email_otps
ADD COLUMN expires_at DATETIME(6) AS (DATE_ADD(created_at, INTERVAL 10 MINUTE)) STORED;

-- Add cleanup job to delete expired OTPs
CREATE EVENT cleanup_expired_otps
ON SCHEDULE EVERY 1 HOUR
DO
DELETE FROM email_otps WHERE expires_at < NOW();
```

**Security Measures**:
- ✅ Rate limiting (already suggested in #13)
- ✅ Short expiry (10 minutes)
- ✅ One-time use (mark as verified)
- ✅ Delete after verification

**Alternative** (if you want hashing):
```python
import hashlib

def hash_otp(otp):
    return hashlib.sha256(f"{otp}{settings.OTP_SALT}".encode()).hexdigest()

def verify_otp(email, input_otp):
    hashed = hash_otp(input_otp)
    return EmailOTP.objects.filter(
        email=email,
        otp_hash=hashed,
        is_verified=False,
        expires_at__gt=timezone.now()
    ).exists()
```

---

## 📊 MEDIUM PRIORITY - Plan for Implementation

### 7. Add Soft Delete Support ⭐⭐
**Status**: **AGREE - GOOD PRACTICE**

**Recommendation**: 
```sql
-- Add to critical tables
ALTER TABLE users ADD COLUMN deleted_at DATETIME(6) NULL;
ALTER TABLE exams ADD COLUMN deleted_at DATETIME(6) NULL;
ALTER TABLE questions ADD COLUMN deleted_at DATETIME(6) NULL;
ALTER TABLE payments ADD COLUMN deleted_at DATETIME(6) NULL;
ALTER TABLE subscriptions ADD COLUMN deleted_at DATETIME(6) NULL;

-- Add indexes for queries
CREATE INDEX idx_users_deleted ON users (deleted_at);
CREATE INDEX idx_exams_deleted ON exams (deleted_at);
```

**Django Implementation**:
```python
# Use django-safedelete or implement custom manager
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class User(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Include deleted
    
    def delete(self, hard=False):
        if hard:
            super().delete()
        else:
            self.deleted_at = timezone.now()
            self.save()
```

---

### 8. Add Exam Availability Window ⭐⭐
**Status**: **AGREE - USEFUL FEATURE**

**Recommendation**: 
```sql
ALTER TABLE exams
ADD COLUMN available_from DATETIME(6) NULL COMMENT 'Exam becomes available from this time',
ADD COLUMN available_until DATETIME(6) NULL COMMENT 'Exam available until this time';

-- Add index for checking availability
CREATE INDEX idx_exam_availability ON exams (available_from, available_until, is_published);
```

**Use Cases**:
- Schedule exam releases (e.g., release 2024 paper on Jan 1, 2025)
- Time-limited mock tests
- Beta testing with limited access

**Query**:
```python
def get_available_exams():
    now = timezone.now()
    return Exam.objects.filter(
        is_published=True,
        available_from__lte=now,
        available_until__gte=now
    )
```

---

### 9. Improve Question Metadata ⭐⭐
**Status**: **AGREE - GOOD FOR ANALYTICS**

**Recommendation**: 
```sql
ALTER TABLE questions
ADD COLUMN difficulty ENUM('easy','medium','hard') DEFAULT 'medium',
ADD COLUMN topic VARCHAR(100) NULL COMMENT 'e.g., Calculus, Probability',
ADD COLUMN explanation TEXT NULL COMMENT 'Detailed solution explanation';

-- Add indexes for filtering
CREATE INDEX idx_question_difficulty ON questions (difficulty);
CREATE INDEX idx_question_topic ON questions (topic);
```

**Benefits**:
- Filter questions by difficulty
- Topic-wise analytics
- Adaptive learning paths
- Better study recommendations

---

## 🚀 PERFORMANCE OPTIMIZATIONS

### 10. Improve Performance with Missing Indexes ⭐⭐⭐
**Status**: **AGREE - IMPLEMENT IMMEDIATELY**

**Recommendation**: 
```sql
-- Leaderboard queries
CREATE INDEX idx_exam_score ON attempts (exam_id, score DESC, finished_at);

-- Question analytics
CREATE INDEX idx_question_attempt ON attempt_answers (question_id, is_correct);

-- Payment reports
CREATE INDEX idx_payments_created ON payments (created_at, status);
CREATE INDEX idx_payments_user_created ON payments (user_id, created_at DESC);

-- Subscription queries
CREATE INDEX idx_subscriptions_active ON subscriptions (status, end_date);

-- User activity
CREATE INDEX idx_user_activity_created ON user_activity (user_id, created_at DESC);
```

**Impact**: 
- 10-100x faster leaderboard queries
- Instant payment reports
- Faster analytics dashboards

---

## 📈 ADVANCED FEATURES

### 11. Add Result Snapshot Table ⭐⭐⭐
**Status**: **STRONGLY AGREE - EXCELLENT IDEA**

**Enhanced Recommendation**: 
```sql
CREATE TABLE results (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    attempt_id BIGINT UNIQUE NOT NULL,
    user_id BIGINT NOT NULL,
    exam_id BIGINT NOT NULL,
    
    -- Score breakdown
    correct_count INT NOT NULL DEFAULT 0,
    wrong_count INT NOT NULL DEFAULT 0,
    unattempted_count INT NOT NULL DEFAULT 0,
    total_score DECIMAL(6,2) NOT NULL,
    max_score INT NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    
    -- Ranking (computed after all attempts)
    rank INT NULL,
    percentile DECIMAL(5,2) NULL,
    total_participants INT NULL,
    
    -- Section-wise performance
    section_scores JSON NULL COMMENT 'Array of {section_id, score, max_score}',
    
    -- Time analytics
    time_taken_seconds INT NOT NULL,
    avg_time_per_question DECIMAL(6,2) NULL,
    
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX idx_user_results (user_id, created_at DESC),
    INDEX idx_exam_results (exam_id, total_score DESC),
    INDEX idx_exam_rank (exam_id, rank),
    
    FOREIGN KEY (attempt_id) REFERENCES attempts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Pre-computed result snapshots for fast analytics';
```

**Benefits**:
- Instant result display (no computation needed)
- Historical ranking preserved
- Fast leaderboards
- Analytics without JOIN hell

---

### 12. Add Admin Audit Logging ⭐⭐
**Status**: **AGREE - IMPORTANT FOR COMPLIANCE**

**Enhanced Recommendation**: 
```sql
CREATE TABLE admin_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    admin_id BIGINT NOT NULL,
    action VARCHAR(50) NOT NULL COMMENT 'CREATE, UPDATE, DELETE, APPROVE, REJECT',
    target_table VARCHAR(50) NOT NULL,
    target_id BIGINT NULL,
    old_values JSON NULL COMMENT 'Before state',
    new_values JSON NULL COMMENT 'After state',
    ip_address VARCHAR(50) NULL,
    user_agent TEXT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX idx_admin_logs_admin (admin_id, created_at DESC),
    INDEX idx_admin_logs_target (target_table, target_id),
    INDEX idx_admin_logs_action (action, created_at DESC),
    
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Audit trail for admin actions';
```

**Use Cases**:
- Track who modified questions
- Payment refund audit trail
- User account modifications
- Compliance and security

---

### 13. Add Rate-Limit Protection ⭐⭐⭐
**Status**: **AGREE - CRITICAL FOR SECURITY**

**Enhanced Recommendation**: 
```sql
CREATE TABLE rate_limits (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    identifier VARCHAR(100) NOT NULL COMMENT 'IP address or user_id',
    action VARCHAR(50) NOT NULL COMMENT 'login, otp_request, exam_submit',
    attempts INT NOT NULL DEFAULT 1,
    window_start DATETIME(6) NOT NULL,
    blocked_until DATETIME(6) NULL,
    
    UNIQUE KEY unique_identifier_action (identifier, action),
    INDEX idx_rate_limit_check (identifier, action, window_start),
    INDEX idx_blocked (blocked_until)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Rate limiting for abuse prevention';

-- Cleanup old entries
CREATE EVENT cleanup_rate_limits
ON SCHEDULE EVERY 1 HOUR
DO
DELETE FROM rate_limits WHERE window_start < DATE_SUB(NOW(), INTERVAL 24 HOUR);
```

**Rate Limit Rules**:
```python
RATE_LIMITS = {
    'login': {'max_attempts': 5, 'window_minutes': 15, 'block_minutes': 30},
    'otp_request': {'max_attempts': 3, 'window_minutes': 10, 'block_minutes': 60},
    'exam_submit': {'max_attempts': 3, 'window_minutes': 1, 'block_minutes': 5},
    'payment_create': {'max_attempts': 5, 'window_minutes': 10, 'block_minutes': 30},
}
```

**Alternative**: Use Redis for rate limiting (faster, auto-expiry)
```python
# Using Redis
def check_rate_limit(identifier, action):
    key = f"rate_limit:{action}:{identifier}"
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, 900)  # 15 minutes
    return count <= RATE_LIMITS[action]['max_attempts']
```

---

## 📋 Implementation Priority

### Phase 1 - Critical (Week 1)
1. ✅ Remove duplicated subscription state (#1, #2)
2. ✅ Add performance indexes (#10)
3. ✅ Add rate limiting (#13)

### Phase 2 - High Priority (Week 2)
4. ✅ Add negative marking (#4)
5. ✅ Add attempt restrictions (#5)
6. ✅ Add result snapshot table (#11)

### Phase 3 - Medium Priority (Week 3-4)
7. ✅ Add soft delete (#7)
8. ✅ Add exam availability window (#8)
9. ✅ Add question metadata (#9)
10. ✅ Add admin audit logging (#12)

### Phase 4 - Optional Enhancements
11. ✅ OTP hashing (if required by security audit)
12. ✅ Computed columns for derived data

---

## 🚨 Breaking Changes Warning

The following changes will require code updates:

1. **Removing `users.user_tier`**: Update all tier checking logic
2. **Removing `profiles.is_paid`**: Update payment verification
3. **Removing `attempt_answers.is_correct`**: Update score calculation (if removed)

**Migration Strategy**:
1. Create new fields/tables
2. Migrate data
3. Update application code
4. Test thoroughly
5. Remove old fields

---

## 📝 Summary

**Strongly Recommended** (13/13):
- All suggestions are valuable and well-thought-out
- Priority should be: Critical → Performance → Features → Enhancements

**Key Disagreements**:
- Keep `is_correct` for performance (use trigger for consistency)
- Keep plaintext OTP (already secure with short expiry + rate limiting)

**Additional Suggestions**:
- Use Redis for rate limiting (faster than DB)
- Add result snapshot table (excellent for analytics)
- Consider using Django signals for audit logging
- Implement soft delete with django-safedelete package

---

## Next Steps

1. Review this analysis
2. Prioritize based on your timeline
3. Create Django migrations for approved changes
4. Update application code
5. Test thoroughly before deployment

Would you like me to generate the Django migration files for any of these changes?
