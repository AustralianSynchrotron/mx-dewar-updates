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


def test_can_load_index(client):
    response = client.get(url_for('main.index'))
    assert response.status_code == 200
