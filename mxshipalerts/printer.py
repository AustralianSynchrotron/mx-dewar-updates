from tempfile import NamedTemporaryFile

def save_page(url):
    file = NamedTemporaryFile(delete=False)
    return file.name


def print_file():
    pass
