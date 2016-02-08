from tempfile import NamedTemporaryFile
import pdfkit
import requests
import subprocess


def save_page(url):
    file = NamedTemporaryFile(delete=False, suffix='.pdf')
    response = requests.get(url)
    pdfkit.from_string(response.text, file.name)
    return file.name


def print_file(filename, *args):
    subprocess.check_output(['lpr', *args, 'file.pdf'])
