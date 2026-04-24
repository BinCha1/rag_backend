from typing import Optional
import redis
from app.api.core.logger import get_logger

logger = get_logger(__name__)


class RedisClient:
    """Redis client wrapper for session state management."""

    def __init__(self) -> None:
        """Initialize Redis connection with error handling."""
        try:
            self.client: Optional[redis.Redis] = redis.Redis(
                host="localhost",
                port=6379,
                decode_responses=True,
                socket_connect_timeout=2,
            )
            # Test connection
            self.client.ping()
            logger.info("Redis connection successful")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            self.client = None

    def set(self, key: str, value: str) -> None:
        """Set value in Redis.

        Args:
            key: Redis key
            value: Value to store

        Raises:
            Exception: If Redis operation fails
        """
        try:
            if self.client:
                self.client.set(key, value)
                logger.debug(f"Redis SET: {key}")
        except Exception as e:
            logger.error(f"Redis SET error: {e}")
            raise

    def get(self, key):
        try:
            if self.client:
                return self.client.get(key)
            return None
        except Exception as e:
            logger.error(f" Redis GET error: {e}")
            return None

    def delete(self, key):
        try:
            if self.client:
                self.client.delete(key)
        except Exception as e:
            logger.error(f" Redis DELETE error: {e}")
