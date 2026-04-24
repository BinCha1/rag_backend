import json
from typing import Dict, Any, Optional
from app.services.memory.redis_client import RedisClient
from app.api.core.logger import get_logger

logger = get_logger(__name__)


class BookingMemory:
    """Redis-backed session memory for multi-turn booking workflow."""

    def __init__(self) -> None:
        self.redis: RedisClient = RedisClient()

    def get(self, session_id: str) -> Dict[str, Any]:
        """Retrieve booking data for session.

        Args:
            session_id: Session identifier

        Returns:
            Booking data dict or empty dict if not found
        """
        try:
            data: Optional[str] = self.redis.get(session_id)
            result: Dict[str, Any] = json.loads(data) if data else {}
            logger.debug(f"Retrieved booking memory for {session_id}: {result}")
            return result
        except Exception as e:
            logger.error(f"BookingMemory.get error for {session_id}: {e}")
            return {}

    def update(self, session_id: str, new_data: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new data with existing booking data.

        Args:
            session_id: Session identifier
            new_data: New fields to merge

        Returns:
            Updated booking data

        Raises:
            Exception: If Redis operation fails
        """
        try:
            current: Dict[str, Any] = self.get(session_id)
            current.update(new_data)
            self.redis.set(session_id, json.dumps(current))
            logger.debug(f"Updated booking memory for {session_id}")
            return current
        except Exception as e:
            logger.error(f"BookingMemory.update error: {e}")
            raise

    def clear(self, session_id: str) -> None:
        """Clear booking data for session after completion.

        Args:
            session_id: Session identifier
        """
        try:
            self.redis.delete(session_id)
            logger.info("Memory cleared")
        except Exception as e:
            logger.error(f"BookingMemory.clear error: {e}")
