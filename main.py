import argparse

from config import Config
from gcredstash.keystore import KeyStore
from gcredstash.kms import GoogleKMS

__version__ = '1.0.0'

parser = argparse.ArgumentParser()
parser.add_argument(
    '--key-ring-id',
    default=Config.DEFAULT_KEY_RING_ID, dest='key_ring_id', type=str, help='Google Cloud KMS KeyRing Id')
parser.add_argument(
    '--crypto-key-id',
    default=Config.DEFAULT_CRYPTO_KEY_ID, dest='key_id', type=str, help='Google Cloud KMS CryptoKey Id')
parser.add_argument(
    '--location-id',
    default=Config.DEFAULT_LOCATION_ID, dest='location_id', type=str, help='Google Cloud KMS Location Id')
parser.add_argument(
    '--project-id',
    default=Config.PROJECT_ID, dest='project_id', type=str, help='GCP Project Id')
parser.add_argument('action', type=str, help='Vault operations',
                    choices=('put', 'get', 'getAll', 'putAll', 'list'))
parser.add_argument('name', type=str, nargs='?', help='The name of credential')
parser.add_argument('plaintext', type=str, nargs='?', help='Text to be encrypted')


def main():
    args = parser.parse_args()
    key_store = KeyStore(args.project_id)
    kms = GoogleKMS(args.project_id, args.location_id, args.key_ring_id, key_store)

    if args.action == "put":
        kms.put(args.key_id, Config.DEFAULT_DATASTORE_KIND, args.name, args.plaintext)
    elif args.action == "get":
        print kms.get(args.key_id, Config.DEFAULT_DATASTORE_KIND, args.name)
    elif args.action == "getAll":
        print kms.get_all(args.key_id, Config.DEFAULT_DATASTORE_KIND)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
