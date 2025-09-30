#!/usr/bin/env python3
"""
Simple test Django app
"""
import os
import sys
import django
from django.conf import settings
from django.http import HttpResponse
from django.core.wsgi import get_wsgi_application

# Simple Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'productapi.settings')

try:
    django.setup()
    print("Django setup successful")
    
    def simple_view(request):
        return HttpResponse("Hello from Django!")
    
    # Test the view
    from django.test import RequestFactory
    factory = RequestFactory()
    request = factory.get('/')
    response = simple_view(request)
    print(f"View test successful: {response.content}")
    
except Exception as e:
    print(f"Django setup failed: {e}")
    import traceback
    traceback.print_exc()
