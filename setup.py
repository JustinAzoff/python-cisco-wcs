from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='cisco-wcs',
    version=version,
    description="Basic Cisco WCS web client",
    keywords='Cisco WCS',
    author='Justin Azoff',
    author_email='JAzoff@albany.edu',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    zip_safe=False,
    install_requires=[
        "requests",
        "pyquery",
    ],
)
