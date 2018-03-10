from google.cloud import datastore


class KeyStore(object):
    CIPHER_PROPERTY_KEY = 'cipher'

    def __init__(self, project_id=None, namespace=None):
        self.client = datastore.Client(project=project_id, namespace=namespace)

    def get(self, kind, name):
        key = self.client.key(kind, name)

        entity = self.client.get(key)
        if not entity:
            return None

        return entity.get(KeyStore.CIPHER_PROPERTY_KEY)

    def put(self, kind, name, content):
        key = self.client.key(kind, name)
        entity = datastore.Entity(key=key, exclude_from_indexes=(KeyStore.CIPHER_PROPERTY_KEY,))
        entity[KeyStore.CIPHER_PROPERTY_KEY] = content
        self.client.put(entity)

    def list(self, kind):
        return [c.key.name for c in self.client.query(kind=kind).fetch()]
