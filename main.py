import os
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException, Query, Security, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from database import Base, engine, init_db, get_db
from models import RSVP
from schemas import RSVPResponse, RSVPCreate

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """
    Validates the API key provided in the header.
    """
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key. Check that you are passing a 'X-API-Key' in your header."
        )
    return api_key

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

# Create tables
# Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI()
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Too many requests"})

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kalynandjack.love", "https://www.kalynandjack.love"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return { "message": "Wedding API" }

# Add a rsvp
@app.post("/rsvp", response_model=RSVPResponse)
@limiter.limit("10/minute")
def submit_rsvp(request: Request, rsvp: RSVPCreate, db: Session = Depends(get_db)):
    new_rsvp = RSVP(**rsvp.dict())
    db.add(new_rsvp)
    db.commit()
    db.refresh(new_rsvp)
    return new_rsvp

# Get all rsvps
@app.get("/rsvp", response_model=List[RSVPResponse], dependencies=[Depends(get_api_key)])
async def list_rsvp(
    is_attending: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(RSVP)
    if is_attending is not None:
        query = query.filter(RSVP.is_attending == is_attending)
    return query.all()

# Lookup guest by name
@app.get("/rsvp/lookup", response_model=RSVPResponse)
@limiter.limit("20/minute")
def lookup_guest(request: Request, first_name: str, last_name: str, db: Session = Depends(get_db)):
    guest = db.query(RSVP).filter(
        RSVP.first_name.ilike(first_name),
        RSVP.last_name.ilike(last_name)
    ).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest

# Update guest RSVP
@app.put("/rsvp/{guest_id}", response_model=RSVPResponse)
@limiter.limit("10/minute")
def update_rsvp(request: Request, guest_id: int, rsvp: RSVPCreate, db: Session = Depends(get_db)):
    guest = db.query(RSVP).filter(RSVP.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    guest.email = rsvp.email
    guest.address = rsvp.address
    guest.is_attending = rsvp.is_attending
    db.commit()
    db.refresh(guest)
    return guest

# Delete guest RSVP
@app.delete("/rsvp/{guest_id}", dependencies=[Depends(get_api_key)])
def delete_rsvp(guest_id: int, db: Session = Depends(get_db)):
    guest = db.query(RSVP).filter(RSVP.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    db.delete(guest)
    db.commit()
    return {"message": "Guest deleted"}