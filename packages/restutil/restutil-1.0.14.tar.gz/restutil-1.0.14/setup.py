#! usr/bin/python
# -*- coding: utf-8 *-*

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

from pathlib import Path

root_dir = Path(__file__).parent
long_description = (root_dir / "README.md").read_text()

setup(
    name='restutil',
    packages=find_packages(exclude=["tests*"]),
    version='1.0.14',
    description='Rest util and common tools',
    author='Adonis Gonzalez Godoy',
    author_email='adions025@gmail.com',
    url='https://github.com/adions025/restutil',
    download_url='https://github.com/adions025/restutil',
    keywords=['Restfull', 'Rest', 'Util', 'Tools, Logger'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
