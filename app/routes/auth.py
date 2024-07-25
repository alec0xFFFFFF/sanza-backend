from flask_restx import Namespace, Resource, fields
from flask import request
from pydantic import BaseModel, EmailStr
import stytch
from app.services.auth_service import AuthService

api = Namespace('auth', description='Authentication operations')

class UserCreate(BaseModel):
    email: EmailStr

user_model = api.model('User', {
    'email': fields.String(required=True, description='User email')
})

auth_service = AuthService()

@api.route('/initiate-login')
class InitiateLogin(Resource):
    @api.expect(user_model)
    @api.response(200, 'Login magic link sent')
    @api.response(400, 'Invalid input')
    def post(self):
        """Initiate login/signup process"""
        try:
            user_data = UserCreate(**request.json)
        except ValueError as e:
            return {'message': 'Invalid input', 'errors': str(e)}, 400

        try:
            response = auth_service.initiate_login(user_data.email)
            return {'message': 'Magic link sent. Please check your email.'}, 200
        except stytch.exceptions.StytchError as e:
            return {'message': 'Error sending magic link', 'error': str(e)}, 400

@api.route('/authenticate')
class Authenticate(Resource):
    @api.doc(params={'token': 'Stytch token from magic link'})
    @api.response(200, 'Authentication successful')
    @api.response(400, 'Invalid token')
    def post(self):
        """Authenticate user with Stytch token"""
        token = request.json.get('token')
        if not token:
            return {'message': 'Token is required'}, 400

        try:
            user = auth_service.authenticate(token)
            return {'message': 'Authentication successful', 'user_id': user.id}, 200
        except stytch.exceptions.StytchError as e:
            return {'message': 'Invalid token', 'error': str(e)}, 400

@api.route('/verify-token')
class VerifyToken(Resource):
    @api.doc(params={'token': 'JWT token'})
    @api.response(200, 'Token verified')
    @api.response(401, 'Invalid token')
    def post(self):
        token = request.json.get('token')
        if not token:
            return {'message': 'Token is required'}, 400

        user = auth_service.verify_token(token)
        if user:
            return {'user': user.to_dict()}, 200
        else:
            return {'message': 'Invalid token'}, 401
