from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
   name='python-queue-reader',
   version='1.0',
   description='Queue reader for python abstracting message brokers such as RabbitMQ', 
   author='uug.ai',
   author_email='', #TODO: Add email
   long_description=open('README.md').read(),
   long_description_content_type='text/markdown',
   packages=['python-queue-reader'],
   install_requires=requirements
)