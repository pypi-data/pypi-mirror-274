from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='org-ds-cdk',
    version='0.1.06',
    description='Constructs for creating an API Gateway and Routes from input JSON configuration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    install_requires=[
        'aws-cdk-lib==2.142.0',
        'constructs>=10.0.0'
    ],
)