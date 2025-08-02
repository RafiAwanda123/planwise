"""
Error handling middleware
"""
import logging
from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandler:
    """Error handler class"""
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize error handlers with Flask app"""
        
        @app.errorhandler(400)
        def bad_request(error):
            return jsonify({
                'success': False,
                'message': 'Bad request',
                'error': 'bad_request'
            }), 400
        
        @app.errorhandler(401)
        def unauthorized(error):
            return jsonify({
                'success': False,
                'message': 'Unauthorized access',
                'error': 'unauthorized'
            }), 401
        
        @app.errorhandler(403)
        def forbidden(error):
            return jsonify({
                'success': False,
                'message': 'Forbidden access',
                'error': 'forbidden'
            }), 403
        
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({
                'success': False,
                'message': 'Resource not found',
                'error': 'not_found'
            }), 404
        
        @app.errorhandler(405)
        def method_not_allowed(error):
            return jsonify({
                'success': False,
                'message': 'Method not allowed',
                'error': 'method_not_allowed'
            }), 405
        
        @app.errorhandler(422)
        def unprocessable_entity(error):
            return jsonify({
                'success': False,
                'message': 'Unprocessable entity',
                'error': 'unprocessable_entity'
            }), 422
        
        @app.errorhandler(500)
        def internal_server_error(error):
            logger.error(f'Internal server error: {error}')
            return jsonify({
                'success': False,
                'message': 'Internal server error',
                'error': 'internal_server_error'
            }), 500
        
        @app.errorhandler(HTTPException)
        def handle_http_exception(error):
            return jsonify({
                'success': False,
                'message': error.description,
                'error': error.name.lower().replace(' ', '_')
            }), error.code
        
        @app.errorhandler(ValidationError)
        def handle_validation_error(error):
            return jsonify({
                'success': False,
                'message': 'Validation error',
                'errors': error.messages,
                'error': 'validation_error'
            }), 400
        
        @app.errorhandler(SQLAlchemyError)
        def handle_database_error(error):
            logger.error(f'Database error: {error}')
            return jsonify({
                'success': False,
                'message': 'Database error occurred',
                'error': 'database_error'
            }), 500
        
        @app.errorhandler(ValueError)
        def handle_value_error(error):
            return jsonify({
                'success': False,
                'message': str(error),
                'error': 'value_error'
            }), 400
        
        @app.errorhandler(KeyError)
        def handle_key_error(error):
            return jsonify({
                'success': False,
                'message': f'Missing required field: {str(error)}',
                'error': 'missing_field'
            }), 400
        
        @app.errorhandler(Exception)
        def handle_generic_exception(error):
            logger.error(f'Unhandled exception: {error}')
            if current_app.debug:
                return jsonify({
                    'success': False,
                    'message': str(error),
                    'error': 'unhandled_exception'
                }), 500
            else:
                return jsonify({
                    'success': False,
                    'message': 'An unexpected error occurred',
                    'error': 'internal_error'
                }), 500

def handle_api_error(message, error_code='api_error', status_code=400):
    """Helper function to create API error responses"""
    return jsonify({
        'success': False,
        'message': message,
        'error': error_code
    }), status_code

def handle_api_success(data=None, message='Success', status_code=200):
    """Helper function to create API success responses"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

