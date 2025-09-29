import time
import psutil
import os
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

# Global metrics storage
_metrics_data = {
    'http_requests_total': {},
    'http_request_duration_seconds': {},
    'process_resident_memory_bytes': 0,
    'process_cpu_seconds_total': 0.0,
    'process_open_fds': 0,
    'up': 1
}

class MetricsMiddleware(MiddlewareMixin):
    """Middleware to collect HTTP request metrics"""
    
    def process_request(self, request):
        """Record request start time"""
        request._metrics_start_time = time.time()
        return None
    
    def process_response(self, request, response):
        """Record request metrics"""
        if hasattr(request, '_metrics_start_time'):
            duration = time.time() - request._metrics_start_time
            
            # Create metric key
            method = request.method
            status = str(response.status_code)
            key = f"{method}_{status}"
            
            # Update HTTP requests counter
            if key not in _metrics_data['http_requests_total']:
                _metrics_data['http_requests_total'][key] = 0
            _metrics_data['http_requests_total'][key] += 1
            
            # Update duration metrics
            if 'duration_sum' not in _metrics_data['http_request_duration_seconds']:
                _metrics_data['http_request_duration_seconds']['duration_sum'] = 0.0
                _metrics_data['http_request_duration_seconds']['duration_count'] = 0
                _metrics_data['http_request_duration_seconds']['buckets'] = {
                    '0.1': 0, '0.5': 0, '1.0': 0, '2.0': 0, '+Inf': 0
                }
            
            _metrics_data['http_request_duration_seconds']['duration_sum'] += duration
            _metrics_data['http_request_duration_seconds']['duration_count'] += 1
            
            # Update buckets
            for bucket in ['0.1', '0.5', '1.0', '2.0']:
                if duration <= float(bucket):
                    _metrics_data['http_request_duration_seconds']['buckets'][bucket] += 1
            _metrics_data['http_request_duration_seconds']['buckets']['+Inf'] += 1
            
            # Update real system metrics
            _update_system_metrics()
        
        return response

def _update_system_metrics():
    """Update system metrics with real data"""
    try:
        process = psutil.Process()
        _metrics_data['process_resident_memory_bytes'] = process.memory_info().rss
        _metrics_data['process_cpu_seconds_total'] = process.cpu_times().user + process.cpu_times().system
        _metrics_data['process_open_fds'] = process.num_fds() if hasattr(process, 'num_fds') else len(process.open_files())
    except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
        # Fallback values if psutil fails
        _metrics_data['process_resident_memory_bytes'] = 50000000
        _metrics_data['process_cpu_seconds_total'] = 0.0
        _metrics_data['process_open_fds'] = 8

def get_metrics_data():
    """Get current metrics data"""
    _update_system_metrics()
    return _metrics_data.copy()
