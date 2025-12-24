🔴 STILL REQUIRED / STRONGLY RECOMMENDED FIXES
1️⃣ email_otps still stores OTP in plaintext (SECURITY ISSUE)

❌ Current:

otp VARCHAR(6) NOT NULL


✔ Fix:

Remove plaintext OTP

Store hash + expiry

ALTER TABLE email_otps
DROP COLUMN otp;

ALTER TABLE email_otps
ADD COLUMN otp_hash VARCHAR(255) NOT NULL,
ADD COLUMN expires_at DATETIME(6) NOT NULL;

2️⃣ attempt_answers.is_correct should NOT be stored

You re-introduced a derived column (bug-prone).

❌ Current:

is_correct BOOLEAN NOT NULL DEFAULT FALSE


✔ Fix (recommended):

ALTER TABLE attempt_answers
DROP COLUMN is_correct;


✔ Compute correctness using:

selected_option = questions.correct_option


If you want snapshotted results, use a results table instead.

3️⃣ Missing negative marking support (DCET requires this)

❌ No negative marks support currently.

✔ Fix:

ALTER TABLE questions
ADD COLUMN negative_marks DECIMAL(4,2) DEFAULT 0;

4️⃣ No restriction on multiple attempts per exam

Right now:

Same user can start unlimited attempts for same exam

✔ Choose ONE:

Option A – Only one attempt allowed

ALTER TABLE attempts
ADD UNIQUE KEY unique_user_exam (user_id, exam_id);


Option B – Multiple attempts allowed

ALTER TABLE attempts
ADD COLUMN attempt_number INT NOT NULL DEFAULT 1,
ADD UNIQUE KEY unique_user_exam_attempt (user_id, exam_id, attempt_number);

5️⃣ Exams lack availability window (only is_published)

This limits scheduling.

✔ Fix:

ALTER TABLE exams
ADD COLUMN available_from DATETIME(6) NULL,
ADD COLUMN available_until DATETIME(6) NULL;

6️⃣ No soft-delete support (important for admin & GDPR)

Right now deletes are hard deletes.

✔ Add soft delete:

ALTER TABLE users ADD COLUMN deleted_at DATETIME(6) NULL;
ALTER TABLE exams ADD COLUMN deleted_at DATETIME(6) NULL;
ALTER TABLE questions ADD COLUMN deleted_at DATETIME(6) NULL;
ALTER TABLE payments ADD COLUMN deleted_at DATETIME(6) NULL;

7️⃣ access_tier should be ENUM, not VARCHAR

❌ Current:

access_tier VARCHAR(10)


✔ Fix:

ALTER TABLE exams
MODIFY access_tier ENUM('FREE','PRO') NOT NULL DEFAULT 'PRO';

🟡 OPTIONAL BUT HIGH-VALUE ADDITIONS
8️⃣ Result snapshot table (performance + analytics)

Avoid recalculating scores repeatedly.

CREATE TABLE results (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    attempt_id BIGINT UNIQUE,
    correct_count INT,
    wrong_count INT,
    unattempted_count INT,
    total_score INT,
    percentile DECIMAL(5,2),
    rank INT,
    created_at DATETIME(6),
    FOREIGN KEY (attempt_id) REFERENCES attempts(id)
);

9️⃣ Admin audit logging (recommended for production)
CREATE TABLE admin_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    admin_id BIGINT,
    action VARCHAR(255),
    target_table VARCHAR(50),
    target_id BIGINT,
    created_at DATETIME(6),
    FOREIGN KEY (admin_id) REFERENCES users(id)
);

🔟 Rate limiting table (OTP / login abuse protection)
CREATE TABLE rate_limits (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    identifier VARCHAR(100),
    action VARCHAR(50),
    attempts INT,
    last_attempt DATETIME(6)
);

✅ FINAL COPILOT SUMMARY (ONE BLOCK)
Remaining improvements:
- Remove plaintext OTP, store hashed OTP + expiry
- Remove derived column attempt_answers.is_correct
- Add negative marking support to questions
- Restrict or version multiple exam attempts
- Add exam availability window (from / until)
- Add soft delete (deleted_at) to core tables
- Change exams.access_tier to ENUM
- (Optional) Add results snapshot table
- (Optional) Add admin audit logs
- (Optional) Add rate-limit tracking