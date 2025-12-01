"""
Quick Redis connection test
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django_redis import get_redis_connection

print("=" * 60)
print("TESTING REDIS CONNECTION")
print("=" * 60)

try:
    # Get Redis connection
    redis = get_redis_connection("default")
    print("✅ Got Redis connection object")
    
    # Test basic operations
    print("\n1. Testing basic SET/GET...")
    redis.set("test_key", "hello_redis")
    result = redis.get("test_key")
    print(f"   Set 'test_key' = 'hello_redis'")
    print(f"   Got back: {result}")
    
    if result == b'hello_redis' or result == 'hello_redis':
        print("   ✅ Basic operations work!")
    else:
        print(f"   ❌ Unexpected result: {result}")
    
    # Test SETEX (what we use for timers)
    print("\n2. Testing SETEX (with TTL)...")
    redis.setex("timer_test", 30, 30)
    ttl = redis.ttl("timer_test")
    print(f"   Created 'timer_test' with 30s TTL")
    print(f"   TTL: {ttl}s")
    
    if ttl > 0 and ttl <= 30:
        print("   ✅ SETEX works!")
    else:
        print(f"   ❌ Unexpected TTL: {ttl}")
    
    # Test exam timer key format
    print("\n3. Testing exam timer key format...")
    test_attempt_id = 999
    key = f"exam:timer:{test_attempt_id}"
    redis.setex(key, 60, 60)
    ttl = redis.ttl(key)
    value = redis.get(key)
    print(f"   Created '{key}' with 60s TTL")
    print(f"   TTL: {ttl}s")
    print(f"   Value: {value}")
    
    if ttl > 0:
        print("   ✅ Exam timer key creation works!")
    else:
        print(f"   ❌ Unexpected TTL: {ttl}")
    
    # Check which database we're in
    print("\n4. Checking Redis database...")
    info = redis.info()
    print(f"   Connected to: {info.get('redis_version', 'Unknown')}")
    
    # List all keys
    print("\n5. Listing all keys in current database...")
    all_keys = redis.keys("*")
    print(f"   Total keys: {len(all_keys)}")
    for key in all_keys:
        ttl = redis.ttl(key)
        print(f"   - {key} (TTL: {ttl}s)")
    
    # Clean up test keys
    print("\n6. Cleaning up test keys...")
    redis.delete("test_key", "timer_test", f"exam:timer:{test_attempt_id}")
    print("   ✅ Cleanup done")
    
    print("\n" + "=" * 60)
    print("RESULT: Redis connection is working! ✅")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 60)
    print("RESULT: Redis connection FAILED! ❌")
    print("=" * 60)
