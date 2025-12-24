"""
Quick script to test Redis caching
Run this to verify cache is working
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.cache import cache
import time

print("=" * 50)
print("REDIS CACHE TEST")
print("=" * 50)

# Test 1: Basic cache
print("\n1. Testing basic cache operations...")
cache.set('test_key', 'Hello from Redis!', 60)
result = cache.get('test_key')
print(f"   Set: 'test_key' = 'Hello from Redis!'")
print(f"   Get: {result}")
print(f"   ✅ Basic cache: {'WORKING' if result else 'FAILED'}")

# Test 2: Cache with prefix
print("\n2. Testing cache with apollo11 prefix...")
cache.set('apollo11:test', 'Prefixed value', 60)
result = cache.get('apollo11:test')
print(f"   Set: 'apollo11:test' = 'Prefixed value'")
print(f"   Get: {result}")
print(f"   ✅ Prefixed cache: {'WORKING' if result else 'FAILED'}")

# Test 3: Check cache backend
print("\n3. Cache backend info...")
from django.conf import settings
cache_config = settings.CACHES['default']
print(f"   Backend: {cache_config['BACKEND']}")
print(f"   Location: {cache_config['LOCATION']}")

print("\n" + "=" * 50)
print("Now check Redis CLI:")
print("  wsl")
print("  redis-cli -n 1  # Note: -n 1 for database 1")
print("  KEYS *")
print("=" * 50)
