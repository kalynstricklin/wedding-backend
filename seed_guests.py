from database import SessionLocal, init_db
from models import RSVP

# Create tables if they don't exist
init_db()

guests = [
    {"first_name": "Danielle", "last_name": "Byrne"},
    {"first_name": "Jared", "last_name": "Cross"},
    {"first_name": "Austin", "last_name": "Stricklin"},
    {"first_name": "Jorge", "last_name": "Zamora"},
    {"first_name": "Jackson", "last_name": "Harpine"},
    {"first_name": "Angela", "last_name": "Mintz"},
    {"first_name": "Bobby", "last_name": "Mintz"},
    {"first_name": "Ceci", "last_name": "Griffin"},
    {"first_name": "Eli", "last_name": "Herlevic"},
    {"first_name": "Alex", "last_name": "Almanza"},
    {"first_name": "Rowan", "last_name": "Pierce"},
    {"first_name": "Bre", "last_name": "Johnson"},
    {"first_name": "Ashleigh", "last_name": "Richardson"},
    {"first_name": "Ashley", "last_name": "Acuff"},
    {"first_name": "Abby", "last_name": "Harwell"},
    {"first_name": "Jake", "last_name": "Harwell"},
    {"first_name": "Omega", "last_name": "Jones"},
    {"first_name": "Brantley", "last_name": "Jones"},
    {"first_name": "Anthony", "last_name": "Dingler"},
    {"first_name": "Elaine", "last_name": "Jones"},
    {"first_name": "Tony", "last_name": "Jones"},
    {"first_name": "Sheri", "last_name": "Stallings"},
    {"first_name": "Andrew", "last_name": "Kercher"},
    {"first_name": "Mackenzie", "last_name": "White"},
    {"first_name": "Hayden", "last_name": "Heathcoat"},
    {"first_name": "Gracie", "last_name": "Pettus"},
    {"first_name": "Kai", "last_name": "Zhang"},
    {"first_name": "Brian", "last_name": "Niswonger"},
    {"first_name": "Alyssa", "last_name": "Shonce"},
    {"first_name": "Kaleb", "last_name": "Ruddle"},
    {"first_name": "Abby", "last_name": "Carroll"},
    {"first_name": "Casey", "last_name": "Bates"},
    {"first_name": "Joey", "last_name": "Bearden"},
    {"first_name": "Mandy", "last_name": "Hunt"},
    {"first_name": "Shawn", "last_name": "Hunt"},
    {"first_name": "Morgyn", "last_name": "Reece"},
    {"first_name": "Scottie", "last_name": "Reece"},
    {"first_name": "Will", "last_name": "Stallings"},
    {"first_name": "Melissa", "last_name": "Turner"},
    {"first_name": "Steve", "last_name": "Turner"},
    {"first_name": "Chris", "last_name": "Munoz"},
    {"first_name": "McKayla", "last_name": "Hopp"},
    {"first_name": "Madison", "last_name": "Oakman"},
    {"first_name": "Cameron", "last_name": "Stricklin"},
    {"first_name": "Valerie", "last_name": "Maxwell"},
    {"first_name": "Lot", "last_name": "Maxwell"},
    {"first_name": "Phil", "last_name": "Darden"},
    {"first_name": "Mary Lynn", "last_name": "Botts"},
    {"first_name": "Mike", "last_name": "Botts"},
    {"first_name": "Justin", "last_name": "Stricklin"},
    {"first_name": "Molly", "last_name": "Stricklin"},
    {"first_name": "Brandon", "last_name": "Stricklin"},
    {"first_name": "Gretta", "last_name": "Wright"},
    {"first_name": "Will", "last_name": "Buchanan"},
    {"first_name": "Salem", "last_name": ""},
    {"first_name": "Shelley", "last_name": "Moore"},
    {"first_name": "Shaina", "last_name": "Doser"},
]

db = SessionLocal()
for guest in guests:
    db.add(RSVP(first_name=guest["first_name"], last_name=guest["last_name"], email="", is_attending=False))
db.commit()
db.close()

print(f"Added {len(guests)} guests to the database.")