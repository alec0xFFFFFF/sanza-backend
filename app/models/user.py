from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stytch_user_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(100))
    dietary_preferences = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
