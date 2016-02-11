from dewarupdates import create_app
from flask import url_for, current_app
import pytest
import requests
from threading import Thread


@pytest.yield_fixture
def app():
    app = create_app('testing')
    context = app.app_context()
    context.push()
    yield app
    context.pop()


@pytest.yield_fixture
def client(app):
    yield app.test_client()


@pytest.yield_fixture
def running_app(app):
    thread = Thread(target=app.run)
    thread.daemon = True
    thread.start()
    yield app



@pytest.yield_fixture
def db():
    yield PuckTracker()


class PuckTracker():
    @property
    def actions_url(self):
        return '%s/actions' % current_app.config['PUCKTRACKER_URL']

    def clear(self):
        requests.post(self.actions_url, json={'type': 'REMOVE_ALL'})

    def add_dewar(self, dewar):
        requests.post(self.actions_url, json={
            'type': 'ADD_DEWAR',
            'dewar': dewar,
        })
