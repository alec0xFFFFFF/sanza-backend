from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    if not token:
        return jsonify({"error": "Token is required"}), 400

    auth_service = AuthService()
    user = auth_service.verify_token(token)

    if user:
        return jsonify({"user": user.to_dict()}), 200
    else:
        return jsonify({"error": "Invalid token"}), 401
