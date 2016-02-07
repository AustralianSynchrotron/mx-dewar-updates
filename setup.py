from setuptools import setup
import re

with open('mxshipalerts/__init__.py') as file:
    version = re.search(r"__version__ = '(.*)'", file.read()).group(1)

setup(
    name='mxshipalerts',
    version=version,
    packages=['mxshipalerts'],
    install_requires=[],
)
