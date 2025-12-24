"""
Redis caching utilities for Apollo11
Provides decorators and helper functions for caching API responses
"""
from functools import wraps
from django.core.cache import cache
from django.conf import settings
import hashlib
import json


def generate_cache_key(prefix, *args, **kwargs):
    """Generate a unique cache key from prefix and arguments"""
    key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
    key_hash = hashlib.md5(key_data.encode()).hexdigest()
    return f"apollo11:{prefix}:{key_hash}"


def cache_response(timeout=3600, key_prefix="view"):
    """
    Decorator to cache view responses
    
    Args:
        timeout: Cache timeout in seconds (default: 1 hour)
        key_prefix: Prefix for cache key
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            # Generate cache key from view name, args, and query params
            cache_key = generate_cache_key(
                key_prefix,
                view_func.__name__,
                args,
                request.query_params.dict() if hasattr(request, 'query_params') else {},
                user_id=request.user.id if request.user.is_authenticated else None
            )
            
            # Try to get from cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response
            
            # Execute view and cache result
            response = view_func(self, request, *args, **kwargs)
            
            # Only cache successful responses
            if response.status_code == 200:
                cache.set(cache_key, response, timeout)
            
            return response
        return wrapper
    return decorator


def invalidate_cache(key_prefix):
    """
    Invalidate all cache keys with given prefix
    Note: This is a simple implementation. For production, consider using cache versioning.
    """
    # Django's cache doesn't support wildcard deletion by default
    # This is a placeholder - implement based on your cache backend
    pass


def cache_exam_data(exam_id, data, timeout=3600):
    """Cache exam data by exam ID"""
    cache_key = f"apollo11:exam:{exam_id}"
    cache.set(cache_key, data, timeout)


def get_cached_exam(exam_id):
    """Get cached exam data"""
    cache_key = f"apollo11:exam:{exam_id}"
    return cache.get(cache_key)


def invalidate_exam_cache(exam_id):
    """Invalidate cache for specific exam"""
    cache_key = f"apollo11:exam:{exam_id}"
    cache.delete(cache_key)
