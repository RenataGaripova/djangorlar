# Project modules
import os

from decouple import config

# ----------------------------------------------
# Env id
#
ENV_POSSIBLE_OPTIONS = (
    'local',
    'prod',
)
ENV_ID = config('DJANGORlAR_ENV_ID', cast=str)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
