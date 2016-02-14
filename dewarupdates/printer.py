import pdfkit
from tempfile import NamedTemporaryFile
import subprocess
from itertools import chain


def page_to_pdf(url, file):
    file.write(pdfkit.from_url(url, False))


def print_file(filename, *, options=None):
    if options is None:
        options = []
    options = chain.from_iterable(('-o', option) for option in options)
    subprocess.check_output(['lpr', *options, filename])


def print_page(url):
    with NamedTemporaryFile(suffix='.pdf') as file:
        print('Printing to %s' % file.name)
        page_to_pdf(url, file)
        print_file(file.name, options=['InputSlot=Tray2'])
