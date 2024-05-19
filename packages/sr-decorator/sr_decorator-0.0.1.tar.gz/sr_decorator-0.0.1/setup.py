#!python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages
import sr_decorator

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="sr_decorator",
    version=sr_decorator.__version__,
    author="CivetWyan",
    author_email="wyan978826399@163.com",
    description="Some commonly used decorations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://blog.fcloud.host",
    py_modules=['sr_decorator'],
    install_requires=[

        ],
    classifiers=[
        "Topic :: Games/Entertainment ",
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Games/Entertainment :: Board Games',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)

