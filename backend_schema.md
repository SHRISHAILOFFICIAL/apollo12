🧱 DCET EXAM PLATFORM – BACKEND SCHEMA & SYSTEM SPECIFICATION
1. Overview
Build a complete backend system for an online DCET exam platform using Django REST Framework + MySQL.
The system must support:
•	Multiple exams (DCET 2023, DCET 2024, Mock Tests, etc.)
•	Multiple sections per exam
•	Multiple questions per section
•	LaTeX-based math questions
•	Paid/unpaid user access
•	Subscriptions & plan-based payments
•	Exam attempts, scoring, analytics
•	Automatic section creation during CSV import
•	Fully scalable for future QPs
Each question has one single correct answer.
________________________________________
2. Users & Authentication
2.1 User
A custom user model with fields:
•	id (PK)
•	username (unique)
•	full_name   
•	email (unique)
•	phone
•	password_hash (Django default hashing)
•	email_verified (boolean)
•	created_at
•	updated_at
Use JWT (access + refresh) for authentication.

2.2 Profile
One-to-one with User.
Stores subscription/payment status.
Fields:
•	id (PK)
•	user_id (FK → User)
•	is_paid (boolean)
•	plan_id (FK → Plan)
•	subscription_start (datetime)
•	subscription_end (datetime)
Business Rule:
User is considered paid if subscription_end > NOW().
________________________________________
3. Payment System
3.1 Plan
Subscription products.
Fields:
•	id (PK)
•	key (e.g., “monthly”, “yearly”)
•	name
•	price_in_paisa
•	duration_days

3.2 Payment
Stores transactions.
Fields:
•	id (PK)
•	user_id (FK → User)
•	provider (e.g., "razorpay")
•	provider_payment_id (unique)
•	order_id
•	amount
•	currency
•	status (created, paid, failed, refunded)
•	metadata (JSON)
•	created_at
•	updated_at
Webhook Behavior:
When status becomes paid, update user’s subscription.
________________________________________
4. DCET Exam Structure (Official)
According to the syllabus:
Sl	Section Name	Marks
1	ENGINEERING MATHEMATICS	20
2	STATISTICS & ANALYTICS	20
3	IT SKILLS	20
4	FUNDAMENTALS OF ELECTRICAL & ELECTRONICS ENGINEERING	20
5	PROJECT MANAGEMENT SKILLS	20
Total: 100 marks
Duration: 3 hours
Each section contains exactly 20 questions (each 1 mark).
________________________________________
5. Exam Data Model
5.1 Exam
Represents each exam/QP.
•	id (PK)
•	name (e.g., “DCET”)
•	year (e.g., 2023)
•	total_marks
•	duration_minutes (is fixed 180 min or 3 hr )

5.2 Section
Each exam contains multiple sections.
•	id (PK)
•	exam_id (FK → Exam)
•	name
•	order
•	max_marks (default 20)
Sections should be autocreated during CSV import if missing.

5.3 Question
Each section contains multiple questions.
Fields:
•	id (PK)
•	section_id (FK → Section)
•	question_number (1–20)
•	question_text (supports LaTeX)
•	plain_text (optional)
•	option_a
•	option_b
•	option_c
•	option_d
•	correct_option (A/B/C/D)
•	marks (default 1)
•	diagram_url (optional)
Unique: (section_id, question_number)
________________________________________
6. Exam Attempts System
6.1 Attempt
Represents a user’s exam session.
Fields:
•	id (PK)
•	user_id (FK → User)
•	exam_id (FK → Exam)
•	started_at
•	finished_at
•	score
•	randomized_order (JSON array, optional)
6.2 AttemptAnswer
Store answers for each question in attempt.
•	id (PK)
•	attempt_id (FK → Attempt)
•	question_id (FK → Question)
•	selected_option
•	is_correct (boolean)
Unique: (attempt_id, question_id)
________________________________________
7. CSV Import System
7.1 CSV Format
CSV columns:
section_name
question_number
question_text
plain_text
option_a
option_b
option_c
option_d
correct_option
marks
diagram_url
Must be UTF-8.

