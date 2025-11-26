import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.env.local')
os.environ.setdefault('DJANGORLAR_ENV_ID', 'local')

# Setup Django
if not settings.configured:
    django.setup()

# pytest configuration
pytest_plugins = []
