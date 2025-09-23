from datetime import datetime, date, timedelta
from .extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submissions = db.relationship("Submission", backref="user", lazy=True)

class Quest(db.Model):
    __tablename__ = "quests"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    starts_on = db.Column(db.Date, nullable=False)
    ends_on = db.Column(db.Date, nullable=False)
    points = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submissions = db.relationship("Submission", backref="quest", lazy=True)

class Submission(db.Model):
    __tablename__ = "submissions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey("quests.id"), nullable=False)
    text = db.Column(db.Text, default="")
    image_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default="pending")  # pending|approved|rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", lazy=True)

def week_start_for(dt: datetime) -> date:
    d = dt.date()
    return d - timedelta(days=d.weekday())  # Monday