7.2 Import Behavior
When importing:
•	Auto-create exam if missing
•	Auto-create sections if missing
•	Auto-number questions correctly
•	Insert questions and options
•	Set correct_option
•	Validate fields
•	Report errors
________________________________________
8. Required Functions / Triggers / Procedures
8.1 Trigger: Auto-expire Subscriptions
Runs daily:
•	If subscription_end < NOW(), set is_paid = FALSE.
8.2 Trigger: Activate Subscription on Payment
When Payment.status = "paid":
1.	Fetch plan duration
2.	Set subscription_start = NOW()
3.	Set subscription_end = NOW() + duration_days
4.	Set is_paid = TRUE
8.3 Procedure: calculate_attempt_score(attempt_id)
Process:
•	Compare selected_option with correct_option
•	Mark is_correct
•	Sum marks
•	Save score in Attempt
8.4 Procedure: import_exam_from_csv(csv_path, exam_id)
Steps:
•	Parse CSV
•	For each row, create section if not found
•	Insert question
•	Validate correct_option
•	Log errors
________________________________________
9. Indexing Plan
Mandatory:
•	user.username (unique)
•	user.email (unique)
•	profile.user_id (unique)
•	payment.provider_payment_id (unique)
•	question.section_id + question_number (unique)
•	attempt.user_id
•	attempt.exam_id
•	attemptanswer.attempt_id
•	attemptanswer.question_id
________________________________________
10. API Requirements
Build REST endpoints for:
User & Auth:
•	Register
•	Login (JWT)
•	Email verification
•	Password reset
Payments:
•	Create order
•	Capture payment
•	Webhook (update subscription)
•	Get subscription status
Exams:
•	List exams
•	Get sections for exam
•	Get questions for exam
•	Admin: Create/update/delete exams, sections, questions
Attempts:
•	Start attempt
•	Submit answers
•	Auto-score
•	Get past attempts
•	Fetch analytics
________________________________________
11. Final Notes
•	This backend must handle any number of future DCET exams.
•	Math questions must be stored using LaTeX in question_text.
•	Frontend will render LaTeX using KaTeX or MathJax.
•	Question order shuffling should be handled in frontend or using randomized_order.
•	The system must support 100k+ users without redesigning the schema.

12. Redis Architecture & Usage Specification
Redis is used as a high-performance in-memory datastore to support real-time features, caching, security, and exam-critical operations.
The backend must integrate Redis for the following specific functionalities:
________________________________________
12.1 Exam Timer System (Primary Use Case)
Redis MUST be used to track exam timers because:
•	It supports TTL (auto-expiring keys)
•	Extremely fast read/write
•	Perfect for countdown timers
•	Survives backend restarts
Key Format
exam_timer:{attempt_id}
exam_timer:{user_id}:{exam_id}
Stored Data
JSON or simple values containing:
•	start_time
•	end_time
•	remaining_seconds
TTL
Set TTL equal to exam duration to auto-expire on exam finish.
________________________________________
12.2 Cache Layer (Performance Optimization)
Redis must be used as a caching layer for frequently accessed, rarely changing data:
•	Exam metadata
•	Sections list
•	Questions for an exam
•	Pricing plans
•	User subscription status
Recommended Cache Keys
cache:exam:{exam_id}
cache:exam:{exam_id}:sections
cache:exam:{exam_id}:questions
cache:plans
cache:user:subscription:{user_id}
Cache Expiry
•	5 to 15 minutes for exam structure
•	1 hour for plans
•	30 seconds for user subscription state
Use cache invalidation on admin updates.
________________________________________
12.3 Login Security & Token Control
Redis must support authentication workflows:
3.1 Failed login rate-limiting
auth:rate_limit:{ip}
TTL: 60 seconds
If > allowed attempts → block temporarily.
3.2 JWT Token Blacklist (Optional but recommended)
token:blacklist:{jwt_id}
TTL = token lifetime
Prevents reuse after logout.
________________________________________
12.4 Attempt Locking (Prevent Double Actions)
Redis is used to ensure that:
•	A user does not start multiple attempts simultaneously
•	Submission happens once
•	Payment webhook is not processed multiple times
Attempt lock key
attempt:lock:{user_id}:{exam_id}
Value: attempt_id
TTL: exam duration
Submission lock key
attempt:submit:lock:{attempt_id}
If key exists → reject duplicate submission.
________________________________________
12.5 Payment Processing Safety (Webhook Idempotency)
Redis ensures webhooks are processed only once.
Key Format
payment:webhook:{provider_payment_id}
If EXISTS → ignore websocket call.
TTL: 24 hours.
________________________________________
12.6 Real-time Features (Future-Friendly)
Redis should be reserved to support future features:
•	Real-time monitoring of mock exams
•	Live leaderboards
•	Active user tracking
•	Live chat or notifications
•	Fraud detection signals
These features rely on Pub/Sub or Streams:
stream:events
pubsub:notifications
leaderboard:exam:{exam_id}
________________________________________
12.7 Housekeeping (Optional Cron Tasks)
Use Redis keys for scheduling:
•	Daily subscription cleanup
•	Clearing expired locks
•	Resetting caches
•	Background scoring workflows
These can be executed via Celery + Redis or simple cron + Django management commands.
________________________________________
12.8 Redis Key Naming & Best Practices
•	Use namespaces like cache:, timer:, auth:, attempt:
•	Use TTL on ALL keys unless permanent
•	Keep keys human-readable
•	Avoid extremely large values
•	Prefer JSON values for structured data
________________________________________
12.9 Redis Failover Policy
If Redis is unavailable:
•	Exam timers should fallback to DB timestamps
•	User should still be able to continue the exam
•	Cache misses default to DB fallback
The backend must degrade gracefully.



