from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey, Table, Column, Integer
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Association Table
session_speakers = Table(
    'session_speakers',
    db.Model.metadata,
    Column('id', Integer, primary_key=True),
    Column('session_id', Integer, ForeignKey('sessions.id')),
    Column('speaker_id', Integer, ForeignKey('speakers.id'))
)

# Event Model
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    sessions = db.relationship("Session", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Event {self.id}, {self.name}, {self.location}>'

# Session Model
class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    event = db.relationship("Event", back_populates="sessions")
    speakers = db.relationship("Speaker", secondary=session_speakers, back_populates="sessions")

    def __repr__(self):
        return f'<Session {self.id}, {self.title}, {self.start_time}>'

# Speaker Model
class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    bio = db.relationship("Bio", back_populates="speaker", uselist=False, cascade="all, delete-orphan")
    sessions = db.relationship("Session", secondary=session_speakers, back_populates="speakers")

    def __repr__(self):
        return f'<Speaker {self.id}, {self.name}>'

# Bio Model
class Bio(db.Model):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.Text, nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))

    speaker = db.relationship("Speaker", back_populates="bio")

    def __repr__(self):
        return f'<Bio {self.id}, {self.bio_text[:20]}...>'
