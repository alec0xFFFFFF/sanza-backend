from config import Config
import stytch
from app import db
from app.models import User

class AuthService:
    def __init__(self):
        self.client = stytch.Client(
            project_id=Config.STYTCH_PROJECT_ID,
            secret=Config.STYTCH_SECRET
        )

    def verify_token(self, token):
        try:
            response = self.client.auth.authenticate_token(token)
            user_id = response['user_id']
            user = User.query.filter_by(stytch_user_id=user_id).first()
            if not user:
                # Create new user if not exists
                user = User(stytch_user_id=user_id, email=response['email'])
                db.session.add(user)
                db.session.commit()
            return user
        except stytch.exceptions.RequestException:
            return None
