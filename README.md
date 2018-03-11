# Google CredStash

## Installation
1. `pip install gcredstash`

## Introduction


## Usage
### Command-line
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