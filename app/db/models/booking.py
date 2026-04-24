# app/db/models/booking.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.session import Base


class Booking(Base):
    """
    Stores interview booking information.
    """

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    email = Column(String, nullable=False)

    date = Column(String, nullable=False)
    time = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
