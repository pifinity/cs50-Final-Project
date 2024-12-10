from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy instance for managing database interactions
db = SQLAlchemy()

# Define the Member model to represent club members
class Member(db.Model):
    # Unique identifier for each member
    id = db.Column(db.Integer, primary_key=True)
    # The name of the member (must be unique and not null)
    name = db.Column(db.String(100), nullable=False, unique=True)
    # Relationship to track all sign-ins associated with this member
    sign_ins = db.relationship('SignIn', backref='member', lazy=True)

# Define the Meeting model to represent club meetings
class Meeting(db.Model):
    # Unique identifier for each meeting
    id = db.Column(db.Integer, primary_key=True)
    # The date and time of the meeting (must be provided)
    date = db.Column(db.DateTime, nullable=False)
    # Optional topic or description of the meeting
    topic = db.Column(db.String(200), nullable=True)
    # Relationship to track all sign-ins associated with this meeting
    attendees = db.relationship('SignIn', backref='meeting', lazy=True)

# Define the SignIn model to record member attendance
class SignIn(db.Model):
    # Unique identifier for each sign-in record
    id = db.Column(db.Integer, primary_key=True)
    # Timestamp of when the member signed in (default is the current UTC time)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.utcnow())
    # Foreign key linking the sign-in to a specific member
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    # Foreign key linking the sign-in to a specific meeting (optional)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=True)
