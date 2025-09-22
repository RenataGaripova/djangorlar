# Project modules
from decouple import config

# ----------------------------------------------
# Env id
#
ENV_POSSIBLE_OPTIONS = (
    'local',
    'prod',
)
ENV_ID = config('DJANGORlAR_ENV_ID', cast=str)
SECRET_KEY = 'django-insecure-g^do)(_9-5+^#zcnxs&ykel^fo3*oq-#8oo9jmvc^_r7@j!@-e'
