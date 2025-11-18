"""
Advanced Logging System
Structured logging with rotation, levels, and formatting
"""

import logging
import logging.handlers
import os
import json
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path

class StructuredLogger:
    """Structured logging with JSON output and file rotation"""
    
    _loggers: Dict[str, logging.Logger] = {}
    
    @staticmethod
    def get_logger(name: str = 'edubot',
                   log_file: Optional[str] = None,
                   level: str = 'INFO',
                   max_bytes: int = 10485760,  # 10MB
                   backup_count: int = 5) -> logging.Logger:
        """
        Get or create a structured logger
        
        Args:
            name: Logger name
            log_file: Log file path
            level: Logging level
            max_bytes: Max log file size before rotation
            backup_count: Number of backup files to keep
            
        Returns:
            logging.Logger: Configured logger
        """
        if name in StructuredLogger._loggers:
            return StructuredLogger._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Console handler with color coding
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            '[%(levelname)s] %(asctime)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler with rotation
        if log_file:
            # Create log directory if it doesn't exist
            log_dir = os.path.dirname(log_file)
            if log_dir:
                Path(log_dir).mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = JSONFormatter()
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        # Error file handler (separate file for errors)
        if log_file:
            error_file = log_file.replace('.log', '.error.log')
            error_handler = logging.handlers.RotatingFileHandler(
                error_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(JSONFormatter())
            logger.addHandler(error_handler)
        
        StructuredLogger._loggers[name] = logger
        return logger
    
    @staticmethod
    def log_request(logger: logging.Logger, request: Any, response_code: int,
                   duration_ms: float, user_id: Optional[int] = None):
        """
        Log HTTP request with structured data
        
        Args:
            logger: Logger instance
            request: Flask request object
            response_code: HTTP response code
            duration_ms: Request duration in milliseconds
            user_id: User ID if authenticated
        """
        extra = {
            'event_type': 'http_request',
            'method': request.method,
            'path': request.path,
            'response_code': response_code,
            'duration_ms': duration_ms,
            'user_id': user_id,
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string if request.user_agent else None
        }
        
        logger.info(
            f'{request.method} {request.path} - {response_code} - {duration_ms:.2f}ms',
            extra=extra
        )
    
    @staticmethod
    def log_security_event(logger: logging.Logger, event_type: str,
                          severity: str, details: Dict[str, Any],
                          user_id: Optional[int] = None):
        """
        Log security event
        
        Args:
            logger: Logger instance
            event_type: Type of security event
            severity: Event severity (low, medium, high, critical)
            details: Event details
            user_id: User ID if applicable
        """
        extra = {
            'event_type': 'security',
            'security_event': event_type,
            'severity': severity,
            'user_id': user_id,
            **details
        }
        
        level = {
            'low': logging.INFO,
            'medium': logging.WARNING,
            'high': logging.ERROR,
            'critical': logging.CRITICAL
        }.get(severity, logging.WARNING)
        
        logger.log(
            level,
            f'Security Event: {event_type} - {severity.upper()}',
            extra=extra
        )
    
    @staticmethod
    def log_database_operation(logger: logging.Logger, operation: str,
                              table: str, duration_ms: float,
                              rows_affected: Optional[int] = None):
        """
        Log database operation
        
        Args:
            logger: Logger instance
            operation: Database operation (SELECT, INSERT, UPDATE, DELETE)
            table: Table name
            duration_ms: Operation duration
            rows_affected: Number of rows affected
        """
        extra = {
            'event_type': 'database',
            'operation': operation,
            'table': table,
            'duration_ms': duration_ms,
            'rows_affected': rows_affected
        }
        
        logger.debug(
            f'DB {operation} on {table} - {duration_ms:.2f}ms',
            extra=extra
        )


class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            'timestamp': datetime.utcfromtimestamp(record.created).isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'event_type'):
            for key, value in record.__dict__.items():
                if key not in ['name', 'msg', 'args', 'created', 'filename',
                              'funcName', 'levelname', 'levelno', 'lineno',
                              'module', 'msecs', 'message', 'pathname',
                              'process', 'processName', 'relativeCreated',
                              'thread', 'threadName', 'exc_info', 'exc_text',
                              'stack_info']:
                    log_data[key] = value
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, default=str)


class ColoredFormatter(logging.Formatter):
    """Colored console formatter"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m'    # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with color"""
        color = self.COLORS.get(record.levelname, '')
        record.levelname = f'{color}{record.levelname}{self.RESET}'
        return super().format(record)


# Performance monitoring decorator
def log_performance(logger: logging.Logger):
    """
    Decorator to log function performance
    Usage: @log_performance(logger)
    """
    def decorator(f):
        from functools import wraps
        import time
        
        @wraps(f)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = f(*args, **kwargs)
                duration_ms = (time.time() - start) * 1000
                
                logger.debug(
                    f'Function {f.__name__} completed in {duration_ms:.2f}ms',
                    extra={
                        'event_type': 'performance',
                        'function': f.__name__,
                        'duration_ms': duration_ms,
                        'success': True
                    }
                )
                
                return result
            except Exception as e:
                duration_ms = (time.time() - start) * 1000
                
                logger.error(
                    f'Function {f.__name__} failed after {duration_ms:.2f}ms: {str(e)}',
                    extra={
                        'event_type': 'performance',
                        'function': f.__name__,
                        'duration_ms': duration_ms,
                        'success': False,
                        'error': str(e)
                    },
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator
