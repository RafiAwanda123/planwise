"""
Authentication utilities for JWT token management
"""
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import current_app, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import User

class AuthManager:
    """Authentication manager class"""
    
    def __init__(self, app=None):
        self.jwt = JWTManager()
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize JWT with Flask app"""
        self.jwt.init_app(app)
        
        # JWT configuration
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
        
        # JWT error handlers
        @self.jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            return jsonify({
                'success': False,
                'message': 'Token has expired',
                'error': 'token_expired'
            }), 401
        
        @self.jwt.invalid_token_loader
        def invalid_token_callback(error):
            return jsonify({
                'success': False,
                'message': 'Invalid token',
                'error': 'invalid_token'
            }), 401
        
        @self.jwt.unauthorized_loader
        def missing_token_callback(error):
            return jsonify({
                'success': False,
                'message': 'Authorization token is required',
                'error': 'authorization_required'
            }), 401
    
    @staticmethod
    def generate_tokens(user_id):
        """Generate access and refresh tokens"""
        access_token = create_access_token(identity=user_id)
        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
        }
    
    @staticmethod
    def get_current_user():
        """Get current authenticated user"""
        try:
            user_id = get_jwt_identity()
            return User.get_by_id(user_id)
        except Exception:
            return None

# Authentication decorators
def auth_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = AuthManager.get_current_user()
        if not current_user or not current_user.is_active:
            return jsonify({
                'success': False,
                'message': 'User not found or inactive',
                'error': 'user_not_found'
            }), 401
        return f(current_user, *args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = AuthManager.get_current_user()
        if not current_user or not current_user.is_active:
            return jsonify({
                'success': False,
                'message': 'User not found or inactive',
                'error': 'user_not_found'
            }), 401
        
        if current_user.role != 'admin':
            return jsonify({
                'success': False,
                'message': 'Admin access required',
                'error': 'insufficient_permissions'
            }), 403
        
        return f(current_user, *args, **kwargs)
    return decorated_function

def optional_auth(f):
    """Decorator for optional authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = None
        try:
            # Try to get user if token is provided
            if request.headers.get('Authorization'):
                from flask_jwt_extended import verify_jwt_in_request
                verify_jwt_in_request()
                current_user = AuthManager.get_current_user()
        except Exception:
            pass
        
        return f(current_user, *args, **kwargs)
    return decorated_function

