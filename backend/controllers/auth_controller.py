"""
Authentication controller for user registration and login
"""
from flask import jsonify
from models import User, db
from utils.auth import AuthManager
from middlewares.validation import validate_json, UserRegistrationSchema, UserLoginSchema
from middlewares.error_handler import handle_api_error, handle_api_success
from middlewares.logging import log_user_action

class AuthController:
    """Authentication controller"""
    
    @staticmethod
    @validate_json(UserRegistrationSchema)
    def register(validated_data):
        """Register new user"""
        try:
            # Check if user already exists
            existing_user = User.get_by_email(validated_data['email'])
            if existing_user:
                return handle_api_error('User with this email already exists', 'user_exists', 409)
            
            # Create new user
            user = User.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                role=validated_data.get('role', 'user')
            )
            
            # Generate tokens
            tokens = AuthManager.generate_tokens(user.id)
            
            # Log user action
            log_user_action(user.id, 'user_registered')
            
            return handle_api_success({
                'user': user.to_dict(),
                'tokens': tokens
            }, 'User registered successfully', 201)
            
        except ValueError as e:
            return handle_api_error(str(e), 'registration_error', 400)
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Registration failed', 'registration_error', 500)
    
    @staticmethod
    @validate_json(UserLoginSchema)
    def login(validated_data):
        """Login user"""
        try:
            # Find user by email
            user = User.get_by_email(validated_data['email'])
            if not user:
                return handle_api_error('Invalid email or password', 'invalid_credentials', 401)
            
            # Check if user is active
            if not user.is_active:
                return handle_api_error('Account is deactivated', 'account_deactivated', 401)
            
            # Verify password
            if not user.check_password(validated_data['password']):
                return handle_api_error('Invalid email or password', 'invalid_credentials', 401)
            
            # Generate tokens
            tokens = AuthManager.generate_tokens(user.id)
            
            # Log user action
            log_user_action(user.id, 'user_login')
            
            return handle_api_success({
                'user': user.to_dict(),
                'tokens': tokens
            }, 'Login successful')
            
        except Exception as e:
            return handle_api_error('Login failed', 'login_error', 500)
    
    @staticmethod
    def logout(current_user):
        """Logout user (client-side token removal)"""
        try:
            # Log user action
            log_user_action(current_user.id, 'user_logout')
            
            return handle_api_success(message='Logout successful')
            
        except Exception as e:
            return handle_api_error('Logout failed', 'logout_error', 500)
    
    @staticmethod
    def get_profile(current_user):
        """Get current user profile"""
        try:
            return handle_api_success({
                'user': current_user.to_dict()
            }, 'Profile retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve profile', 'profile_error', 500)
    
    @staticmethod
    @validate_json(UserRegistrationSchema)
    def update_profile(current_user, validated_data):
        """Update user profile"""
        try:
            # Update user fields (excluding email and password)
            update_fields = {
                'first_name': validated_data.get('first_name', current_user.first_name),
                'last_name': validated_data.get('last_name', current_user.last_name)
            }
            
            current_user.update(**update_fields)
            
            # Log user action
            log_user_action(current_user.id, 'profile_updated', update_fields)
            
            return handle_api_success({
                'user': current_user.to_dict()
            }, 'Profile updated successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to update profile', 'update_error', 500)
    
    @staticmethod
    def change_password(current_user, validated_data):
        """Change user password"""
        try:
            current_password = validated_data.get('current_password')
            new_password = validated_data.get('new_password')
            
            if not current_password or not new_password:
                return handle_api_error('Current password and new password are required', 'missing_fields', 400)
            
            # Verify current password
            if not current_user.check_password(current_password):
                return handle_api_error('Current password is incorrect', 'invalid_password', 400)
            
            # Update password
            current_user.set_password(new_password)
            current_user.save()
            
            # Log user action
            log_user_action(current_user.id, 'password_changed')
            
            return handle_api_success(message='Password changed successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to change password', 'password_error', 500)

