"""
SQL Injection Prevention Middleware
Additional layer of security for database operations
"""

from flask import request, jsonify
from functools import wraps
import re


class SQLInjectionPrevention:
    """Prevent SQL injection attacks"""
    
    # Dangerous SQL patterns
    SQL_INJECTION_PATTERNS = [
        # Union-based injection
        r'(\bUNION\b.*\bSELECT\b)',
        r'(\bUNION\b.*\bALL\b.*\bSELECT\b)',
        
        # Boolean-based injection
        r"(\b(OR|AND)\b.*[=<>].*['\"])",
        r"(\b(OR|AND)\b.*\b1\s*=\s*1\b)",
        r"(\b(OR|AND)\b.*\b1\s*=\s*1\b.*--)",
        
        # Time-based injection
        r'(\bSLEEP\b\s*\()',
        r'(\bBENCHMARK\b\s*\()',
        r'(\bWAITFOR\b.*\bDELAY\b)',
        
        # Stacked queries
        r'(;.*\b(DROP|DELETE|INSERT|UPDATE|CREATE|ALTER)\b)',
        
        # Comment-based injection
        r'(--|\#|\/\*|\*\/)',
        
        # Database manipulation
        r'(\bDROP\b.*\b(TABLE|DATABASE|SCHEMA)\b)',
        r'(\bDELETE\b.*\bFROM\b)',
        r'(\bINSERT\b.*\bINTO\b)',
        r'(\bUPDATE\b.*\bSET\b)',
        r'(\bCREATE\b.*\b(TABLE|DATABASE|USER)\b)',
        r'(\bALTER\b.*\bTABLE\b)',
        r'(\bTRUNCATE\b.*\bTABLE\b)',
        
        # Information gathering
        r'(\bSELECT\b.*\bFROM\b.*\binformation_schema\b)',
        r'(\bSELECT\b.*\bFROM\b.*\bmysql\b)',
        r'(\bSELECT\b.*\bFROM\b.*\bpg_catalog\b)',
        
        # Privilege escalation
        r'(\bGRANT\b.*\bTO\b)',
        r'(\bREVOKE\b.*\bFROM\b)',
        
        # Execution
        r'(\bEXEC\b|\bEXECUTE\b)',
        r'(\bxp_cmdshell\b)',
        
        # Hex/Char encoding
        r'(0x[0-9a-fA-F]+)',
        r'(\bCHAR\b\s*\()',
        r'(\bCONCAT\b\s*\()',
    ]
    
    def __init__(self):
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.SQL_INJECTION_PATTERNS
        ]
    
    def detect_sql_injection(self, text):
        """
        Detect SQL injection patterns in text
        
        Args:
            text: Text to check
            
        Returns:
            tuple: (is_safe, matched_patterns)
        """
        if not text or not isinstance(text, str):
            return True, []
        
        matched_patterns = []
        
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                matched_patterns.append(pattern.pattern)
        
        is_safe = len(matched_patterns) == 0
        
        return is_safe, matched_patterns
    
    def sanitize_input(self, text, max_length=1000):
        """
        Sanitize text input for database operations
        
        Args:
            text: Text to sanitize
            max_length: Maximum allowed length
            
        Returns:
            str: Sanitized text
        """
        if not text:
            return text
        
        # Convert to string
        text = str(text)
        
        # Limit length
        text = text[:max_length]
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Remove control characters except newlines and tabs
        text = ''.join(char for char in text 
                      if char.isprintable() or char in ['\n', '\t', '\r'])
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def validate_identifier(self, identifier):
        """
        Validate database identifiers (table/column names)
        
        Args:
            identifier: Identifier to validate
            
        Returns:
            bool: True if valid
        """
        if not identifier:
            return False
        
        # Only alphanumeric and underscores
        return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier))


# Global instance
sql_injection_prevention = SQLInjectionPrevention()


def validate_sql_input(f):
    """
    Decorator to validate request inputs for SQL injection
    
    Usage:
        @app.route('/api/search')
        @validate_sql_input
        def search():
            query = request.args.get('q')
            # query is already validated
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check GET parameters
        for key, value in request.args.items():
            if isinstance(value, str):
                is_safe, patterns = sql_injection_prevention.detect_sql_injection(value)
                if not is_safe:
                    return jsonify({
                        'error': 'Invalid input detected',
                        'message': 'Your input contains potentially dangerous patterns',
                        'field': key,
                        'patterns_matched': len(patterns)
                    }), 400
        
        # Check JSON body
        if request.is_json:
            data = request.get_json()
            if data:
                for key, value in data.items():
                    if isinstance(value, str):
                        is_safe, patterns = sql_injection_prevention.detect_sql_injection(value)
                        if not is_safe:
                            return jsonify({
                                'error': 'Invalid input detected',
                                'message': 'Your input contains potentially dangerous patterns',
                                'field': key,
                                'patterns_matched': len(patterns)
                            }), 400
        
        # Check form data
        for key, value in request.form.items():
            if isinstance(value, str):
                is_safe, patterns = sql_injection_prevention.detect_sql_injection(value)
                if not is_safe:
                    return jsonify({
                        'error': 'Invalid input detected',
                        'message': 'Your input contains potentially dangerous patterns',
                        'field': key,
                        'patterns_matched': len(patterns)
                    }), 400
        
        return f(*args, **kwargs)
    
    return decorated_function


def sanitize_search_query(query):
    """
    Sanitize search query for safe database operations
    
    Args:
        query: Search query string
        
    Returns:
        str: Sanitized query
    """
    if not query:
        return ""
    
    # Basic sanitization
    query = sql_injection_prevention.sanitize_input(query, max_length=500)
    
    # Check for SQL injection
    is_safe, patterns = sql_injection_prevention.detect_sql_injection(query)
    
    if not is_safe:
        # Return empty string if dangerous patterns found
        return ""
    
    # Escape special characters for LIKE queries
    query = query.replace('%', '\\%').replace('_', '\\_')
    
    return query


def validate_database_identifier(identifier):
    """
    Validate database identifiers (table/column names)
    
    Args:
        identifier: Identifier to validate
        
    Returns:
        bool: True if valid
    """
    return sql_injection_prevention.validate_identifier(identifier)
