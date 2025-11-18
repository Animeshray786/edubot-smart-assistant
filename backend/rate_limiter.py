"""
API Rate Limiting Dashboard
Monitor API usage, set custom rate limits, block abusive IPs, usage analytics
"""
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import threading


class RateLimiter:
    """Rate limiting system with analytics"""
    
    def __init__(self):
        self.requests = defaultdict(list)  # IP/User -> list of timestamps
        self.blocked_ips = set()
        self.user_limits = {}  # user_id -> custom limit
        self.ip_limits = {}  # IP -> custom limit
        self.violations = []
        self._lock = threading.Lock()
        
        # Default limits
        self.default_limits = {
            'requests_per_minute': 60,
            'requests_per_hour': 1000,
            'requests_per_day': 10000
        }
    
    def check_rate_limit(self, identifier: str, limit_type: str = 'ip') -> Dict:
        """
        Check if request should be allowed
        
        Args:
            identifier: IP address or user_id
            limit_type: 'ip' or 'user'
            
        Returns:
            Dict with allowed status and details
        """
        with self._lock:
            now = time.time()
            
            # Check if blocked
            if limit_type == 'ip' and identifier in self.blocked_ips:
                return {
                    'allowed': False,
                    'reason': 'IP address is blocked',
                    'retry_after': None
                }
            
            # Get custom or default limits
            if limit_type == 'user' and identifier in self.user_limits:
                limits = self.user_limits[identifier]
            elif limit_type == 'ip' and identifier in self.ip_limits:
                limits = self.ip_limits[identifier]
            else:
                limits = self.default_limits
            
            # Clean old requests
            cutoff_minute = now - 60
            cutoff_hour = now - 3600
            cutoff_day = now - 86400
            
            self.requests[identifier] = [
                ts for ts in self.requests[identifier]
                if ts > cutoff_day
            ]
            
            # Count requests
            recent_requests = self.requests[identifier]
            minute_count = sum(1 for ts in recent_requests if ts > cutoff_minute)
            hour_count = sum(1 for ts in recent_requests if ts > cutoff_hour)
            day_count = len(recent_requests)
            
            # Check limits
            if minute_count >= limits['requests_per_minute']:
                self._log_violation(identifier, 'minute', minute_count, limits['requests_per_minute'])
                return {
                    'allowed': False,
                    'reason': 'Rate limit exceeded (per minute)',
                    'limit': limits['requests_per_minute'],
                    'current': minute_count,
                    'retry_after': 60,
                    'period': 'minute'
                }
            
            if hour_count >= limits['requests_per_hour']:
                self._log_violation(identifier, 'hour', hour_count, limits['requests_per_hour'])
                return {
                    'allowed': False,
                    'reason': 'Rate limit exceeded (per hour)',
                    'limit': limits['requests_per_hour'],
                    'current': hour_count,
                    'retry_after': 3600,
                    'period': 'hour'
                }
            
            if day_count >= limits['requests_per_day']:
                self._log_violation(identifier, 'day', day_count, limits['requests_per_day'])
                return {
                    'allowed': False,
                    'reason': 'Rate limit exceeded (per day)',
                    'limit': limits['requests_per_day'],
                    'current': day_count,
                    'retry_after': 86400,
                    'period': 'day'
                }
            
            # Request allowed - record it
            self.requests[identifier].append(now)
            
            return {
                'allowed': True,
                'remaining': {
                    'minute': limits['requests_per_minute'] - minute_count - 1,
                    'hour': limits['requests_per_hour'] - hour_count - 1,
                    'day': limits['requests_per_day'] - day_count - 1
                }
            }
    
    def _log_violation(self, identifier: str, period: str, current: int, limit: int):
        """Log rate limit violation"""
        self.violations.append({
            'identifier': identifier,
            'period': period,
            'current': current,
            'limit': limit,
            'timestamp': datetime.now()
        })
        
        # Keep only last 1000 violations
        if len(self.violations) > 1000:
            self.violations = self.violations[-1000:]
    
    def set_custom_limit(self, identifier: str, limit_type: str, limits: Dict):
        """
        Set custom rate limits for user or IP
        
        Args:
            identifier: User ID or IP address
            limit_type: 'ip' or 'user'
            limits: Dict with requests_per_minute, requests_per_hour, requests_per_day
        """
        with self._lock:
            if limit_type == 'user':
                self.user_limits[identifier] = limits
            elif limit_type == 'ip':
                self.ip_limits[identifier] = limits
    
    def remove_custom_limit(self, identifier: str, limit_type: str):
        """Remove custom rate limits"""
        with self._lock:
            if limit_type == 'user' and identifier in self.user_limits:
                del self.user_limits[identifier]
            elif limit_type == 'ip' and identifier in self.ip_limits:
                del self.ip_limits[identifier]
    
    def block_ip(self, ip_address: str, reason: str = None):
        """Block an IP address"""
        with self._lock:
            self.blocked_ips.add(ip_address)
            self.violations.append({
                'identifier': ip_address,
                'action': 'blocked',
                'reason': reason or 'Manual block',
                'timestamp': datetime.now()
            })
    
    def unblock_ip(self, ip_address: str):
        """Unblock an IP address"""
        with self._lock:
            self.blocked_ips.discard(ip_address)
    
    def get_usage_stats(self, identifier: str = None, hours: int = 24) -> Dict:
        """
        Get usage statistics
        
        Args:
            identifier: Specific IP/user or None for all
            hours: Time period to analyze
            
        Returns:
            Usage statistics
        """
        cutoff = time.time() - (hours * 3600)
        
        if identifier:
            recent = [ts for ts in self.requests.get(identifier, []) if ts > cutoff]
            
            return {
                'identifier': identifier,
                'total_requests': len(recent),
                'requests_per_hour': len(recent) / hours if hours > 0 else 0,
                'custom_limits': self.user_limits.get(identifier) or self.ip_limits.get(identifier),
                'is_blocked': identifier in self.blocked_ips
            }
        else:
            # All identifiers
            stats = {
                'total_identifiers': len(self.requests),
                'total_requests': 0,
                'top_users': [],
                'blocked_count': len(self.blocked_ips),
                'custom_limits_count': len(self.user_limits) + len(self.ip_limits)
            }
            
            identifier_stats = []
            for ident, timestamps in self.requests.items():
                recent = [ts for ts in timestamps if ts > cutoff]
                if recent:
                    stats['total_requests'] += len(recent)
                    identifier_stats.append({
                        'identifier': ident,
                        'requests': len(recent),
                        'requests_per_hour': len(recent) / hours if hours > 0 else 0
                    })
            
            stats['top_users'] = sorted(
                identifier_stats,
                key=lambda x: x['requests'],
                reverse=True
            )[:10]
            
            return stats
    
    def get_violations(self, hours: int = 24, identifier: str = None) -> List[Dict]:
        """Get rate limit violations"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        recent_violations = [
            v for v in self.violations
            if v['timestamp'] > cutoff
        ]
        
        if identifier:
            recent_violations = [
                v for v in recent_violations
                if v.get('identifier') == identifier
            ]
        
        return sorted(recent_violations, key=lambda x: x['timestamp'], reverse=True)
    
    def get_abuse_suspects(self, threshold_multiplier: float = 2.0) -> List[Dict]:
        """
        Identify potential abusive users
        
        Args:
            threshold_multiplier: How many times over limit to consider abuse
            
        Returns:
            List of suspected abusive identifiers
        """
        suspects = []
        
        for identifier, timestamps in self.requests.items():
            if not timestamps:
                continue
            
            now = time.time()
            minute_count = sum(1 for ts in timestamps if ts > now - 60)
            hour_count = sum(1 for ts in timestamps if ts > now - 3600)
            
            # Get applicable limits
            limits = (
                self.user_limits.get(identifier) or
                self.ip_limits.get(identifier) or
                self.default_limits
            )
            
            abuse_score = 0
            reasons = []
            
            if minute_count > limits['requests_per_minute'] * threshold_multiplier:
                abuse_score += 3
                reasons.append(f"Minute: {minute_count}/{limits['requests_per_minute']}")
            
            if hour_count > limits['requests_per_hour'] * threshold_multiplier:
                abuse_score += 2
                reasons.append(f"Hour: {hour_count}/{limits['requests_per_hour']}")
            
            if abuse_score > 0:
                suspects.append({
                    'identifier': identifier,
                    'abuse_score': abuse_score,
                    'reasons': reasons,
                    'minute_requests': minute_count,
                    'hour_requests': hour_count,
                    'is_blocked': identifier in self.blocked_ips
                })
        
        return sorted(suspects, key=lambda x: x['abuse_score'], reverse=True)
    
    def auto_block_abusers(self, threshold_score: int = 5) -> List[str]:
        """
        Automatically block abusive users
        
        Args:
            threshold_score: Minimum abuse score to block
            
        Returns:
            List of blocked identifiers
        """
        suspects = self.get_abuse_suspects()
        blocked = []
        
        for suspect in suspects:
            if suspect['abuse_score'] >= threshold_score and not suspect['is_blocked']:
                self.block_ip(
                    suspect['identifier'],
                    f"Auto-blocked: abuse score {suspect['abuse_score']}"
                )
                blocked.append(suspect['identifier'])
        
        return blocked
    
    def get_analytics(self, hours: int = 24) -> Dict:
        """Get comprehensive analytics"""
        return {
            'usage': self.get_usage_stats(hours=hours),
            'violations': {
                'total': len(self.get_violations(hours=hours)),
                'recent': self.get_violations(hours=1)
            },
            'abuse': {
                'suspects_count': len(self.get_abuse_suspects()),
                'blocked_count': len(self.blocked_ips),
                'top_suspects': self.get_abuse_suspects()[:5]
            },
            'limits': {
                'default': self.default_limits,
                'custom_users': len(self.user_limits),
                'custom_ips': len(self.ip_limits)
            }
        }
    
    def reset_identifier(self, identifier: str):
        """Reset request history for an identifier"""
        with self._lock:
            if identifier in self.requests:
                del self.requests[identifier]
    
    def cleanup_old_data(self, days: int = 7):
        """Cleanup old tracking data"""
        cutoff = time.time() - (days * 86400)
        
        with self._lock:
            # Clean requests
            for identifier in list(self.requests.keys()):
                self.requests[identifier] = [
                    ts for ts in self.requests[identifier]
                    if ts > cutoff
                ]
                
                if not self.requests[identifier]:
                    del self.requests[identifier]
            
            # Clean violations
            cutoff_dt = datetime.now() - timedelta(days=days)
            self.violations = [
                v for v in self.violations
                if v['timestamp'] > cutoff_dt
            ]


# Global rate limiter instance
rate_limiter = RateLimiter()
