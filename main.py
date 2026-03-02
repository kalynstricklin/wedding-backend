from typing import List
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, init_db, get_db
from models import RSVP
from schemas import RSVPResponse, RSVPCreate

# Create tables
# Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI()

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "https://kalynandjack.love", "https://www.kalynandjack.love", "https://www.kalynandjack.love"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return { "message": "Welcome to our wedding website API where we are tracking guest rsvps" }

# Add a rsvp
@app.post("/rsvp", response_model=RSVPResponse)
def submit_rsvp(rsvp: RSVPCreate, db: Session = Depends(get_db)):
    new_rsvp = RSVP(**rsvp.dict())
    db.add(new_rsvp)
    db.commit()
    db.refresh(new_rsvp)
    return new_rsvp

# Get all rsvps
@app.get("/rsvp", response_model=List[RSVPResponse])
async def list_rsvp(db: Session = Depends(get_db)):
    rsvps = db.query(RSVP).all()
    return rsvps

# Lookup guest by name
@app.get("/rsvp/lookup", response_model=RSVPResponse)
def lookup_guest(first_name: str, last_name: str, db: Session = Depends(get_db)):
    guest = db.query(RSVP).filter(
        RSVP.first_name.ilike(first_name),
        RSVP.last_name.ilike(last_name)
    ).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest

# Update guest RSVP
@app.put("/rsvp/{guest_id}", response_model=RSVPResponse)
def update_rsvp(guest_id: int, rsvp: RSVPCreate, db: Session = Depends(get_db)):
    guest = db.query(RSVP).filter(RSVP.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    guest.email = rsvp.email
    guest.address = rsvp.address
    guest.is_attending = rsvp.is_attending
    db.commit()
    db.refresh(guest)
    return guest

# can return guests that are attending by filtering by is_attending boolean

