from pydantic import BaseModel, Field
from typing import List, Optional


class RSVPBase():
    first_name: str
    last_name: str
    address: Optional[str] = None
    email: str
    is_attending: bool
    dietary_restrictions: Optional[str] = None
    message: Optional[str] = None


class RSVPCreate(RSVPBase):
    pass

class RSVPResponse(RSVPBase):
    id: int

    class Config:
        from_attr = True