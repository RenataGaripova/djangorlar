from settings.base import *

DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    {
        'default': 'django.db.sqlite3',
        'NAME': 'db.sqlite3',
    },
}
