"""
Main Flask application for ERP Webapp
Enterprise Risk Management System for Personal Finance
"""
import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from config.database import config
from models import db, migrate
from utils.auth import AuthManager
from middlewares.error_handler import ErrorHandler
from middlewares.cors import CORSManager
from middlewares.logging import RequestLogger

# Import routes
from routes.auth_routes import auth_bp
from routes.financial_routes import financial_bp
from routes.risk_routes import risk_bp
from routes.report_routes import report_bp

def create_app(config_name=None):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize middleware and utilities
    AuthManager(app)
    ErrorHandler(app)
    CORSManager(app)
    RequestLogger(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(financial_bp)
    app.register_blueprint(risk_bp)
    app.register_blueprint(report_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return{'status': 'ok'}, 200
        # """Health check endpoint"""
        # return jsonify({
        #     'status': 'healthy',
        #     'service': 'ERP Webapp Backend',
        #     'version': '1.0.0',
        #     'timestamp': db.func.now()
        # })
    
    # API info endpoint
    @app.route('/api')
    def api_info():
        """API information endpoint"""
        return jsonify({
            'name': 'Plan Wise',
            'version': '1.0.0',
            'description': 'Enterprise Risk Management System for Personal Finance',
            'endpoints': {
                'authentication': '/api/auth',
                'financial_data': '/api/financial',
                'risk_assessment': '/api/risk',
                'reports': '/api/reports'
            },
            'documentation': '/api/docs',
            'health': '/health'
        })


    @app.route('/')
    def index():
        return {
            'message': 'Plan Wise Enterprise Risk Management',
            'status': 'running',
            'version': '1.0.0',
            'endpoints':{
                'health': '/health',
                'auth': '/api/auth',
                'financial': '/api/financial',
                'risk': '/api/risk',
                'reports': '/api/reports'
            }
        }, 200

    
    @app.route('/favicon.ico')
    def favicon():
        return '', 204


    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    
    return app

# Create application instance
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', False)
    
    print(f"Starting ERP Webapp Backend on {host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    # Run the application
    app.run(host=host, port=port, debug=debug)

