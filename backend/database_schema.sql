-- ============================================================================
-- DCET Platform - Complete Database Schema (Final Version)
-- ============================================================================
-- Generated: 2025-12-20
-- Database: MySQL 8.0+
-- Description: Complete SQL schema for the DCET EdTech platform
-- 
-- IMPROVEMENTS IMPLEMENTED:
-- ✅ Removed duplicated subscription state (user_tier, is_paid)
-- ✅ Added exam availability window (available_from, available_until)
-- ✅ Added attempt restrictions (attempt_number with unique constraint)
-- ✅ Removed derived is_correct field (computed dynamically)
-- ✅ Added performance indexes for leaderboards and analytics
-- ============================================================================

-- ============================================================================
-- USER MANAGEMENT TABLES
-- ============================================================================

-- Users table - Core authentication
CREATE TABLE `users` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(100) NOT NULL UNIQUE,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `phone` VARCHAR(20) NULL,
    `password_hash` VARCHAR(255) NOT NULL,
    `email_verified` BOOLEAN NOT NULL DEFAULT FALSE,
    `is_staff` BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Admin/staff access',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    
    INDEX `idx_username` (`username`),
    INDEX `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User authentication - tier computed from subscriptions table';

-- User profiles (simplified)
CREATE TABLE `profiles` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL UNIQUE,
    
    INDEX `idx_user_id` (`user_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User profile - ready for avatar, bio, preferences';

