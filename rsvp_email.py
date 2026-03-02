import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Database setup
DATABASE_URL = "sqlite:///wedding.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RSVP(Base):
    __tablename__ = "rsvps"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=True)
    is_attending = Column(Boolean, default=False)


def send_email(sender_email, recipient_email, sender_password, subject, body):
    """
    Send an email using AOL SMTP server
    """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.aol.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
        return False


def send_date_correction_emails(sender_email, sender_password):
    """
    Send date correction emails to all attending guests
    """
    db = SessionLocal()

    # Get all guests who are attending
    attending_guests = db.query(RSVP).filter(RSVP.is_attending == True).all()

    subject = "Important Date Correction for Our Wedding Reception"

    success_count = 0
    fail_count = 0

    for guest in attending_guests:
        if not guest.email or guest.email.strip() == "":
            print(f"Skipping {guest.first_name} {guest.last_name} - no email address")
            continue

        body = f"""Dear {guest.first_name},

We hope this message finds you well! We wanted to reach out with an important correction regarding our wedding date.

We accidentally listed the wrong date on our invitation. The correct date is:

    CORRECT DATE: Sunday, April 26th, 2026
    (NOT April 25th, 2026)

We sincerely apologize for any confusion this may have caused. Please update your calendars accordingly.

We can't wait to celebrate with you!

With love,
Kalyn & Jack
"""

        if send_email(sender_email, guest.email, sender_password, subject, body):
            success_count += 1
        else:
            fail_count += 1

    db.close()

    print(f"\nEmail Summary:")
    print(f"  Successfully sent: {success_count}")
    print(f"  Failed: {fail_count}")
    print(f"  Total attending guests: {len(attending_guests)}")


if __name__ == "__main__":
    # You'll need to set these - use environment variables for security
    SENDER_EMAIL = os.environ.get("AOL_EMAIL", "your_email@aol.com")
    SENDER_PASSWORD = os.environ.get("AOL_PASSWORD", "your_app_password")

    if SENDER_EMAIL == "your_email@aol.com" or SENDER_PASSWORD == "your_app_password":
        print("Please set your AOL credentials:")
        print("  export AOL_EMAIL='your_email@aol.com'")
        print("  export AOL_PASSWORD='your_app_password'")
        print("\nOr edit this script directly with your credentials.")
    else:
        send_date_correction_emails(SENDER_EMAIL, SENDER_PASSWORD)
