import base64
import logging

import googleapiclient.discovery


class GoogleKMS(object):
    def __init__(self, project_id, location, key_ring_id, key_store):
        self.key_store = key_store
        self.client = googleapiclient.discovery.build('cloudkms', 'v1')
        self.parent_resource_uri = 'projects/{project_id}/locations/{location}/keyRings/{key_ring_id}'.format(
            project_id=project_id,
            location=location,
            key_ring_id=key_ring_id
        )

        self.resource_uri = self.parent_resource_uri + '/cryptoKeys/{key_id}'

    def _encrypt(self, key_id, plain_text):
        """
        Encrypt text using the CryptoKey
        :param key_id: CryptKey id
        :param plain_text: Plain text for encryption
        :return: Cipher used for encryption
        """
        try:

            name = self.resource_uri.format(key_id=key_id)

            crypto_keys = self.get_crypto_keys()
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
            name = self.resource_uri.format(key_id=key_id)
            crypto_keys = self.get_crypto_keys()

            request = crypto_keys.decrypt(
                name=name,
                body={'ciphertext': cipher})
            response = request.execute()

            return base64.b64decode(response.get('plaintext').encode('utf8'))

        except Exception as e:
            logging.exception(e)

    def get_crypto_keys(self):
        """
        Get Google KMS CryptKeys in the KeyRing
        :return: CryptoKeys
        """
        return self.client.projects().locations().keyRings().cryptoKeys()

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

        for name, value in credentials.iteritems():
            self.put(key_id, kind, name, value)

    def get_all(self, key_id, kind):
        """
        Get the cipher from KeyStore and decrypted all the credentials
        :param key_id: CryptKey id
        :param kind: Keystore collection name

        :return: Dictionary of credentials
        """

        return {name: self.get(key_id, kind, name) for name in self.key_store.list(kind)}