-- Email OTP verification
CREATE TABLE `email_otps` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(254) NOT NULL,
    `otp` VARCHAR(6) NOT NULL,
    `purpose` VARCHAR(20) NOT NULL DEFAULT 'signup',
    `is_verified` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX `idx_email` (`email`),
    INDEX `idx_created_at` (`created_at`),
    INDEX `idx_email_created` (`email`, `created_at`),
    INDEX `idx_email_purpose_verified` (`email`, `purpose`, `is_verified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Password reset requests
CREATE TABLE `password_reset_requests` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `reset_token` VARCHAR(255) NOT NULL,
    `expires_at` DATETIME(6) NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX `idx_user_id` (`user_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- User activity log
CREATE TABLE `user_activity` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `activity` VARCHAR(255) NOT NULL,
    `ip_address` VARCHAR(50) NULL,
    `user_agent` TEXT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_user_created` (`user_id`, `created_at` DESC),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- User notifications
CREATE TABLE `notifications` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `message` TEXT NOT NULL,
    `is_read` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_created_at` (`created_at`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- EXAM AND QUESTION TABLES
-- ============================================================================

-- Exams/Mock Tests
CREATE TABLE `exams` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `year` INT NOT NULL,
    `total_marks` INT NOT NULL DEFAULT 0,
    `duration_minutes` INT NOT NULL,
    `solution_video_url` VARCHAR(200) NULL,
    `access_tier` VARCHAR(10) NOT NULL DEFAULT 'PRO',
    `is_published` BOOLEAN NOT NULL DEFAULT FALSE,
    `available_from` DATETIME(6) NULL COMMENT 'Exam available from this time',
    `available_until` DATETIME(6) NULL COMMENT 'Exam available until this time',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    
    INDEX `idx_is_published` (`is_published`),
    INDEX `idx_year` (`year`),
    INDEX `idx_access_tier` (`access_tier`),
    CHECK (`access_tier` IN ('FREE', 'PRO'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Exam metadata with availability window';

-- Sections within exams
CREATE TABLE `sections` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `exam_id` BIGINT NOT NULL,
    `name` VARCHAR(200) NOT NULL,
    `order` INT NOT NULL,
    `max_marks` INT NOT NULL DEFAULT 20,
    
    INDEX `idx_exam_id` (`exam_id`),
    INDEX `idx_exam_order` (`exam_id`, `order`),
    UNIQUE KEY `unique_exam_order` (`exam_id`, `order`),
    FOREIGN KEY (`exam_id`) REFERENCES `exams`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Questions
CREATE TABLE `questions` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `section_id` BIGINT NOT NULL,
    `question_number` INT NOT NULL,
    `question_text` TEXT NOT NULL,
    `plain_text` TEXT NULL,
    `option_a` VARCHAR(500) NOT NULL,
    `option_b` VARCHAR(500) NOT NULL,
    `option_c` VARCHAR(500) NOT NULL,
    `option_d` VARCHAR(500) NOT NULL,
    `correct_option` VARCHAR(1) NOT NULL,
    `marks` INT NOT NULL DEFAULT 1,
    `diagram_url` VARCHAR(200) NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX `idx_section_id` (`section_id`),
    INDEX `idx_section_question` (`section_id`, `question_number`),
    UNIQUE KEY `unique_section_question` (`section_id`, `question_number`),
    FOREIGN KEY (`section_id`) REFERENCES `sections`(`id`) ON DELETE CASCADE,
    CHECK (`correct_option` IN ('A', 'B', 'C', 'D'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- EXAM ATTEMPTS AND RESULTS TABLES
-- ============================================================================

-- Exam attempts (with attempt versioning)
CREATE TABLE `attempts` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `exam_id` BIGINT NOT NULL,
    `attempt_number` INT NOT NULL DEFAULT 1 COMMENT 'Attempt number for this user-exam',
    `started_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `finished_at` DATETIME(6) NULL,
    `score` INT NOT NULL DEFAULT 0,
    `status` VARCHAR(15) NOT NULL DEFAULT 'in_progress',
    `randomized_order` JSON NULL,
    
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_exam_id` (`exam_id`),
    INDEX `idx_user_exam` (`user_id`, `exam_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_exam_score` (`exam_id`, `score` DESC, `finished_at`),
    INDEX `idx_user_exam_attempt` (`user_id`, `exam_id`, `attempt_number`),
    UNIQUE KEY `unique_user_exam_attempt` (`user_id`, `exam_id`, `attempt_number`),
    
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`exam_id`) REFERENCES `exams`(`id`) ON DELETE CASCADE,
    CHECK (`status` IN ('in_progress', 'submitted', 'timeout'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User exam attempts with versioning support';

-- Attempt answers (is_correct computed dynamically)
CREATE TABLE `attempt_answers` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `attempt_id` BIGINT NOT NULL,
    `question_id` BIGINT NOT NULL,
    `selected_option` VARCHAR(1) NULL,
    
    INDEX `idx_attempt_id` (`attempt_id`),
    INDEX `idx_question_id` (`question_id`),
    INDEX `idx_attempt_question` (`attempt_id`, `question_id`),
    UNIQUE KEY `unique_attempt_question` (`attempt_id`, `question_id`),
    
    FOREIGN KEY (`attempt_id`) REFERENCES `attempts`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`question_id`) REFERENCES `questions`(`id`) ON DELETE CASCADE,
    CHECK (`selected_option` IN ('A', 'B', 'C', 'D') OR `selected_option` IS NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Question answers - correctness computed as: selected_option = questions.correct_option';

-- Question issues
CREATE TABLE `question_issues` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `question_id` BIGINT NOT NULL,
    `attempt_id` BIGINT NULL,
    `issue_type` VARCHAR(20) NOT NULL,
    `description` TEXT NULL,
    `status` VARCHAR(15) NOT NULL DEFAULT 'pending',
    `admin_notes` TEXT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_question_id` (`question_id`),
    INDEX `idx_question_status` (`question_id`, `status`),
    INDEX `idx_user_created` (`user_id`, `created_at`),
    INDEX `idx_status` (`status`),
    
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`question_id`) REFERENCES `questions`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`attempt_id`) REFERENCES `attempts`(`id`) ON DELETE SET NULL,
    CHECK (`issue_type` IN ('wrong_answer', 'latex_format', 'unclear_question', 'typo', 'other')),
    CHECK (`status` IN ('pending', 'resolved', 'dismissed'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- PAYMENT AND SUBSCRIPTION TABLES
-- ============================================================================

-- Subscription plans
CREATE TABLE `plans` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `key` VARCHAR(50) NOT NULL UNIQUE,
    `name` VARCHAR(100) NOT NULL,
    `price_in_paisa` INT NOT NULL,
    `duration_days` INT NOT NULL,
    `features` JSON NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX `idx_key` (`key`),
    INDEX `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Payment transactions
CREATE TABLE `payments` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `provider` VARCHAR(50) NOT NULL DEFAULT 'razorpay',
    `provider_payment_id` VARCHAR(255) NOT NULL UNIQUE,
    `order_id` VARCHAR(255) NOT NULL,
    `amount` INT NOT NULL,
    `currency` VARCHAR(10) NOT NULL DEFAULT 'INR',
    `status` VARCHAR(20) NOT NULL DEFAULT 'created',
    `metadata` JSON NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_user_status` (`user_id`, `status`),
    INDEX `idx_provider_payment_id` (`provider_payment_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_created_status` (`created_at`, `status`),
    INDEX `idx_user_created` (`user_id`, `created_at` DESC),
    
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    CHECK (`status` IN ('created', 'paid', 'activated', 'failed', 'refunded'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Subscriptions (SINGLE SOURCE OF TRUTH for user tier)
CREATE TABLE `subscriptions` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `plan_id` BIGINT NOT NULL,
    `payment_id` BIGINT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'active',
    `start_date` DATETIME(6) NOT NULL,
    `end_date` DATETIME(6) NOT NULL,
    `auto_renew` BOOLEAN NOT NULL DEFAULT FALSE,
    `cancelled_at` DATETIME(6) NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_plan_id` (`plan_id`),
    INDEX `idx_user_status` (`user_id`, `status`),
    INDEX `idx_end_date` (`end_date`),
    INDEX `idx_status_end_date` (`status`, `end_date`),
    INDEX `idx_active_subs` (`user_id`, `status`, `end_date`),
    
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`plan_id`) REFERENCES `plans`(`id`) ON DELETE PROTECT,
    FOREIGN KEY (`payment_id`) REFERENCES `payments`(`id`) ON DELETE SET NULL,
    CHECK (`status` IN ('active', 'expired', 'cancelled'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User tier: PRO if active subscription exists (status=active AND end_date>NOW), else FREE';

-- ============================================================================
-- ADMIN TABLES
-- ============================================================================

-- Global settings
CREATE TABLE `app_settings` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `setting_key` VARCHAR(100) NOT NULL UNIQUE,
    `setting_value` TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- DJANGO FRAMEWORK TABLES
-- ============================================================================

CREATE TABLE `django_migrations` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `app` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `applied` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `django_content_type` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `app_label` VARCHAR(100) NOT NULL,
    `model` VARCHAR(100) NOT NULL,
    UNIQUE KEY `django_content_type_app_label_model` (`app_label`, `model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `django_session` (
    `session_key` VARCHAR(40) PRIMARY KEY,
    `session_data` LONGTEXT NOT NULL,
    `expire_date` DATETIME(6) NOT NULL,
    INDEX `django_session_expire_date` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- KEY DESIGN DECISIONS
-- ============================================================================
--
-- ✅ SINGLE SOURCE OF TRUTH
-- - User tier computed from subscriptions table only
-- - No duplicated user_tier, is_paid fields
-- - Prevents data inconsistency
--
-- ✅ COMPUTED CORRECTNESS
-- - is_correct removed from attempt_answers
-- - Computed as: selected_option = questions.correct_option
-- - Prevents bugs when questions are corrected
--
-- ✅ ATTEMPT VERSIONING
-- - attempt_number allows multiple attempts per exam
-- - Unique constraint: (user_id, exam_id, attempt_number)
-- - Can restrict to single attempt by setting max_attempts=1 in business logic
--
-- ✅ EXAM SCHEDULING
-- - available_from and available_until for time-based access
-- - is_available computed in Django as property
--
-- ✅ PERFORMANCE INDEXES
-- - Leaderboard: idx_exam_score on attempts
-- - User history: idx_user_created on payments, user_activity
-- - Active subscriptions: idx_active_subs for fast tier lookups
--
-- ============================================================================
