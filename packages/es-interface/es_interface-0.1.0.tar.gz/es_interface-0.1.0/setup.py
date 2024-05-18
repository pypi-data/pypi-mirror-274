# setup.py

from setuptools import setup, find_packages

setup(
    name='es-interface',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'elasticsearch',
    ],
) 