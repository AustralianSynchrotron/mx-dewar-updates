import pdfkit
import subprocess
from itertools import chain


def page_to_pdf(url, file):
    file.write(pdfkit.from_url(url, False))


def print_file(filename, options=None):
    if options is None:
        options = []
    options = chain.from_iterable(('-o', option) for option in options)
    subprocess.check_output(['lpr', *options, filename])
