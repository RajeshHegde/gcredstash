# Google CredStash

## Installation
1. `pip install gcredstash`

## Dependencies
`gcredstash` uses following Google Cloud services
* Google Cloud KMS
* Google Datastore

Make sure `gcredstash` have access to the above services.


## Introduction
Software systems often need access to some shared credential. For example, your web application needs access to a database password, or an API key for some third party service.

Google CredStash is a very simple, easy to use credential management and distribution system that uses Google Cloud Key Management Service (KMS) for key storage, and Datastore for credential storage.

## Usage
### Command-line
#### Create KeyRing
`gcredstash --project-id=<gcp-project-id> --location-id=global create-keyring <your-first-keyring-name>`

#### Create CryptoKey in KeyRing
`gcredstash --project-id=<gcp-project-id> --location-id=global --keyring-id=<your-keyring-name>  create-key `<your-first-key-name>

#### Command-line reference 
```
usage: gcredstash [-h] [--project-id PROJECT_ID] [--location-id LOCATION_ID]
               [--keyring-id KEY_RING_ID] [--key-id KEY_ID]
               {create-keyring,create-key,get,put,get-all,list} ...

A Credential Management Tool using Google Cloud KMS and Datastore

positional arguments:
  {create-keyring,create-key,get,put,get-all,list}
                        Try commands like "gcredstash get -h" to get sub command's options
    create-keyring      Creates a KeyRing in the given location (e.g. global)
    create-key          Creates a CryptoKey within a KeyRing in the given
                        location
    get                 Get the cipher from KeyStore and decrypted the
                        credential
    put                 Encrypt the credential and put the cipher on KeyStore
    get-all             Get the cipher from KeyStore and decrypted all the
                        credentials

optional arguments:
  -h, --help            show this help message and exit
  --project-id PROJECT_ID
                        GCP Project Id
  --location-id LOCATION_ID
                        Google Cloud KMS Location Id
  --keyring-id KEY_RING_ID
                        Google Cloud KMS KeyRing Id
  --key-id KEY_ID       Google Cloud KMS CryptoKey Id


```

#### Set default values in ENV
You can set the default values for project_id, location etc in ENV and `gcredstash` is coded to read those variables,
Here is the list of variables `gcredstash` recognises,

```
GCREDSTASH_GCP_PROJECT_ID
GCREDSTASH_DEFAULT_KEY_RING_ID
GCREDSTASH_DEFAULT_LOCATION_ID
GCREDSTASH_DEFAULT_CRYPTO_KEY_ID
GCREDSTASH_DEFAULT_DATASTORE_KIND
```

### Python Package
```
# import statements
from gcredstash import GoogleKMS
from gcredstash import KeyStore
import googleapiclient.discovery

# create keystore instance
key_store = KeyStore()

# create google kms api client 
kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

# create kms instance
kms = GoogleKMS(kms_client, '<project-id>', '<location-id>', '<keyring-id>', key_store)
 
# store credential
kms.put(<crypto-key-id>, <datastore-kind>, <credential-name>, <credential-plaintext>)

```

#### Class References
```
class KeyStore(__builtin__.object)
    Methods defined here:
    
    __init__(self, project_id=None, namespace=None)
    
    get(self, kind, name)
        Get value associated with the name from Datastore
        :param kind: Collection name
        :param name: Datastore key
        :return: str
    
    list(self, kind)
        :param kind: Collection name
        :return: list of Datastore keys
    
    put(self, kind, name, content)
        Put value on the Datastore
        :param kind: Collection name
        :param name: Datastore key
        :param content: value to store
        :return:


class GoogleKMS(__builtin__.object)
    Methods defined here:
    
    __init__(self, client, project_id, location_id, key_ring_id, key_store)
    
    get(self, key_id, kind, name)
        Get the cipher from KeyStore and decrypted the credential
        :param key_id: CryptKey id
        :param kind: Keystore collection name
        :param name: Name of the credential to fetch ex: PRODUCTION_DATABASE_PASSWORD
        :return: Decrypted text
    
    get_all(self, key_id, kind)
        Get the cipher from KeyStore and decrypted all the credentials
        :param key_id: CryptKey id
        :param kind: Keystore collection name
        
        :return: Dictionary of credentials
    
    put(self, key_id, kind, name, value)
        Encrypt the credential and put the cipher on KeyStore
        :param key_id: CryptKey id
        :param kind: Keystore collection name
        :param name: Name of the credential to store ex: PRODUCTION_DATABASE_PASSWORD
        :param value: Value for the credential
        :return:
    
    put_all(self, key_id, kind, credentials)
        Encrypt all the credential and store the cipher on KeyStore
        :param key_id: CryptKey id
        :param kind: Keystore collection name
        :param credentials: Credentials {name: value} dictionary
        
        :return:
    
    ----------------------------------------------------------------------
    Static methods defined here:
    
    create_key(client, project_id, location_id, key_ring_id, key_id)
        Creates a CryptoKey within a KeyRing in the given location
        :param client: Google Cloud KMS client
        :param project_id: GCP Project id
        :param location_id: KeyRing location id
        :param key_ring_id: KeyRing id inside the location
        :param key_id: New unique key name
        :return: Key creation response object
    
    create_key_ring(client, project_id, location_id, key_ring_id)
        Creates a KeyRing in the given location (e.g. global)
        :param client: Google Cloud KMS client
        :param project_id: GCP Project Id
        :param location_id: KeyRing location id
        :param key_ring_id: New unique key ring name
        :return: KeyRing creation response object
```

## Credits
Following open source projects are inspiration to this,
* https://github.com/fugue/credstash
* https://github.com/tly1980/gcreds