# app/repositories/booking_repository.py

from typing import Dict, Any, List
from app.db.session import SessionLocal
from app.db.models.booking import Booking
from app.api.core.logger import get_logger

logger = get_logger(__name__)


class BookingRepository:
    """Database persistence layer for booking data."""

    REQUIRED_FIELDS: List[str] = ["name", "email", "date", "time"]

    def save(self, data: Dict[str, Any]) -> int:
        """Save booking to PostgreSQL database.

        Args:
            data: Booking data dict with name, email, date, time

        Returns:
            Booking ID from database

        Raises:
            ValueError: If required fields are missing
        """
        logger.info("Saving booking")

        # Validate all required fields are present
        missing: List[str] = [f for f in self.REQUIRED_FIELDS if not data.get(f)]

        if missing:
            error_msg: str = f"Cannot save: Missing required fields: {missing}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        db = SessionLocal()

        try:
            booking: Booking = Booking(
                name=data.get("name"),
                email=data.get("email"),
                date=data.get("date"),
                time=data.get("time"),
            )

            logger.debug(f"Created Booking object: {booking}")
            db.add(booking)
            db.commit()
            db.refresh(booking)

            logger.info("Booking saved")
            return booking.id

        except Exception as e:
            logger.error(f"Error saving booking: {e}")
            db.rollback()
            raise
        finally:
            db.close()
