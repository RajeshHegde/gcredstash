from setuptools import setup

setup(
    name='gcredstash',
    author='Rajesh Hegde',
    version='1.0.1',
    description='A Credential Management Tool using Google Cloud KMS and Datastore',
    url='https://github.com/RajeshHegde/gcredstash',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
    ],
    packages=['gcredstash'],
    install_requires=[
        'google-api-python-client>=1.6.5',
        'google-cloud-datastore>=1.6.0',
        'google-auth-httplib2>=0.0.3',
    ],
    entry_points={
        'console_scripts': [
            'gcredstash = gcredstash.main:main'
        ]
    }
)
