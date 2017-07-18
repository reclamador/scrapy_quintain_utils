#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

setup_requirements = [
    'Scrapy==1.4.0',
    'pymongo==3.4.0',
    'scrapy-splash==0.7.2',
    'boto3==1.4.4'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='scrapy_quintain_utils',
    version='0.1.0',
    description="Scrapy utils to create scrapers fast",
    long_description=readme + '\n\n' + history,
    author="Juan Madurga",
    author_email='jlmadurga@gmail.com',
    url='https://github.com/jlmadurga/scrapy_quintain_utils',
    packages=['scrapy_quintain_utils', 'scrapy_quintain_utils.pipelines'],
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='scrapy_quintain_utils',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
