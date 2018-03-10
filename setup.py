from setuptools import setup

setup(
    name='google-credstash',
    author='Rajesh Hegde',
    version='1.0.0',
    description='A Credential Management Tool using Google Cloud KMS and Datastore',
    url='https://github.com/RajeshHegde/google-credstash',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
    ],
    scripts=['google-credstash'],
    install_requires=[
        'google-api-python-client',
        'google-cloud-datastore',
        'google-auth-httplib2',
        'python-dotenv',
    ],
)
