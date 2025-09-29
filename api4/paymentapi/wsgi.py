"""
WSGI config for paymentapi project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paymentapi.settings')

application = get_wsgi_application()
