from dewarupdates.printer import page_to_pdf
from flask import url_for
from bs4 import BeautifulSoup
from PIL import Image
from base64 import b64decode
import zbarlight
from PyPDF2 import PdfFileReader
from io import BytesIO
import json
from vcr import VCR


vcr = VCR(cassette_library_dir='tests/fixtures/cassettes')


def decode_img(img):
    src = img['src']
    encoded_data = src.split(',')[1]
    image = Image.open(BytesIO(b64decode(encoded_data)))
    return image


def load_qrcode(image):
    code = zbarlight.scan_codes('qrcode', image)[0]
    return json.loads(code.decode('utf-8'))


@vcr.use_cassette()
def test_get_dewar_arrival_page(client, db):
    db.clear()
    db.add_dewar({
        'name': 'd-123a-1',
        'owner': 'Jane',
        'department': 'Chemistry',
        'institute': 'Some University',
        'streetAddress': '123 Main Road',
        'city': 'Brisbane',
        'state': 'Queensland',
        'postcode': '3000',
        'country': 'Australia',
        'phone': '111-222-333',
        'email': 'jane@example.com',
        'epn': '123a',
        'experimentStartTime': '2017-01-02T03:04:05',
        'beamline': 'MX1',
        'returnDewar': True,
        'courier': 'Fast Deliveries',
        'courierAccount': '999',
        'container_type': 'pucks',
        'expectedContainers': '1 | 2 | 3 | 4 | 5 |  |  | ',
    })
    response = client.get(url_for('main.arrival_slip', dewar_name='d-123a-1'))
    assert response.status_code == 200
    page = BeautifulSoup(response.data, 'html.parser')
    assert 'Jane' in page.find(id='owner').text == 'Jane'
    assert 'Chemistry' in page.find(id='department').text
    assert 'Some University' in page.find(id='institute').text
    assert '123 Main Road' in page.find(id='street_address').text
    assert 'Brisbane' in page.find(id='city').text
    assert 'Queensland' in page.find(id='state').text
    assert '3000' in page.find(id='postcode').text
    assert 'Australia' in page.find(id='country').text
    assert '111-222-333' in page.find(id='phone').text
    assert 'jane@example.com' in page.find(id='email').text
    assert '123a' in page.find(id='epn').text
    assert '2017-01-02 03:04' in page.find(id='start_time').text
    assert 'MX1' in page.find(id='beamline').text
    assert 'd-123a-1' in page.find(id='name').text
    assert 'User wants samples returned by courier' in page.text
    assert 'Fast Deliveries' in page.find(id='courier').text
    assert '999' in page.find(id='courier_account').text
    assert '1 | 2 | 3 | 4 | 5 |  |  | ' in page.find(id='containers').text


@vcr.use_cassette()
def test_arrival_slip_returns_404_when_dewar_doesnt_exist(client):
    response = client.get(url_for('main.arrival_slip', dewar_name='not-a-dewar'))
    assert response.status_code == 404


@vcr.use_cassette()
def test_renders_qr_codes(client, db):
    db.clear()
    db.add_dewar({'name': 'd-123a-1'})
    response = client.get(url_for('main.arrival_slip', dewar_name='d-123a-1'))
    page = BeautifulSoup(response.data, 'html.parser')
    filled_data = load_qrcode(decode_img(page.find(id='filled_code').img))
    assert filled_data['type'] == 'DEWAR_FILLED'
    departed_data = load_qrcode(decode_img(page.find(id='departed_code').img))
    assert departed_data['type'] == 'SET_DEWAR_OFFSITE'


@vcr.use_cassette()
def test_arrival_slip_fits_on_one_page(running_app, db):
    db.clear()
    db.add_dewar({
        'name': 'd-123a-1',
        'owner': 'Jane',
        'department': 'Chemistry',
        'institute': 'Some University',
        'streetAddress': '123 Main Road',
        'city': 'Brisbane',
        'state': 'Queensland',
        'postcode': '3000',
        'country': 'Australia',
        'phone': '111-222-333',
        'email': 'jane@example.com',
        'epn': '123a',
        'returnDewar': True,
        'courier': 'Fast Deliveries',
        'courierAccount': '999',
        'container_type': 'pucks',
        'expectedContainers': '1 | 2 | 3 | 4 | 5 |  |  | ',
    })
    url = url_for('main.arrival_slip', dewar_name='d-123a-1')
    with BytesIO() as file:
        page_to_pdf(url, file)
        reader = PdfFileReader(file)
        assert reader.numPages == 1


@vcr.use_cassette()
def test_arrival_ship_shows_courier_none_if_field_is_empty(client, db):
    db.clear()
    db.add_dewar({'name': 'd-123a-1', 'courier': ''})
    response = client.get(url_for('main.arrival_slip', dewar_name='d-123a-1'))
    page = BeautifulSoup(response.data, 'html.parser')
    assert page.find(id='courier').text == 'Using courier: none'
    assert page.find(id='courier_account').text == 'With account number: none'
