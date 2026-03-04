from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class RSVPBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    address: Optional[str] = Field(None, max_length=500)
    email: EmailStr
    is_attending: bool



class RSVPCreate(RSVPBase):
    pass

class RSVPResponse(RSVPBase):
    id: int

    class Config:
        from_attributes = True