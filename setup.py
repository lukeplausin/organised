#!/usr/bin/env python

from setuptools import setup

setup(
    name='organized',
    version='0.1',
    author='Luke Plausin',
    # author_email=...,
    description_file='README.md',
    description_content_type='text/markdown',
    # long_description='Really, the funniest around.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='utilities python exif images library could documents organisation tidy organization',
    url='https://github.com/lukeplausin/organized',
    license='MIT',
    packages=['organized'],
    install_requires=[
        'pyexiftool', 'click', 'pyyaml',
    ],
    include_package_data=True,
    zip_safe=True,
    entry_points = {
        'console_scripts': [
            'organize=organized.cli:organize',
            'organise=organized.cli:organize',
            'org=organized.cli:organize',
        ],
    }
)
