"""
CORS middleware for cross-origin requests
"""
from flask_cors import CORS

class CORSManager:
    """CORS manager class"""
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize CORS with Flask app"""
        
        # CORS configuration
        cors_config = {
            'origins': ['*'],  # Allow all origins for development
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            'allow_headers': [
                'Content-Type',
                'Authorization',
                'Access-Control-Allow-Credentials',
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Headers',
                'Access-Control-Allow-Methods'
            ],
            'supports_credentials': True
        }
        
        # Initialize CORS
        CORS(app, **cors_config)
        
        # Add custom CORS headers
        @app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response

