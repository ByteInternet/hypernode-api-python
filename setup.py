#!/usr/bin/env python
import os
from pathlib import Path

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
requirements = """
pip
requests
"""


setup(
    name="hypernode_api_python",
    version="0.0.3",
    description='"Hypernode API Client for Python"',
    url="https://github.com/ByteInternet/hypernode_api_python",
    packages=find_packages(
        include=["hypernode_api_python", "requirements/base.txt"], exclude=["tests"]
    ),
    author="Hypernode Team",
    author_email="support@hypernode.com",
    install_requires=requirements.split("\n"),
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
)
