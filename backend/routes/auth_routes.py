"""
Authentication routes
"""
from flask import Blueprint
from controllers.auth_controller import AuthController
from utils.auth import auth_required

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Public routes
@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    return AuthController.register()

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    return AuthController.login()

# Protected routes
@auth_bp.route('/logout', methods=['POST'])
@auth_required
def logout(current_user):
    """User logout endpoint"""
    return AuthController.logout(current_user)

@auth_bp.route('/profile', methods=['GET'])
@auth_required
def get_profile(current_user):
    """Get user profile endpoint"""
    return AuthController.get_profile(current_user)

@auth_bp.route('/profile', methods=['PUT'])
@auth_required
def update_profile(current_user):
    """Update user profile endpoint"""
    return AuthController.update_profile(current_user)

@auth_bp.route('/change-password', methods=['POST'])
@auth_required
def change_password(current_user):
    """Change password endpoint"""
    return AuthController.change_password(current_user)

