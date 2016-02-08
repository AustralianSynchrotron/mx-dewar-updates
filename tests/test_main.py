from mxshipalerts import create_app
from flask import url_for
import pytest
from bs4 import BeautifulSoup
import responses


@pytest.yield_fixture
def client():
    app = create_app('testing')
    context = app.app_context()
    context.push()
    yield app.test_client()
    context.pop()


def test_post_dewar_arrival_to_actions(client, monkeypatch):
    data = {
        'type': 'UPDATE_DEWAR',
        'dewar': '1',
        'onsite': True,
    }
    response = client.post(url_for('main.actions'), data=data)
    assert response.status_code == 200


@responses.activate
def test_get_dewar_arrival_page(client):
    responses.add('GET', 'http://pucktracker-test/dewars/d-123a-1', json={
        'data': {
            'owner': 'Jane',
            'department': 'Chemistry',
            'institute': 'Some University',
            'street_address': '123 Main Road',
            'city': 'Brisbane',
            'state': 'Queensland',
            'postcode': '3000',
            'country': 'Australia',
            'phone': '111-222-333',
            'email': 'jane@example.com',
            'epn': '123a',
            'return_dewar': True,
            'courier': 'Fast Deliveries',
            'courier_account': '999',
            'container_type': 'pucks',
            'pucks': ['1', '2', '3', '', '4', '5', '', '', ''],
        }
    })
    response = client.get(url_for('main.arrival_slip', dewar_id='d-123a-1'))
    assert response.status_code == 200
    page = BeautifulSoup(response.data, 'html.parser')
    assert 'MX dewar shipment information' in page.text
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
    assert 'User wants samples returned by courier' in page.text
    assert 'Fast Deliveries' in page.find(id='courier').text
    assert '999' in page.find(id='courier_account').text


@responses.activate
def test_arrival_slip_returns_404_when_dewar_doesnt_exist(client):
    responses.add('GET', 'http://pucktracker-test/dewars/not-a-dewar',
                  json={'error': 'Not found'})
    response = client.get(url_for('main.arrival_slip', dewar_id='not-a-dewar'))
    assert response.status_code == 404
