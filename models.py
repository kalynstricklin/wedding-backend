
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from database import Base

# Database Model
class RSVP(Base):
    __tablename__ = "rsvps"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, description= Column(String))
    last_name = Column(String, index=True, description= Column(String))
    email = Column(String, index=True, description= Column(String))
    address = Column(String, index=True, description= Column(String))
    is_attending = Column(Boolean, index=True, description= Column(Boolean))
    dietary_restrictions = Column(String, index=True, description= Column(String))
    message = Column(Text, index=True, default="")



class RSVPRequest:
    def __init__(self, first_name, last_name, email, address, is_attending, dietary_restrictions, message):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.is_attending = is_attending
        self.dietary_restrictions = dietary_restrictions
        self.message = message


