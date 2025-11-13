from fastapi import FastAPI

from database import Base, engine
from models import RSVPRequest

# Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI()



@app.get("/")
async def root():
    return { "message": "Welcome to our wedding website API :P" }


@app.post("/rsvp")
def submit_rsvp():
    # new_rsvp = RSVPRequest()
    return print("hey")

@app.get("/rsvp")
async def list_rsvp():
    return print("hey")

@app.get("/guesta")
def list_guests():
    return print("hey")
