from typing import Dict, Any, Optional, Tuple, List
from app.services.memory.booking_memory import BookingMemory
from app.repositories.booking_repository import BookingRepository
from app.services.booking.booking_validator import BookingValidator
from app.services.booking.booking_extraction import BookingExtractor
from app.api.core.logger import get_logger

logger = get_logger(__name__)


class BookingService:
    """Orchestrates multi-turn booking workflow with LLM extraction and validation."""

    def __init__(self, llm) -> None:
        self.extractor: BookingExtractor = BookingExtractor(llm)
        self.validator: BookingValidator = BookingValidator()
        self.repo: BookingRepository = BookingRepository()
        self.memory: BookingMemory = BookingMemory()

    def process(self, message: str, session_id: str) -> Optional[Dict[str, Any]]:
        """Process booking message and manage state across turns.

        Args:
            message: User message
            session_id: Session identifier for multi-turn context

        Returns:
            Dict with type (booking_incomplete/booking_confirmed/error) or None
        """
        logger.debug(f"Processing booking message for session {session_id}")

        # Check if there's existing booking data (continuation)
        existing_data: Dict[str, Any] = self.memory.get(session_id) or {}
        is_continuation: bool = bool(existing_data)
        logger.debug(f"Is continuation: {is_continuation}")

        # Extract new data from message
        new_data: Dict[str, Any] = self.extractor.extract(
            message, is_continuation=is_continuation
        )
        if not new_data:
            logger.debug("No data extracted from message")
            return None

        # Check if this is a booking-related message
        is_booking: bool = new_data.pop("is_booking", False)

        if not is_booking and not is_continuation:
            logger.debug("Message not booking-related and no continuation context")
            return None

        # Merge with previous data in Redis
        full_data: Dict[str, Any] = self.memory.update(session_id, new_data)
        logger.debug(f"Merged data: {full_data}")

        # Validate completeness
        valid: bool
        missing: List[str]
        valid, missing = self.validator.validate(full_data)

        if not valid:
            logger.info("Booking incomplete")
            return {
                "type": "booking_incomplete",
                "missing_fields": missing,
                "current_data": full_data,
                "message": f"Please provide: {', '.join(missing)}",
            }

        # Save confirmed booking to database
        try:
            logger.info("Saving booking")
            self.repo.save(full_data)
        except Exception as e:
            logger.error(f"Failed to save booking: {e}", exc_info=True)
            return {"type": "error", "message": "Failed to save booking"}

        # Clear memory after success
        self.memory.clear(session_id)
        logger.info("Booking confirmed")

        return {"type": "booking_confirmed", "data": full_data}
