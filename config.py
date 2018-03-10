import os
import settings


class Config(object):
    PROJECT_ID = os.environ.get('PROJECT_ID')
    DEFAULT_KEY_RING_ID = os.environ.get('DEFAULT_KEY_RING_ID')
    DEFAULT_LOCATION_ID = os.environ.get('DEFAULT_LOCATION_ID')
    DEFAULT_CRYPTO_KEY_ID = os.environ.get('DEFAULT_CRYPTO_KEY_ID')
    DEFAULT_DATASTORE_KIND = os.environ.get('DEFAULT_DATASTORE_KIND')
