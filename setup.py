#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

try:
    from setuptools import setup, find_packages
except ImportError:
    msg = "Payday needs setuptools in order to build. Install it using your " +\
          "package manager (usually python-setuptools) or via pip (pip " +\
          "install setuptools)."
    raise SystemExit(msg)

BASEDIR = os.path.dirname(__file__)

with open(os.path.join(BASEDIR, 'payday', '__init__.py'), 'r') as f:
    PACKAGE_INIT = f.read()

VERSION = re.compile(
    r".*__version__ = '(.*?)'", re.S).match(PACKAGE_INIT).group(1)

AUTHOR = re.compile(
    r".*__author__ = '(.*?)'", re.S).match(PACKAGE_INIT).group(1)

with open(os.path.join(BASEDIR, 'README.rst'), 'r') as f:
    README = f.read()

with open(os.path.join(BASEDIR, 'CHANGELOG.rst'), 'r') as f:
    CHANGELOG = f.read()

setup(
    name='payday',
    packages=find_packages('.'),
    version=VERSION,
    description='Radically simple invoice generator',
    author=AUTHOR,
    author_email='@'.join(("paul", "spurious.biz")),  # avoid spam,
    url='https://paul.spurious.biz/',
    license='MIT',
    install_requires=[
        'PyYAML',
        'jinja2',
        'setuptools',
        # 'watchdog',  # should be optional for debugging templates
        'webassets'],  # essential for including pictures in PDFs
    package_data={
        # '': ['module_utils/*.ps1'],
    },
    entry_points=("""
      [console_scripts]
      payday-invoice=payday.cli.invoice:main
      payday-client=payday.cli.client:main
    """),
    data_files=[],
    test_suite='payday.tests',
    tests_require='pep8>=1.3',
)
