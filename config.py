import os
from dotenv import load_dotenv

load_dotenv()  # This loads the .env file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STYTCH_PROJECT_ID = os.environ.get('STYTCH_PROJECT_ID')
    STYTCH_SECRET = os.environ.get('STYTCH_SECRET')
