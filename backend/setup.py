#!/usr/bin/env python

from setuptools import setup

setup(
    name="nomnombring-backend",
    version="0.0.1",
    author="tljuniper",
    author_email="48209000+tljuniper@users.noreply.github.com",
    description="Add recipes from book to Bring shopping list",
    packages=[
        'nomnombring',
    ],
    install_requires=[
        'flask',
        'flask-cors',
        'requests',
        'pip',
        'setuptools'
    ],
    entry_points={"console_scripts": ["nomnombring = nomnombring.main:main"]},
)
