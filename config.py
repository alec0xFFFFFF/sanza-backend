import os
from dotenv import load_dotenv

load_dotenv()  # This loads the .env file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Database configuration
    db_params = {
        "dbname": os.environ.get("PGDATABASE"),
        "user": os.environ.get("PGUSER"),
        "password": os.environ.get("PGPASSWORD"),
        "host": os.environ.get("PGHOST"),
        "port": os.environ.get("PGPORT")
    }
    
    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STYTCH_PROJECT_ID = os.environ.get('STYTCH_PROJECT_ID')
    STYTCH_SECRET = os.environ.get('STYTCH_SECRET')
    POSTHOG_KEY = os.environ.get("POSTHOG_KEY")
    POSTHOG_URL = os.environ.get("POSTHOG_URL")
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
