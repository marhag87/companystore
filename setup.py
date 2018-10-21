#!/bin/env python
"""
Setuptools file for companystore
"""
from setuptools import (
    setup,
    find_packages,
)

setup(
    name='companystore',
    author='marhag87',
    author_email='marhag87@gmail.com',
    url='https://github.com/marhag87/companystore',
    version='0.1.0',
    packages=find_packages(),
    license='WTFPL',
    description='Keep track of companies, products and orders',
    long_description='A backend web application for keeping track of companies, products and orders',
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
    ],
    extras_require={
        'test': [
            'pytest',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
    ],
)
