from mxshipalerts.printer import print_file, save_page
import pytest
import os


def test_save_page():
    filename = save_page('http://google.com')
    assert os.path.exists(filename)
    assert os.stat(filename).st_size > 0


@pytest.mark.skipif(True, reason='Not implemented')
def test_print_file():
    assert False
