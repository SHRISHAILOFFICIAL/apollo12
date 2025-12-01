"""
Redis utility functions for exam timer management.

Purpose: Handle exam countdown timers using Redis with automatic expiration.
- Redis stores ONLY timers (temporary data)
- MySQL stores all permanent exam attempt data
- TTL determines when an exam has timed out
"""

from django_redis import get_redis_connection
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class RedisTimerManager:
    """Manages exam timers in Redis with automatic expiration."""
    
    def __init__(self):
        """Initialize Redis connection."""
        self.redis = get_redis_connection("default")
    
    @staticmethod
    def _get_key(attempt_id: int) -> str:
        """
        Generate Redis key for exam timer.
        
        Args:
            attempt_id: ExamAttempt ID from MySQL
            
        Returns:
            Redis key in format: exam:timer:{attempt_id}
        """
        return f"exam:timer:{attempt_id}"
    
    def create_timer(self, attempt_id: int, duration_seconds: int) -> bool:
        """
        Create a new exam timer in Redis with automatic expiration.
        
        Args:
            attempt_id: ExamAttempt ID from MySQL
            duration_seconds: Exam duration in seconds
            
        Returns:
            True if timer created successfully, False otherwise
            
        Example:
            >>> manager = RedisTimerManager()
            >>> manager.create_timer(attempt_id=42, duration_seconds=3600)
            True
        """
        try:
            key = self._get_key(attempt_id)
            # Set the remaining time and TTL
            # SETEX atomically sets value and expiration
            self.redis.setex(key, duration_seconds, duration_seconds)
            logger.info(f"Created timer for attempt {attempt_id} with {duration_seconds}s duration")
            return True
        except Exception as e:
            logger.error(f"Failed to create timer for attempt {attempt_id}: {str(e)}")
            return False
    
    def get_remaining_time(self, attempt_id: int) -> int:
        """
        Get remaining time for an exam attempt.
        
        Args:
            attempt_id: ExamAttempt ID from MySQL
            
        Returns:
            Remaining seconds (>= 0) if timer exists
            -2 if timer has expired or doesn't exist (key missing)
            -1 if key exists but has no TTL (should never happen)
            
        Example:
            >>> manager = RedisTimerManager()
            >>> manager.get_remaining_time(42)
            2847  # 47 minutes 27 seconds remaining
        """
        try:
            key = self._get_key(attempt_id)
            # TTL returns:
            # -2 if key doesn't exist (expired or never created)
            # -1 if key exists but has no expiration
            # >= 0 if key exists with remaining TTL in seconds
            ttl = self.redis.ttl(key)
            
            if ttl == -2:
                logger.warning(f"Timer for attempt {attempt_id} not found (expired or missing)")
            elif ttl == -1:
                logger.error(f"Timer for attempt {attempt_id} exists but has no TTL (data corruption)")
            
            return ttl
        except Exception as e:
            logger.error(f"Failed to get remaining time for attempt {attempt_id}: {str(e)}")
            return -2  # Treat errors as expired
    
    def delete_timer(self, attempt_id: int) -> bool:
        """
        Delete an exam timer from Redis.
        Called when exam is submitted before timeout.
        
        Args:
            attempt_id: ExamAttempt ID from MySQL
            
        Returns:
            True if timer was deleted, False if it didn't exist
            
        Example:
            >>> manager = RedisTimerManager()
            >>> manager.delete_timer(42)
            True
        """
        try:
            key = self._get_key(attempt_id)
            deleted = self.redis.delete(key)
            
            if deleted:
                logger.info(f"Deleted timer for attempt {attempt_id}")
                return True
            else:
                logger.warning(f"Timer for attempt {attempt_id} not found (already expired or deleted)")
                return False
        except Exception as e:
            logger.error(f"Failed to delete timer for attempt {attempt_id}: {str(e)}")
            return False
    
    def is_expired(self, attempt_id: int) -> bool:
        """
        Check if an exam timer has expired.
        
        Args:
            attempt_id: ExamAttempt ID from MySQL
            
        Returns:
            True if timer has expired or doesn't exist, False if still running
            
        Example:
            >>> manager = RedisTimerManager()
            >>> manager.is_expired(42)
            False  # Exam still in progress
        """
        ttl = self.get_remaining_time(attempt_id)
        return ttl == -2  # Key doesn't exist = expired
    
    def extend_timer(self, attempt_id: int, additional_seconds: int) -> bool:
        """
        Extend an existing exam timer (e.g., for special accommodations).
        
        Args:
            attempt_id: ExamAttempt ID from MySQL
            additional_seconds: Additional time to add in seconds
            
        Returns:
            True if timer was extended, False if timer doesn't exist
            
        Example:
            >>> manager = RedisTimerManager()
            >>> manager.extend_timer(attempt_id=42, additional_seconds=600)  # Add 10 minutes
            True
        """
        try:
            key = self._get_key(attempt_id)
            current_ttl = self.redis.ttl(key)
            
            if current_ttl <= 0:
                logger.warning(f"Cannot extend timer for attempt {attempt_id} - timer expired or missing")
                return False
            
            new_ttl = current_ttl + additional_seconds
            # Update TTL
            self.redis.expire(key, new_ttl)
            logger.info(f"Extended timer for attempt {attempt_id} by {additional_seconds}s (new TTL: {new_ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Failed to extend timer for attempt {attempt_id}: {str(e)}")
            return False


# Singleton instance for convenient imports
timer_manager = RedisTimerManager()


# Convenience functions for backward compatibility
def create_timer(attempt_id: int, duration_seconds: int) -> bool:
    """Create exam timer. See RedisTimerManager.create_timer for details."""
    return timer_manager.create_timer(attempt_id, duration_seconds)


def get_remaining_time(attempt_id: int) -> int:
    """Get remaining time. See RedisTimerManager.get_remaining_time for details."""
    return timer_manager.get_remaining_time(attempt_id)


def delete_timer(attempt_id: int) -> bool:
    """Delete exam timer. See RedisTimerManager.delete_timer for details."""
    return timer_manager.delete_timer(attempt_id)


def is_expired(attempt_id: int) -> bool:
    """Check if timer expired. See RedisTimerManager.is_expired for details."""
    return timer_manager.is_expired(attempt_id)
