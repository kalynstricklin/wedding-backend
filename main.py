from typing import List
from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import Base, engine, init_db, get_db
from models import RSVP
from schemas import RSVPResponse, RSVPCreate

# Create tables
# Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI()



@app.get("/")
async def root():
    return { "message": "Welcome to our wedding website API :P" }

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


# can return guests that are attending by filtering by is_attending boolean
