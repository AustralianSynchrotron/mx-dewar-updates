from mxshipalerts.printer import page_to_pdf, print_file
from flask import url_for
from unittest.mock import call, patch
from PyPDF2 import PdfFileReader
from io import BytesIO


def test_page_to_pdf():
    with BytesIO() as file:
        page_to_pdf('https://httpbin.org/html', file)
        reader = PdfFileReader(file)
        assert reader.numPages >= 1


def test_print_file():
    with patch('subprocess.check_output') as check_output_mock:
        print_file('the-file.pdf', options=['InputSlot=Tray2'])
        expected_command = call(['lpr', '-o', 'InputSlot=Tray2', 'the-file.pdf'])
        assert check_output_mock.call_args == expected_command
