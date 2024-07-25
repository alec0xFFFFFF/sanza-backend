from flask import Blueprint, request
from pydantic import BaseModel, EmailStr
import stytch
from stytch.core.response_base import StytchError
from app.services.auth_service import AuthService

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

class UserCreate(BaseModel):
    email: EmailStr

auth_service = AuthService()

@bp.route('/initiate-login', methods=['POST'])
def initiate_login():
    """Initiate login/signup process"""
    try:
        user_data = UserCreate(**request.json)
    except ValueError as e:
        return {'message': 'Invalid input', 'errors': str(e)}, 400

    try:
        response = auth_service.initiate_login(user_data.email)
        return {'message': 'Magic link sent. Please check your email.'}, 200
    except StytchError as e:
        return {'message': 'Error sending magic link', 'error': str(e)}, 400

@bp.route('/authenticate', methods=['POST'])
def authenticate():
    """Authenticate user with Stytch token"""
    token = request.json.get('token')
    if not token:
        return {'message': 'Token is required'}, 400

    try:
        user = auth_service.authenticate(token)
        return {'message': 'Authentication successful', 'user_id': user.id}, 200
    except StytchError as e:
        return {'message': 'Invalid token', 'error': str(e)}, 400

@bp.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    if not token:
        return {'message': 'Token is required'}, 400

    user = auth_service.verify_token(token)
    if user:
        return {'user': user.to_dict()}, 200
    else:
        return {'message': 'Invalid token'}, 401
