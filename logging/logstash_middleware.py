import logging
import json
import socket
import time
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

class LogstashMiddleware(MiddlewareMixin):
    """Middleware to send logs to Logstash"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('api')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.logstash_host = 'logstash'
        self.logstash_port = 5000
        
    def process_request(self, request):
        request._logstash_start_time = time.time()
        return None
    
    def process_response(self, request, response):
        if hasattr(request, '_logstash_start_time'):
            duration = time.time() - request._logstash_start_time
            
            # Create log entry
            log_entry = {
                '@timestamp': datetime.utcnow().isoformat(),
                'level': 'INFO',
                'logger': 'api',
                'message': f"{request.method} {request.path} - {response.status_code}",
                'service': self.get_service_name(request.path),
                'environment': 'development',
                'host': socket.gethostname(),
                'http': {
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                    'response_time_ms': round(duration * 1000, 2),
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    'remote_addr': self.get_client_ip(request),
                },
                'request': {
                    'method': request.method,
                    'path': request.path,
                    'query_string': request.META.get('QUERY_STRING', ''),
                    'content_type': request.META.get('CONTENT_TYPE', ''),
                    'content_length': request.META.get('CONTENT_LENGTH', 0),
                },
                'response': {
                    'status_code': response.status_code,
                    'content_type': response.get('Content-Type', ''),
                    'content_length': len(response.content) if hasattr(response, 'content') else 0,
                },
                'performance': {
                    'duration_ms': round(duration * 1000, 2),
                    'duration_seconds': round(duration, 3),
                }
            }
            
            # Add error information if status >= 400
            if response.status_code >= 400:
                log_entry['level'] = 'ERROR'
                log_entry['error'] = {
                    'status_code': response.status_code,
                    'message': f"HTTP {response.status_code}",
                }
            
            # Send to Logstash
            try:
                self.sock.sendto(
                    json.dumps(log_entry).encode('utf-8'),
                    (self.logstash_host, self.logstash_port)
                )
            except Exception as e:
                self.logger.error(f"Failed to send log to Logstash: {e}")
        
        return response
    
    def get_service_name(self, path):
        """Determine service name from request path"""
        if '/api/users/' in path:
            return 'user-api'
        elif '/api/products/' in path:
            return 'product-api'
        elif '/api/orders/' in path:
            return 'order-api'
        elif '/api/payments/' in path:
            return 'payment-api'
        else:
            return 'unknown'
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
