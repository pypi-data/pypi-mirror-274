#!/usr/bin/env python
from setuptools import setup, find_packages

COMPANY_NAME="jaanca"
PACKAGE_NAME = "jaanca-chronometer"
VERSION = "0.1.2"

install_requires = []

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=f'A tool library created by {COMPANY_NAME} that allows measuring the time between two moments in the source code.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='MIT License',
    author='Andres Cardona',
    author_email='jacardona@outlook.com',
    url='https://github.com/jaanca/python-libraries/tree/main/jaanca-chronometer',
    keywords="timer stopwatch in interval format for databases",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=install_requires,
)
