import os


class Config(object):
    PROJECT_ID = os.environ.get('GCREDSTASH_GCP_PROJECT_ID')
    DEFAULT_KEY_RING_ID = os.environ.get('GCREDSTASH_DEFAULT_KEY_RING_ID')
    DEFAULT_LOCATION_ID = os.environ.get('GCREDSTASH_DEFAULT_LOCATION_ID') or "global"
    DEFAULT_CRYPTO_KEY_ID = os.environ.get('GCREDSTASH_DEFAULT_CRYPTO_KEY_ID')
    DEFAULT_DATASTORE_KIND = os.environ.get('GCREDSTASH_DEFAULT_DATASTORE_KIND') or "Credentials"
