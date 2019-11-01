from setuptools import setup

def read_readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='gcredstash',
    author='Rajesh Hegde',
    author_email="rajesh.p.hegde@gmail.com",
    version='1.0.2',
    description='A Credential Management Tool using Google Cloud KMS and Datastore',
    long_description=read_readme(),
    long_description_content_type="text/markdown",
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
