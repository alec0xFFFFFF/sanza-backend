from config import Config
import stytch
from stytch.core.response_base import StytchError
from app import db
from app.models import User

class AuthService:
    def __init__(self):
        self.client = stytch.Client(
            project_id=Config.STYTCH_PROJECT_ID,
            secret=Config.STYTCH_SECRET
        )

    def initiate_login(self, email):
        resp = self.client.magic_links.email.login_or_create(
            email=email,
            login_redirect_url=Config.FRONTEND_URL + '/auth/callback'  # Adjust this path as needed
        )
        return resp

    def authenticate(self, token):
        auth_response = self.client.magic_links.authenticate(token=token)
        user = User.query.filter_by(stytch_user_id=auth_response.user_id).first()
        if not user:
            user = User(
                stytch_user_id=auth_response.user_id,
                email=auth_response.email
            )
            db.session.add(user)
            db.session.commit()
        return user

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
        except StytchError as e:
            print(e)
            return None
