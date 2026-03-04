from database import SessionLocal, init_db
from models import RSVP

# Create tables if they don't exist
init_db()

guests = [
    {"first_name": "name", "last_name": "name"},
]

db = SessionLocal()
for guest in guests:
    db.add(RSVP(first_name=guest["first_name"], last_name=guest["last_name"], email="", is_attending=False))
db.commit()
db.close()

print(f"Added {len(guests)} guests to the database.")