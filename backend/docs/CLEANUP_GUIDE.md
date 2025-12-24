# 🗑️ Files to Clean Up - Apollo11 Backend

## 📋 Recommended Files to DELETE

### 1. Old Test Files (`.old` extension) - **SAFE TO DELETE**
These are backup files from previous development:

```
✅ SAFE TO DELETE:
- add_questions.py.old
- check_users.py.old
- cleanup_attempts.py.old
- create_sample_data.py.old
- populate_db.py.old
- test_api.py.old
- test_api_timer.py.old
- test_auth_flow.py.old
- test_complete_flow.py.old
- test_exam_flow.py.old
- test_redis_connection.py.old
- test_redis_timer.py.old
- test_simple.py.old
- api/serializers_exam_timer.py.old
- api/serializers_test.py.old
```
**Total:** 15 files

### 2. Duplicate/Temporary Documentation - **REVIEW BEFORE DELETE**

```
⚠️ REVIEW THESE (may have duplicate info):
- BREVO_API_KEY_FIX.md (temporary fix guide)
- BREVO_FINAL_STEPS.md (temporary setup guide)
- ENV_FIX_GUIDE.md (temporary fix guide)
- FIX_ENV_NOW.md (temporary fix guide)
- RESTART_BACKEND.md (temporary reminder)
- SENDPULSE_SETUP.md (alternative email - not using)
- SENDPULSE_COMPLETE_GUIDE.md (alternative email - not using)
- URL_FIX.md (temporary fix guide)
```
**Reason:** These were created during troubleshooting. Main docs cover everything.

### 3. Duplicate Database Files - **KEEP ONE, DELETE OTHERS**

```
⚠️ CHOOSE ONE TO KEEP:
- dcet_platform_full_backup.sql (64 KB) ✅ KEEP THIS - Most complete
- dcet_platform_backup.sql (6 KB) ❌ DELETE - Older/smaller
- dcet_platform_schema.sql (37 KB) ❌ DELETE - Schema only, no data
```

### 4. Large Test Report - **OPTIONAL DELETE**

```
⚠️ OPTIONAL:
- Locust_2025-12-10-01h16_locustfile.py_http___localhost_8000.html (889 KB)
```
**Reason:** Old load test report. Can regenerate if needed.

### 5. Temporary Environment Files - **KEEP .env.example, DELETE OTHERS**

```
✅ KEEP:
- .env (your actual config)
- .env.example (template for others)

❌ DELETE:
- .env.brevo (temporary template)
- .env.corrected (temporary fix)
- .env.sendpulse (alternative not using)
```

### 6. Test/Debug Scripts - **REVIEW BEFORE DELETE**

```
⚠️ REVIEW:
- debug_redis.py (Redis debugging - may need later)
- simple_test.py (basic test - probably not needed)
- test_password.py (password testing - may need)
- test_redis_cache.py (Redis testing - may need)
- test_baseline.py (load testing - may need)
- reset_database.py (database reset - may need)
- setup_database.py (database setup - may need)
```

---

## 📊 Summary

| Category | Files | Recommendation |
|----------|-------|----------------|
| `.old` backup files | 15 | ✅ DELETE ALL |
| Temporary docs | 8 | ⚠️ REVIEW & DELETE |
| Duplicate DB files | 2 | ❌ DELETE 2, KEEP 1 |
| Large test report | 1 | ⚠️ OPTIONAL DELETE |
| Temp .env files | 3 | ❌ DELETE |
| Test scripts | 7 | ⚠️ REVIEW |

**Total potential cleanup:** ~30-40 files

---

## 🎯 Recommended Action Plan

### Phase 1: Safe Deletions (No Risk)
Delete all `.old` files:
```bash
# Windows PowerShell
Get-ChildItem -Recurse -Filter "*.old" | Remove-Item
```

### Phase 2: Documentation Cleanup
Keep only essential docs:
- ✅ KEEP: README.md, QUICK_SETUP.md, DATABASE_RESTORE.md, EMAIL_SETUP_GUIDE.md
- ❌ DELETE: Temporary fix guides (BREVO_API_KEY_FIX.md, etc.)

### Phase 3: Database Files
- ✅ KEEP: dcet_platform_full_backup.sql
- ❌ DELETE: dcet_platform_backup.sql, dcet_platform_schema.sql

### Phase 4: Environment Files
- ✅ KEEP: .env, .env.example
- ❌ DELETE: .env.brevo, .env.corrected, .env.sendpulse

---

## ✅ Files to DEFINITELY KEEP

**Core Application:**
- manage.py
- requirements.txt
- requirements-production.txt
- gunicorn.conf.py
- All directories (users/, exams/, results/, etc.)

**Essential Documentation:**
- README.md
- QUICK_SETUP.md
- DATABASE_RESTORE.md
- EMAIL_SETUP_GUIDE.md
- API_DOCUMENTATION.md
- AUTH_API_DOCUMENTATION.md
- QUERY_OPTIMIZATION.md

**Database & Data:**
- dcet_platform_full_backup.sql (KEEP THIS ONE)
- dcet_pyq_2023.csv

**Useful Scripts:**
- check_config.py
- test_email.py
- locustfile.py (load testing)

**Configuration:**
- .env
- .env.example

---

## 🚨 DO NOT DELETE

- Any files in app directories (users/, exams/, results/, etc.)
- manage.py
- requirements files
- gunicorn.conf.py
- dcet_platform_full_backup.sql
- .env and .env.example

---

**Would you like me to create a cleanup script to safely delete the recommended files?**
