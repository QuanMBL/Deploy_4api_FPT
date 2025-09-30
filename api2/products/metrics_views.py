from django.http import HttpResponse
from .middleware import get_metrics_data

def metrics_view(request):
    """Dynamic metrics endpoint that tracks real HTTP requests"""
    metrics_data = []
    data = get_metrics_data()
    
    # HTTP Request Metrics - Dynamic data
    metrics_data.append('# HELP django_http_requests_total Total HTTP requests')
    metrics_data.append('# TYPE django_http_requests_total counter')
    
    for key, count in data['http_requests_total'].items():
        if '_' in key:
            method, status = key.split('_', 1)
            metrics_data.append(f'django_http_requests_total{{job="{data["job"]}",method="{method}",status="{status}"}} {count}')
    
    # HTTP Request Duration - Dynamic data
    metrics_data.append('# HELP django_http_request_duration_seconds HTTP request duration')
    metrics_data.append('# TYPE django_http_request_duration_seconds histogram')
    
    duration_data = data['http_request_duration_seconds']
    if 'buckets' in duration_data:
        for bucket, count in duration_data['buckets'].items():
            metrics_data.append(f'django_http_request_duration_seconds_bucket{{le="{bucket}"}} {count}')
        metrics_data.append(f'django_http_request_duration_seconds_sum {duration_data.get("duration_sum", 0)}')
        metrics_data.append(f'django_http_request_duration_seconds_count {duration_data.get("duration_count", 0)}')
    
    # Process Metrics - Dynamic data
    metrics_data.append('# HELP process_resident_memory_bytes Resident memory size in bytes')
    metrics_data.append('# TYPE process_resident_memory_bytes gauge')
    metrics_data.append(f'process_resident_memory_bytes{{job="{data["job"]}"}} {data["process_resident_memory_bytes"]}')
    
    metrics_data.append('# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds')
    metrics_data.append('# TYPE process_cpu_seconds_total counter')
    metrics_data.append(f'process_cpu_seconds_total{{job="{data["job"]}"}} {data["process_cpu_seconds_total"]}')
    
    metrics_data.append('# HELP process_open_fds Number of open file descriptors')
    metrics_data.append('# TYPE process_open_fds gauge')
    metrics_data.append(f'process_open_fds{{job="{data["job"]}"}} {data["process_open_fds"]}')
    
    # System Metrics
    metrics_data.append('# HELP up Whether the service is up')
    metrics_data.append('# TYPE up gauge')
    metrics_data.append(f'up{{job="{data["job"]}"}} {data["up"]}')
    
    return HttpResponse('\n'.join(metrics_data), content_type='text/plain')
