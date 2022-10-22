#!/usr/bin/env python
from setuptools import setup
from os.path import abspath, dirname, join


def readfile(filename):
    path = join(dirname(abspath(__file__)), filename)
    with open(path, 'rt') as filehandle:
        return filehandle.read()


setup(
    name='hypernode_api_python',
    version='0.0.1',
    description='"Hypernode API Client for Python"',
    long_description=readfile('README.md'),
    long_description_content_type='text/markdown',
    author='Hypernode',
    author_email='support@hypernode.com',
    license='MIT',
    url='https://github.com/ByteInternet/hypernode_api_python',
    packages=['hypernode_api_python'],
    install_requires=['pip'],
    entry_points={
        'console_scripts': []
    }
)
