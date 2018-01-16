from distutils.core import setup
import py2exe
import sys
import os

setup (
    console = [{'script': 'console.py'}],
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    zipfile = None,
)