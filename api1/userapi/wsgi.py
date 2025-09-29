"""
WSGI config for userapi project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userapi.settings')

application = get_wsgi_application()
