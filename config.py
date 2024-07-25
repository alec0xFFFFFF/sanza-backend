import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost/sanza_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STYTCH_PROJECT_ID = os.environ.get('STYTCH_PROJECT_ID')
    STYTCH_SECRET = os.environ.get('STYTCH_SECRET')
