import logging
import json
import socket
from datetime import datetime

class LogstashHandler(logging.Handler):
    def __init__(self, host='logstash', port=5000):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def emit(self, record):
        try:
            log_entry = {
                '@timestamp': datetime.utcnow().isoformat(),
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'service': getattr(record, 'service', 'unknown'),
                'environment': getattr(record, 'environment', 'development'),
                'host': socket.gethostname(),
                'pid': record.process,
                'thread': record.thread,
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            }
            
            # Add extra fields if they exist
            if hasattr(record, 'extra_fields'):
                log_entry.update(record.extra_fields)
            
            # Send to Logstash
            self.sock.sendto(
                json.dumps(log_entry).encode('utf-8'),
                (self.host, self.port)
            )
        except Exception:
            self.handleError(record)

# Django logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] [{process:d}] [{levelname}] {message}',
            'style': '{',
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'logstash': {
            'class': 'logging_django_logstash.LogstashHandler',
            'host': 'logstash',
            'port': 5000,
            'formatter': 'json',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/app/logs/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logstash', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'logstash', 'file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'api': {
            'handlers': ['console', 'logstash', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console', 'logstash', 'file'],
        'level': 'INFO',
    },
}
