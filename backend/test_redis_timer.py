"""
Quick test script to verify Redis timer implementation.

This script tests:
1. Redis connection
2. Timer creation
3. TTL checking
4. Timer deletion
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.redis_utils import timer_manager
import time


def test_redis_connection():
    """Test basic Redis connection."""
    print("=" * 60)
    print("TEST 1: Redis Connection")
    print("=" * 60)
    
    try:
        # Test connection by setting and getting a test key
        timer_manager.redis.set("test_connection", "OK")
        result = timer_manager.redis.get("test_connection")
        timer_manager.redis.delete("test_connection")
        
        if result == b"OK" or result == "OK":
            print("✅ Redis connection successful!")
            return True
        else:
            print("❌ Redis connection failed - unexpected response")
            return False
    except Exception as e:
        print(f"❌ Redis connection failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check if Redis is running: redis-cli ping")
        print("2. Start Redis: redis-server")
        print("3. Check settings.py CACHES configuration")
        return False


def test_create_timer():
    """Test creating a timer."""
    print("\n" + "=" * 60)
    print("TEST 2: Create Timer")
    print("=" * 60)
    
    attempt_id = 99999  # Test attempt ID
    duration = 30  # 30 seconds for testing
    
    print(f"Creating timer for attempt {attempt_id} with {duration}s duration...")
    
    success = timer_manager.create_timer(attempt_id, duration)
    
    if success:
        print(f"✅ Timer created successfully!")
        
        # Verify it exists
        remaining = timer_manager.get_remaining_time(attempt_id)
        print(f"   Remaining time: {remaining}s")
        
        if remaining > 0 and remaining <= duration:
            print(f"✅ Timer verification passed!")
            return True
        else:
            print(f"❌ Timer verification failed - unexpected TTL: {remaining}")
            return False
    else:
        print("❌ Timer creation failed!")
        return False


def test_remaining_time():
    """Test getting remaining time."""
    print("\n" + "=" * 60)
    print("TEST 3: Get Remaining Time")
    print("=" * 60)
    
    attempt_id = 99999
    
    print("Waiting 3 seconds...")
    time.sleep(3)
    
    remaining = timer_manager.get_remaining_time(attempt_id)
    print(f"Remaining time after 3s: {remaining}s")
    
    if 25 <= remaining <= 27:  # Should be ~27s (30 - 3)
        print("✅ Remaining time check passed!")
        return True
    else:
        print(f"❌ Remaining time check failed - expected ~27s, got {remaining}s")
        return False


def test_is_expired():
    """Test checking if timer expired."""
    print("\n" + "=" * 60)
    print("TEST 4: Check Expiration")
    print("=" * 60)
    
    attempt_id = 99999
    
    is_expired = timer_manager.is_expired(attempt_id)
    print(f"Timer expired? {is_expired}")
    
    if not is_expired:
        print("✅ Expiration check passed - timer still running!")
        return True
    else:
        print("❌ Expiration check failed - timer shouldn't be expired yet")
        return False


def test_delete_timer():
    """Test deleting a timer."""
    print("\n" + "=" * 60)
    print("TEST 5: Delete Timer")
    print("=" * 60)
    
    attempt_id = 99999
    
    print(f"Deleting timer for attempt {attempt_id}...")
    success = timer_manager.delete_timer(attempt_id)
    
    if success:
        print("✅ Timer deleted successfully!")
        
        # Verify it's gone
        is_expired = timer_manager.is_expired(attempt_id)
        remaining = timer_manager.get_remaining_time(attempt_id)
        
        print(f"   Is expired? {is_expired}")
        print(f"   Remaining time: {remaining}s")
        
        if is_expired and remaining == -2:
            print("✅ Timer deletion verified!")
            return True
        else:
            print("❌ Timer deletion verification failed")
            return False
    else:
        print("❌ Timer deletion failed!")
        return False


def test_expired_timer():
    """Test auto-expiration with short TTL."""
    print("\n" + "=" * 60)
    print("TEST 6: Auto-Expiration")
    print("=" * 60)
    
    attempt_id = 88888
    duration = 5  # 5 seconds
    
    print(f"Creating timer with {duration}s duration...")
    timer_manager.create_timer(attempt_id, duration)
    
    print(f"Waiting {duration + 2} seconds for auto-expiration...")
    time.sleep(duration + 2)
    
    remaining = timer_manager.get_remaining_time(attempt_id)
    is_expired = timer_manager.is_expired(attempt_id)
    
    print(f"Remaining time: {remaining}s")
    print(f"Is expired? {is_expired}")
    
    if is_expired and remaining == -2:
        print("✅ Auto-expiration works correctly!")
        return True
    else:
        print("❌ Auto-expiration failed")
        # Clean up
        timer_manager.delete_timer(attempt_id)
        return False


def run_all_tests():
    """Run all tests."""
    print("\n")
    print("🚀 REDIS EXAM TIMER TESTS")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Connection
    results.append(("Redis Connection", test_redis_connection()))
    
    if not results[0][1]:
        print("\n❌ Cannot proceed - Redis connection failed")
        return
    
    # Test 2: Create Timer
    results.append(("Create Timer", test_create_timer()))
    
    # Test 3: Remaining Time
    results.append(("Get Remaining Time", test_remaining_time()))
    
    # Test 4: Is Expired
    results.append(("Check Expiration", test_is_expired()))
    
    # Test 5: Delete Timer
    results.append(("Delete Timer", test_delete_timer()))
    
    # Test 6: Auto-Expiration
    results.append(("Auto-Expiration", test_expired_timer()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Redis timer system is working correctly.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please check the errors above.")


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
