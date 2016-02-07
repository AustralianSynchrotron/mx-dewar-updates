from mxshipalerts import create_app
from flask import url_for
import pytest


@pytest.yield_fixture
def client():
    app = create_app('testing')
    context = app.app_context()
    context.push()
    yield app.test_client()
    context.pop()


def test_post_dewar_arrival_to_actions(client):
    data = {
        'type': 'UPDATE_DEWAR',
        'dewar': '1',
        'onsite': True,
    }
    response = client.post(url_for('main.actions'), data=data)
    assert response.status_code == 200
