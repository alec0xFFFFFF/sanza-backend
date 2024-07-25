from datetime import datetime
from app import db
from pgvector.sqlalchemy import Vector

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.JSON, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    embedding = db.Column(Vector(1024))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stytch_user_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(100))
    dietary_preferences = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
