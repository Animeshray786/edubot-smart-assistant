"""
Performance Monitoring System
CPU, memory, disk usage, database query performance, bottleneck identification
"""
import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, List
from functools import wraps
import threading


class PerformanceMonitor:
    """Monitor system and application performance"""
    
    def __init__(self):
        self.metrics = {
            'requests': [],
            'queries': [],
            'endpoints': {},
            'errors': []
        }
        self.start_time = datetime.now()
        self._lock = threading.Lock()
    
    def get_system_metrics(self) -> Dict:
        """Get current system metrics"""
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu': {
                'percent': round(psutil.cpu_percent(interval=0.1), 2),
                'per_core': [round(p, 2) for p in cpu_percent],
                'cores': psutil.cpu_count(),
                'load_average': [round(x / psutil.cpu_count() * 100, 2) for x in psutil.getloadavg()] if hasattr(psutil, 'getloadavg') else []
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': round(memory.percent, 2),
                'total_gb': round(memory.total / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2)
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': round(disk.percent, 2),
                'total_gb': round(disk.total / (1024**3), 2),
                'free_gb': round(disk.free / (1024**3), 2)
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def get_process_metrics(self) -> Dict:
        """Get current process metrics"""
        process = psutil.Process()
        
        with process.oneshot():
            return {
                'pid': process.pid,
                'cpu_percent': round(process.cpu_percent(interval=0.1), 2),
                'memory_info': {
                    'rss': process.memory_info().rss,
                    'vms': process.memory_info().vms,
                    'rss_mb': round(process.memory_info().rss / (1024**2), 2)
                },
                'memory_percent': round(process.memory_percent(), 2),
                'threads': process.num_threads(),
                'open_files': len(process.open_files()),
                'connections': len(process.connections()),
                'create_time': datetime.fromtimestamp(process.create_time()).isoformat()
            }
    
    def track_request(self, endpoint: str, method: str, duration: float, 
                     status_code: int, user_id: int = None):
        """Track HTTP request"""
        with self._lock:
            request_data = {
                'endpoint': endpoint,
                'method': method,
                'duration': duration,
                'status_code': status_code,
                'user_id': user_id,
                'timestamp': datetime.now()
            }
            
            self.metrics['requests'].append(request_data)
            
            # Track endpoint statistics
            if endpoint not in self.metrics['endpoints']:
                self.metrics['endpoints'][endpoint] = {
                    'count': 0,
                    'total_duration': 0,
                    'errors': 0,
                    'methods': {}
                }
            
            self.metrics['endpoints'][endpoint]['count'] += 1
            self.metrics['endpoints'][endpoint]['total_duration'] += duration
            
            if status_code >= 400:
                self.metrics['endpoints'][endpoint]['errors'] += 1
            
            if method not in self.metrics['endpoints'][endpoint]['methods']:
                self.metrics['endpoints'][endpoint]['methods'][method] = 0
            
            self.metrics['endpoints'][endpoint]['methods'][method] += 1
            
            # Keep only last 1000 requests
            if len(self.metrics['requests']) > 1000:
                self.metrics['requests'] = self.metrics['requests'][-1000:]
    
    def track_db_query(self, query: str, duration: float, rows_affected: int = 0):
        """Track database query"""
        with self._lock:
            query_data = {
                'query': query[:200],  # Truncate long queries
                'duration': duration,
                'rows_affected': rows_affected,
                'timestamp': datetime.now()
            }
            
            self.metrics['queries'].append(query_data)
            
            # Keep only last 500 queries
            if len(self.metrics['queries']) > 500:
                self.metrics['queries'] = self.metrics['queries'][-500:]
    
    def track_error(self, error_type: str, message: str, endpoint: str = None):
        """Track application error"""
        with self._lock:
            error_data = {
                'type': error_type,
                'message': message,
                'endpoint': endpoint,
                'timestamp': datetime.now()
            }
            
            self.metrics['errors'].append(error_data)
            
            # Keep only last 200 errors
            if len(self.metrics['errors']) > 200:
                self.metrics['errors'] = self.metrics['errors'][-200:]
    
    def get_request_analytics(self, minutes: int = 60) -> Dict:
        """Get request analytics for last N minutes"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        recent_requests = [r for r in self.metrics['requests'] if r['timestamp'] > cutoff]
        
        if not recent_requests:
            return {
                'total_requests': 0,
                'avg_response_time': 0,
                'requests_per_minute': 0,
                'error_rate': 0
            }
        
        total = len(recent_requests)
        avg_duration = sum(r['duration'] for r in recent_requests) / total
        errors = sum(1 for r in recent_requests if r['status_code'] >= 400)
        
        return {
            'total_requests': total,
            'avg_response_time': round(avg_duration, 3),
            'requests_per_minute': round(total / minutes, 2),
            'error_rate': round((errors / total) * 100, 2) if total > 0 else 0,
            'by_status': self._count_by_status(recent_requests),
            'by_method': self._count_by_method(recent_requests)
        }
    
    def _count_by_status(self, requests: List[Dict]) -> Dict:
        """Count requests by status code"""
        counts = {}
        for r in requests:
            code = r['status_code']
            category = f"{code // 100}xx"
            counts[category] = counts.get(category, 0) + 1
        return counts
    
    def _count_by_method(self, requests: List[Dict]) -> Dict:
        """Count requests by HTTP method"""
        counts = {}
        for r in requests:
            method = r['method']
            counts[method] = counts.get(method, 0) + 1
        return counts
    
    def get_slow_endpoints(self, threshold_ms: float = 1000, limit: int = 10) -> List[Dict]:
        """Get slowest endpoints"""
        endpoint_stats = []
        
        for endpoint, stats in self.metrics['endpoints'].items():
            if stats['count'] > 0:
                avg_duration = (stats['total_duration'] / stats['count']) * 1000  # Convert to ms
                
                if avg_duration >= threshold_ms:
                    endpoint_stats.append({
                        'endpoint': endpoint,
                        'avg_duration_ms': round(avg_duration, 2),
                        'count': stats['count'],
                        'error_rate': round((stats['errors'] / stats['count']) * 100, 2),
                        'total_time_seconds': round(stats['total_duration'], 2)
                    })
        
        return sorted(endpoint_stats, key=lambda x: x['avg_duration_ms'], reverse=True)[:limit]
    
    def get_slow_queries(self, threshold_ms: float = 100, limit: int = 10) -> List[Dict]:
        """Get slowest database queries"""
        slow_queries = [
            {
                'query': q['query'],
                'duration_ms': round(q['duration'] * 1000, 2),
                'rows_affected': q['rows_affected'],
                'timestamp': q['timestamp'].isoformat()
            }
            for q in self.metrics['queries']
            if q['duration'] * 1000 >= threshold_ms
        ]
        
        return sorted(slow_queries, key=lambda x: x['duration_ms'], reverse=True)[:limit]
    
    def get_error_summary(self, hours: int = 24) -> Dict:
        """Get error summary"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_errors = [e for e in self.metrics['errors'] if e['timestamp'] > cutoff]
        
        by_type = {}
        by_endpoint = {}
        
        for error in recent_errors:
            by_type[error['type']] = by_type.get(error['type'], 0) + 1
            
            if error['endpoint']:
                by_endpoint[error['endpoint']] = by_endpoint.get(error['endpoint'], 0) + 1
        
        return {
            'total_errors': len(recent_errors),
            'by_type': by_type,
            'by_endpoint': by_endpoint,
            'recent_errors': recent_errors[-10:]  # Last 10 errors
        }
    
    def get_bottlenecks(self) -> Dict:
        """Identify performance bottlenecks"""
        system = self.get_system_metrics()
        process = self.get_process_metrics()
        slow_endpoints = self.get_slow_endpoints(threshold_ms=500)
        slow_queries = self.get_slow_queries(threshold_ms=50)
        
        bottlenecks = []
        
        # CPU bottleneck
        if system['cpu']['percent'] > 80:
            bottlenecks.append({
                'type': 'CPU',
                'severity': 'high',
                'message': f"CPU usage is {system['cpu']['percent']}%",
                'recommendation': 'Consider optimizing CPU-intensive operations or scaling horizontally'
            })
        
        # Memory bottleneck
        if system['memory']['percent'] > 85:
            bottlenecks.append({
                'type': 'Memory',
                'severity': 'high',
                'message': f"Memory usage is {system['memory']['percent']}%",
                'recommendation': 'Check for memory leaks or increase available memory'
            })
        
        # Disk bottleneck
        if system['disk']['percent'] > 90:
            bottlenecks.append({
                'type': 'Disk',
                'severity': 'critical',
                'message': f"Disk usage is {system['disk']['percent']}%",
                'recommendation': 'Clean up disk space immediately or add more storage'
            })
        
        # Slow endpoints
        if slow_endpoints:
            bottlenecks.append({
                'type': 'Slow Endpoints',
                'severity': 'medium',
                'message': f"Found {len(slow_endpoints)} slow endpoints",
                'details': slow_endpoints[:3],
                'recommendation': 'Optimize these endpoints or add caching'
            })
        
        # Slow queries
        if slow_queries:
            bottlenecks.append({
                'type': 'Slow Queries',
                'severity': 'medium',
                'message': f"Found {len(slow_queries)} slow database queries",
                'details': slow_queries[:3],
                'recommendation': 'Add database indexes or optimize queries'
            })
        
        return {
            'total_bottlenecks': len(bottlenecks),
            'bottlenecks': bottlenecks,
            'system_health': 'critical' if any(b['severity'] == 'critical' for b in bottlenecks) else
                           'warning' if bottlenecks else 'healthy'
        }
    
    def get_uptime(self) -> Dict:
        """Get application uptime"""
        uptime = datetime.now() - self.start_time
        
        return {
            'started_at': self.start_time.isoformat(),
            'uptime_seconds': uptime.total_seconds(),
            'uptime_formatted': str(uptime).split('.')[0],  # Remove microseconds
            'uptime_days': uptime.days,
            'uptime_hours': uptime.seconds // 3600
        }
    
    def reset_metrics(self):
        """Reset all metrics"""
        with self._lock:
            self.metrics = {
                'requests': [],
                'queries': [],
                'endpoints': {},
                'errors': []
            }


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def track_performance(func):
    """Decorator to track function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            performance_monitor.track_error(
                error_type=type(e).__name__,
                message=str(e),
                endpoint=func.__name__
            )
            raise
        finally:
            duration = time.time() - start_time
            performance_monitor.track_request(
                endpoint=func.__name__,
                method='FUNCTION',
                duration=duration,
                status_code=200
            )
    
    return wrapper
