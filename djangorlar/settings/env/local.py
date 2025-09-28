from settings.base import *

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    {
        'default': 'django.db.sqlite3',
        'NAME': 'db.sqlite3',
    },
}
