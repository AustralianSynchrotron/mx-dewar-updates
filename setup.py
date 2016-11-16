from setuptools import setup
import re

with open('dewarupdates/__init__.py') as file:
    version = re.search(r"__version__ = '(.*)'", file.read()).group(1)

setup(
    name='dewarupdates',
    version=version,
    packages=['dewarupdates'],
    install_requires=[
        'Flask',
        'Flask-Script',
        'requests',
        'pdfkit',
        'Flask-QRcode',
        'Flask-Bootstrap',
        'click',
        'MailShake',
        'jinja2',
    ],
    entry_points={
        'console_scripts': [
            'dewarupdates=dewarupdates.monitor:main',
        ],
    },
)
