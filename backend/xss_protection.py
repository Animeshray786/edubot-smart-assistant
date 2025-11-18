"""
XSS Protection Module
Comprehensive Cross-Site Scripting prevention
"""

import re
import html
import bleach
from typing import Optional, List, Dict, Any
from functools import wraps
from flask import request, jsonify

class XSSProtection:
    """Comprehensive XSS protection utilities"""
    
    # Allowed HTML tags for rich text content
    SAFE_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'span', 'div'
    ]
    
    # Allowed attributes for safe tags
    SAFE_ATTRIBUTES = {
        'a': ['href', 'title', 'target'],
        'span': ['class'],
        'div': ['class'],
        'code': ['class'],
        'pre': ['class']
    }
    
    # Dangerous patterns that indicate XSS attempts
    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',  # JavaScript protocol
        r'on\w+\s*=',  # Event handlers (onclick, onload, etc.)
        r'<iframe[^>]*>',  # Iframes
        r'<embed[^>]*>',  # Embed tags
        r'<object[^>]*>',  # Object tags
        r'data:text/html',  # Data URIs
        r'vbscript:',  # VBScript protocol
        r'<meta[^>]*>',  # Meta tags
        r'<link[^>]*>',  # Link tags (can load malicious stylesheets)
        r'<base[^>]*>',  # Base tag (can redirect)
        r'<form[^>]*>',  # Form injection
        r'eval\s*\(',  # eval() calls
        r'expression\s*\(',  # CSS expressions
        r'import\s+',  # ES6 imports
        r'@import',  # CSS imports
    ]
    
    @staticmethod
    def sanitize_html(content: str, allowed_tags: Optional[List[str]] = None) -> str:
        """
        Sanitize HTML content to prevent XSS attacks
        
        Args:
            content: HTML content to sanitize
            allowed_tags: List of allowed HTML tags (uses SAFE_TAGS if None)
            
        Returns:
            str: Sanitized HTML content
        """
        if not content:
            return ''
        
        tags = allowed_tags or XSSProtection.SAFE_TAGS
        
        # Use bleach to clean HTML
        cleaned = bleach.clean(
            content,
            tags=tags,
            attributes=XSSProtection.SAFE_ATTRIBUTES,
            strip=True,  # Remove disallowed tags instead of escaping
            strip_comments=True  # Remove HTML comments
        )
        
        return cleaned
    
    @staticmethod
    def escape_html(text: str) -> str:
        """
        Escape HTML special characters
        
        Args:
            text: Text to escape
            
        Returns:
            str: HTML-escaped text
        """
        if not text:
            return ''
        
        return html.escape(str(text))
    
    @staticmethod
    def detect_xss(text: str) -> tuple[bool, List[str]]:
        """
        Detect potential XSS attacks in text
        
        Args:
            text: Text to analyze
            
        Returns:
            tuple: (is_safe, matched_patterns)
        """
        if not text:
            return True, []
        
        matched_patterns = []
        text_lower = text.lower()
        
        for pattern in XSSProtection.XSS_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL):
                matched_patterns.append(pattern)
        
        is_safe = len(matched_patterns) == 0
        return is_safe, matched_patterns
    
    @staticmethod
    def sanitize_url(url: str) -> str:
        """
        Sanitize URL to prevent JavaScript injection
        
        Args:
            url: URL to sanitize
            
        Returns:
            str: Sanitized URL or empty string if dangerous
        """
        if not url:
            return ''
        
        url = url.strip()
        url_lower = url.lower()
        
        # Block dangerous protocols
        dangerous_protocols = ['javascript:', 'data:', 'vbscript:', 'file:']
        for protocol in dangerous_protocols:
            if url_lower.startswith(protocol):
                return ''
        
        # Only allow http, https, mailto, and relative URLs
        if not (url_lower.startswith('http://') or 
                url_lower.startswith('https://') or 
                url_lower.startswith('mailto:') or
                url_lower.startswith('/') or
                url_lower.startswith('#')):
            return ''
        
        return url
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent path traversal
        
        Args:
            filename: Filename to sanitize
            
        Returns:
            str: Safe filename
        """
        if not filename:
            return 'unnamed'
        
        # Remove path components
        filename = filename.split('/')[-1]
        filename = filename.split('\\')[-1]
        
        # Remove dangerous characters
        filename = re.sub(r'[^\w\s\-\.]', '', filename)
        
        # Limit length
        if len(filename) > 255:
            filename = filename[:255]
        
        return filename or 'unnamed'
    
    @staticmethod
    def sanitize_json_output(data: Any) -> Any:
        """
        Recursively sanitize JSON data before output
        
        Args:
            data: Data structure to sanitize
            
        Returns:
            Sanitized data structure
        """
        if isinstance(data, dict):
            return {key: XSSProtection.sanitize_json_output(value) 
                   for key, value in data.items()}
        elif isinstance(data, list):
            return [XSSProtection.sanitize_json_output(item) for item in data]
        elif isinstance(data, str):
            return XSSProtection.escape_html(data)
        else:
            return data


def validate_xss_input(f):
    """
    Decorator to validate all input data for XSS attacks
    Usage: @validate_xss_input
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check all request data
        data_sources = [
            request.args.to_dict(),
            request.form.to_dict(),
            request.get_json(silent=True) or {}
        ]
        
        for data_dict in data_sources:
            for key, value in data_dict.items():
                if isinstance(value, str):
                    is_safe, patterns = XSSProtection.detect_xss(value)
                    if not is_safe:
                        return jsonify({
                            'error': 'Potential XSS attack detected',
                            'field': key,
                            'patterns_matched': patterns[:3]  # Don't reveal all patterns
                        }), 400
        
        return f(*args, **kwargs)
    
    return decorated_function


def sanitize_response(data: Dict[str, Any], 
                     html_fields: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Sanitize response data before sending to client
    
    Args:
        data: Response data dictionary
        html_fields: Fields that should allow safe HTML (others are escaped)
        
    Returns:
        Sanitized response data
    """
    html_fields = html_fields or []
    sanitized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            if key in html_fields:
                # Allow safe HTML in designated fields
                sanitized[key] = XSSProtection.sanitize_html(value)
            else:
                # Escape all HTML in other fields
                sanitized[key] = XSSProtection.escape_html(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_response(value, html_fields)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_response(item, html_fields) if isinstance(item, dict)
                else XSSProtection.escape_html(item) if isinstance(item, str)
                else item
                for item in value
            ]
        else:
            sanitized[key] = value
    
    return sanitized
