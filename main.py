from fastapi import FastAPI

from models import RSVPRequest

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Welcome to our wedding website API :P" }


@app.post("/rsvp")
def create_rsvp():
    # new_rsvp = RSVPRequest()
    return print("hey")

@app.get("/rsvp")
def list_rsvp():
    return print("hey")
