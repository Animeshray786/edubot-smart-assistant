"""
Enhanced Error Handling
Custom error handlers and error pages
"""

from flask import jsonify, render_template, request
from typing import Tuple, Dict, Any
import traceback
import sys

class AppError(Exception):
    """Base application error"""
    
    def __init__(self, message: str, status_code: int = 500, 
                 payload: Dict[str, Any] = None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary"""
        rv = dict(self.payload)
        rv['error'] = self.message
        rv['status_code'] = self.status_code
        return rv


class ValidationError(AppError):
    """Validation error"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, status_code=400)
        if field:
            self.payload['field'] = field


class AuthenticationError(AppError):
    """Authentication error"""
    def __init__(self, message: str = 'Authentication required'):
        super().__init__(message, status_code=401)


class AuthorizationError(AppError):
    """Authorization error"""
    def __init__(self, message: str = 'Insufficient permissions'):
        super().__init__(message, status_code=403)


class NotFoundError(AppError):
    """Resource not found error"""
    def __init__(self, message: str = 'Resource not found', resource_type: str = None):
        super().__init__(message, status_code=404)
        if resource_type:
            self.payload['resource_type'] = resource_type


class ConflictError(AppError):
    """Conflict error (e.g., duplicate entry)"""
    def __init__(self, message: str = 'Resource conflict'):
        super().__init__(message, status_code=409)


class RateLimitError(AppError):
    """Rate limit exceeded error"""
    def __init__(self, message: str = 'Rate limit exceeded', retry_after: int = None):
        super().__init__(message, status_code=429)
        if retry_after:
            self.payload['retry_after'] = retry_after


def register_error_handlers(app):
    """Register error handlers with Flask app"""
    
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError) -> Tuple[Dict[str, Any], int]:
        """Handle custom app errors"""
        response = error.to_dict()
        
        # Log error
        if hasattr(app, 'logger'):
            app.logger.error(
                f'App Error: {error.message}',
                extra={
                    'event_type': 'error',
                    'error_type': error.__class__.__name__,
                    'status_code': error.status_code,
                    'payload': error.payload
                }
            )
        
        return jsonify(response), error.status_code
    
    @app.errorhandler(400)
    def handle_bad_request(error) -> Tuple[Any, int]:
        """Handle 400 Bad Request"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Bad Request',
                'message': str(error) if str(error) != '400 Bad Request: ' else 'Invalid request data',
                'status_code': 400
            }), 400
        return render_template_or_json('errors/400.html', error=error), 400
    
    @app.errorhandler(401)
    def handle_unauthorized(error) -> Tuple[Any, int]:
        """Handle 401 Unauthorized"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required',
                'status_code': 401
            }), 401
        return render_template_or_json('errors/401.html', error=error), 401
    
    @app.errorhandler(403)
    def handle_forbidden(error) -> Tuple[Any, int]:
        """Handle 403 Forbidden"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Forbidden',
                'message': 'You do not have permission to access this resource',
                'status_code': 403
            }), 403
        return render_template_or_json('errors/403.html', error=error), 403
    
    @app.errorhandler(404)
    def handle_not_found(error) -> Tuple[Any, int]:
        """Handle 404 Not Found"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Not Found',
                'message': f'The requested resource was not found: {request.path}',
                'status_code': 404
            }), 404
        return render_template_or_json('errors/404.html', error=error), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error) -> Tuple[Any, int]:
        """Handle 405 Method Not Allowed"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Method Not Allowed',
                'message': f'Method {request.method} not allowed for {request.path}',
                'status_code': 405
            }), 405
        return render_template_or_json('errors/405.html', error=error), 405
    
    @app.errorhandler(429)
    def handle_rate_limit(error) -> Tuple[Any, int]:
        """Handle 429 Too Many Requests"""
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later.',
            'status_code': 429
        }), 429
    
    @app.errorhandler(500)
    def handle_internal_error(error) -> Tuple[Any, int]:
        """Handle 500 Internal Server Error"""
        # Log the full error
        if hasattr(app, 'logger'):
            app.logger.error(
                'Internal Server Error',
                extra={
                    'event_type': 'error',
                    'error_type': 'InternalServerError',
                    'path': request.path,
                    'method': request.method
                },
                exc_info=True
            )
        
        if request.path.startswith('/api/'):
            # Don't expose internal errors in production
            if app.config.get('DEBUG'):
                return jsonify({
                    'error': 'Internal Server Error',
                    'message': str(error),
                    'traceback': traceback.format_exc(),
                    'status_code': 500
                }), 500
            else:
                return jsonify({
                    'error': 'Internal Server Error',
                    'message': 'An unexpected error occurred',
                    'status_code': 500
                }), 500
        
        return render_template_or_json('errors/500.html', error=error), 500
    
    @app.errorhandler(503)
    def handle_service_unavailable(error) -> Tuple[Any, int]:
        """Handle 503 Service Unavailable"""
        return jsonify({
            'error': 'Service Unavailable',
            'message': 'The service is temporarily unavailable. Please try again later.',
            'status_code': 503
        }), 503
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> Tuple[Any, int]:
        """Handle unexpected errors"""
        # Log the full error
        if hasattr(app, 'logger'):
            app.logger.critical(
                f'Unexpected error: {str(error)}',
                extra={
                    'event_type': 'error',
                    'error_type': error.__class__.__name__,
                    'path': request.path,
                    'method': request.method
                },
                exc_info=True
            )
        
        if request.path.startswith('/api/'):
            if app.config.get('DEBUG'):
                return jsonify({
                    'error': 'Unexpected Error',
                    'message': str(error),
                    'type': error.__class__.__name__,
                    'traceback': traceback.format_exc(),
                    'status_code': 500
                }), 500
            else:
                return jsonify({
                    'error': 'Internal Server Error',
                    'message': 'An unexpected error occurred',
                    'status_code': 500
                }), 500
        
        return render_template_or_json('errors/500.html', error=error), 500


def render_template_or_json(template: str, **context) -> Any:
    """Render template or return JSON based on request type"""
    try:
        return render_template(template, **context)
    except:
        # If template doesn't exist, return JSON
        error = context.get('error')
        return jsonify({
            'error': str(error) if error else 'An error occurred',
            'template': template
        })
