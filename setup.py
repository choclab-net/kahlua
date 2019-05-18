#!/usr/bin/env python3

from setuptools import setup

setup(
    name='kahlua',
    version='0.1.0',
    description='Website for Kahlua the chocolate Labrador',
    author='Martin Proffitt',
    author_email='mproffitt@choclab.net',
    license='MIT',
    url='https://kahlua.choclab.net',
    python_requires='>=3.7.0',
    package_dir={
        'kahlua': 'kahlua',
        'home': 'home',
        'search': 'search'
    },
    packages=[
        'home',
        'kahlua',
        'search'
    ],
    install_requires=[
        'Django',
        'wagtail',
        'wagtail-blog'
    ],
)
