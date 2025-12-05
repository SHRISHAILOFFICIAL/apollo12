"""
Test exam start with timer creation - Full flow
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Test, Attempt
from api.redis_utils import create_timer, get_remaining_time, timer_manager
from django.utils import timezone

User = get_user_model()

print("=" * 60)
print("TESTING EXAM START WITH TIMER")
print("=" * 60)

# Get a user and exam
user = User.objects.first()
exam = Test.objects.filter(is_published=True).first()

if not user:
    print("❌ No users found. Create a user first.")
    sys.exit(1)

if not exam:
    print("❌ No published exams found.")
    print("Creating a test exam...")
    exam = Test.objects.create(
        title="Test Exam",
        description="Test exam for timer",
        duration=60,  # 60 minutes
        total_marks=100,
        is_published=True
    )
    print(f"✅ Created exam: {exam.title}")

print(f"\nUser: {user.username} (ID: {user.id})")
print(f"Exam: {exam.title} (ID: {exam.id})")
print(f"Duration: {exam.duration} minutes ({exam.duration * 60} seconds)")

# Create attempt
print("\n" + "-" * 60)
print("Creating Attempt in MySQL...")
attempt = Attempt.objects.create(
    user=user,
    test=exam,
    status='ongoing',
    created_at=timezone.now()
)
print(f"✅ Created attempt ID: {attempt.id}")

# Create Redis timer
print("\n" + "-" * 60)
print("Creating Redis timer...")
duration_seconds = exam.duration * 60
success = create_timer(attempt.id, duration_seconds)

if success:
    print(f"✅ Timer created successfully!")
    print(f"   Key: exam:timer:{attempt.id}")
    print(f"   Duration: {duration_seconds}s")
else:
    print("❌ Timer creation FAILED!")
    sys.exit(1)

# Check timer
print("\n" + "-" * 60)
print("Checking timer...")
remaining = get_remaining_time(attempt.id)
print(f"Remaining time: {remaining}s")

if remaining > 0:
    print("✅ Timer is active!")
else:
    print(f"❌ Timer check failed! TTL: {remaining}")
    sys.exit(1)

# Verify in Redis directly
print("\n" + "-" * 60)
print("Verifying in Redis...")
redis = timer_manager.redis
key = f"exam:timer:{attempt.id}"
ttl = redis.ttl(key)
value = redis.get(key)
print(f"Redis TTL: {ttl}s")
print(f"Redis Value: {value}")

# List all timer keys
print("\n" + "-" * 60)
print("All exam timer keys in Redis:")
timer_keys = redis.keys("exam:timer:*")
print(f"Found {len(timer_keys)} timer(s):")
for key in timer_keys:
    ttl = redis.ttl(key)
    value = redis.get(key)
    print(f"  - {key.decode() if isinstance(key, bytes) else key}")
    print(f"    TTL: {ttl}s, Value: {value}")

print("\n" + "=" * 60)
print("✅ SUCCESS! Timer system working correctly!")
print("=" * 60)
print(f"\nAttempt ID: {attempt.id}")
print(f"To check in WSL Redis:")
print(f"  redis-cli")
print(f"  SELECT 1")
print(f"  KEYS exam:timer:*")
print(f"  TTL exam:timer:{attempt.id}")
print(f"  GET exam:timer:{attempt.id}")
