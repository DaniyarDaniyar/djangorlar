# Project modules
from settings.base import *


DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backend.sqlite3',
        'NAME': 'db.sqlite3',
}
}