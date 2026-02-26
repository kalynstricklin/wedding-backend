from pydantic import BaseModel, Field
from typing import List, Optional


class RSVPBase(BaseModel):
    first_name: str
    last_name: str
    address: Optional[str] = None
    email: str
    is_attending: bool



class RSVPCreate(RSVPBase):
    pass

class RSVPResponse(RSVPBase):
    id: int

    class Config:
        from_attr = True