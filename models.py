from sqlalchemy import create_engine, Column, Integer, DateTime, String, Boolean, Text
from database import Base
from datetime import datetime

class BaseModel():
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

class RSVP(Base):
    __tablename__ = "rsvps"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=True)
    is_attending = Column(Boolean, default=False)
    dietary_restrictions = Column(String, nullable=True)
    message = Column(Text, index=True, default="")

