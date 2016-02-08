from mxshipalerts.printer import print_file, save_page
import pytest
import os
from vcr import VCR
from unittest.mock import call, patch


vcr = VCR(cassette_library_dir='tests/fixtures/cassettes')


@pytest.mark.skipif(True, reason='slow')
@vcr.use_cassette()
def test_save_page():
    filename = save_page('https://httpbin.org/html')
    assert os.path.exists(filename)
    assert os.stat(filename).st_size > 0


def test_print_file():
    with patch('subprocess.check_output') as check_output_mock:
        print_file('file.pdf', '-o', 'InputSlot=Tray2')
        expected_command = call(['lpr', '-o', 'InputSlot=Tray2', 'file.pdf'])
        assert check_output_mock.call_args == expected_command
