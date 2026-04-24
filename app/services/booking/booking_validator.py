from typing import Tuple, List, Dict, Any


class BookingValidator:
    """Validates booking data against required fields."""

    REQUIRED_FIELDS: List[str] = ["name", "email", "date", "time"]

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Check if all required booking fields are present.

        Args:
            data: Booking data dictionary

        Returns:
            Tuple of (is_valid: bool, missing_fields: List[str])
        """
        missing: List[str] = []

        for field in self.REQUIRED_FIELDS:
            if not data.get(field):
                missing.append(field)

        return len(missing) == 0, missing
