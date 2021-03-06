from distutils.core import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
import sys
import os.path

PACKAGE = "pyfeature"
NAME = "pyfeature"
DESCRIPTION = "Inspired by lettuce, but be more pythonic!"
AUTHOR = "xiechao"
AUTHOR_EMAIL = "xiechao06@gmail.com"
VERSION = "0.9.0"
URL = ""
DOC = __doc__

setup(
    name=NAME,
    version=VERSION,
    long_description=__doc__,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    py_modules=["pyfeature"],
    include_package_data=True,
    zip_safe=False,
    install_requires=["twill>=0.9"],
    scripts=['scripts/pyfeature_step_gen.py', 'scripts/pyfeature_reader.py']
)

