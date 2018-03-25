from __future__ import print_function
import base64
import logging


class GoogleKMS(object):
    PARENT_URI = 'projects/{project_id}/locations/{location_id}'
    KEY_RING_URI = PARENT_URI + '/keyRings/{key_ring_id}'
    KEY_URI = KEY_RING_URI + '/cryptoKeys/{key_id}'

    def __init__(self, client, project_id, location_id, key_ring_id, key_store):
        self.client = client
        self.project_id = project_id
        self.location_id = location_id
        self.key_ring_id = key_ring_id
        self.key_store = key_store

    def _encrypt(self, key_id, plain_text):
        """
        Encrypt text using the CryptoKey
        :param key_id: CryptKey id
        :param plain_text: Plain text for encryption
        :return: Cipher used for encryption
        """
        try:

            name = self._get_key_uri(key_id)

            crypto_keys = self._get_crypto_keys()
            request = crypto_keys.encrypt(
                name=name,
                body={'plaintext': base64.b64encode(plain_text.encode('utf8')).decode('utf8')}
            )

            response = request.execute()
            return response.get('ciphertext').encode('utf8')
        except Exception as e:
            logging.exception(e)

    def _decrypt(self, key_id, cipher):
        """
        Decrypt the credential using cipher text
        :param key_id: CryptKey id
        :param cipher: Cipher text for decrypting the encrypted credential
        :return: Decrypted text
        """
        try:
            name = self._get_key_uri(key_id)
            crypto_keys = self._get_crypto_keys()

            request = crypto_keys.decrypt(
                name=name,
                body={'ciphertext': cipher})
            response = request.execute()

            return base64.b64decode(response.get('plaintext').encode('utf8'))

        except Exception as e:
            logging.exception(e)

    def _get_crypto_keys(self):
        """
        Get Google KMS CryptKeys in the KeyRing
        :return: CryptoKeys
        """
        return self.client.projects().locations().keyRings().cryptoKeys()

    def _get_key_uri(self, key_id):
        """
        Get Google Cloud KMS resource id
        :param key_id: CryptKey id
        :return:
        """
        return GoogleKMS.KEY_URI.format(
            project_id=self.project_id,
            location_id=self.location_id,
            key_ring_id=self.key_ring_id,
            key_id=key_id,

        )

    def get(self, key_id, kind, name):
        """
        Get the cipher from KeyStore and decrypted the credential
        :param key_id: CryptKey id
        :param kind: Keystore collection name
        :param name: Name of the credential to fetch ex: PRODUCTION_DATABASE_PASSWORD
        :return: Decrypted text
        """

        if not isinstance(name, basestring):
            raise ValueError("name and value should be a string")

        cipher = self.key_store.get(kind, name)
        return self._decrypt(key_id, cipher)

    def put(self, key_id, kind, name, value):
        """
        Encrypt the credential and put the cipher on KeyStore
        :param key_id: CryptKey id
        :param kind: Keystore collection name
        :param name: Name of the credential to store ex: PRODUCTION_DATABASE_PASSWORD
        :param value: Value for the credential
        :return:
        """

        if not isinstance(name, basestring) or not isinstance(value, basestring):
            raise ValueError("name and value should be a string")

        cipher = self._encrypt(key_id, value)
        return self.key_store.put(kind, name, cipher)

    def put_all(self, key_id, kind, credentials):
        """
        Encrypt all the credential and store the cipher on KeyStore
        :param key_id: CryptKey id
        :param kind: Keystore collection name
        :param credentials: Credentials {name: value} dictionary

        :return:
        """

        if type(credentials) != dict:
            raise ValueError("credentials should be a dictionary of credential name and value")

        for name, value in credentials.items():
            self.put(key_id, kind, name, value)

    def get_all(self, key_id, kind):
        """
        Get the cipher from KeyStore and decrypted all the credentials
        :param key_id: CryptKey id
        :param kind: Keystore collection name

        :return: Dictionary of credentials
        """

        return {name: self.get(key_id, kind, name) for name in self.key_store.list(kind)}

    @staticmethod
    def create_key_ring(client, project_id, location_id, key_ring_id):
        """
        Creates a KeyRing in the given location (e.g. global)
        :param client: Google Cloud KMS client
        :param project_id: GCP Project id
        :param location_id: KeyRing location id
        :param key_ring_id: New unique key ring name
        :return: KeyRing creation response object
        """
        try:
            key_rings = client.projects().locations().keyRings()
            parent_uri = GoogleKMS.PARENT_URI.format(
                project_id=project_id,
                location_id=location_id
            )

            request = key_rings.create(parent=parent_uri, body={}, keyRingId=key_ring_id)
            return request.execute()
        except Exception as e:
            logging.exception(e)

    @staticmethod
    def create_key(client, project_id, location_id, key_ring_id, key_id):
        """
        Creates a CryptoKey within a KeyRing in the given location
        :param client: Google Cloud KMS client
        :param project_id: GCP Project id
        :param location_id: KeyRing location id
        :param key_ring_id: KeyRing id inside the location
        :param key_id:  New unique key name
        :return: Key creation response object
        """

        try:
            parent_uri = GoogleKMS.KEY_RING_URI.format(
                project_id=project_id,
                location_id=location_id,
                key_ring_id=key_ring_id
            )

            crypto_keys = client.projects().locations().keyRings().cryptoKeys()

            request = crypto_keys.create(
                parent=parent_uri, body={'purpose': 'ENCRYPT_DECRYPT'},
                cryptoKeyId=key_id)
            return request.execute()
        except Exception as e:
            logging.exception(e)
