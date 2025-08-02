"""
Request logging middleware
"""
import logging
import time
from flask import request, g
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RequestLogger:
    """Request logging middleware"""
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize request logging with Flask app"""
        
        @app.before_request
        def before_request():
            g.start_time = time.time()
            g.request_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
            
            # Log incoming request
            logger.info(f'[{g.request_id}] {request.method} {request.url} - Start')
            
            # Log request data for debugging (be careful with sensitive data)
            if app.debug and request.is_json:
                try:
                    data = request.get_json()
                    # Remove sensitive fields
                    safe_data = {k: v for k, v in data.items() if k not in ['password', 'token']}
                    logger.debug(f'[{g.request_id}] Request data: {safe_data}')
                except Exception:
                    pass
        
        @app.after_request
        def after_request(response):
            if hasattr(g, 'start_time'):
                duration = time.time() - g.start_time
                logger.info(
                    f'[{g.request_id}] {request.method} {request.url} - '
                    f'{response.status_code} - {duration:.3f}s'
                )
            return response
        
        @app.teardown_request
        def teardown_request(exception):
            if exception:
                logger.error(f'[{getattr(g, "request_id", "unknown")}] Request failed: {exception}')

def log_user_action(user_id, action, details=None):
    """Log user actions for audit trail"""
    log_data = {
        'user_id': user_id,
        'action': action,
        'timestamp': datetime.utcnow().isoformat(),
        'ip_address': request.remote_addr if request else None,
        'user_agent': request.headers.get('User-Agent') if request else None
    }
    
    if details:
        log_data['details'] = details
    
    logger.info(f'User Action: {log_data}')

