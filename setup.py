from setuptools import setup

setup(
    name='google-credstash',
    version='1.0.0',
    description='A utility for managing secrets in Google Cloud KMS and Datastore',
    url='https://github.com/RajeshHegde/google-credstash',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
    ],
    scripts=['main.py'],
    install_requires=[
        'google-api-python-client',
        'google-cloud-datastore',
        'google-auth-httplib2',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'google-credstash = google-credstash:main'
        ]
    }
)
