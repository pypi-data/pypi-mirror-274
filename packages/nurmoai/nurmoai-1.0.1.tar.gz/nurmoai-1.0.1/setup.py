from setuptools import setup, find_packages

setup(
    name='nurmoai',
    version='1.0.1',
    author='Reksely',
    author_email='reksely@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    description='A Python client for the NurmoAI API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://nurmo.app',
)