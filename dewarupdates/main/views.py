from flask import render_template, current_app, abort
import requests
import json
from . import main
from .. import printer
from ..utils import dewar_filled_payload, dewar_departed_payload


@main.route('/actions', methods=['POST'])
def actions():
    return 'Works!'


@main.route('/arrival-slip/<dewar_name>')
def arrival_slip(dewar_name):
    url = '%s/dewars/%s' % (current_app.config['PUCKTRACKER_URL'], dewar_name)
    response = requests.get(url)
    body = response.json()
    data = body.get('data')
    if body.get('error') or not data:
        abort(404)
    data['filled_payload'] = dewar_filled_payload(dewar_name)
    data['departed_payload'] = dewar_departed_payload(dewar_name)
    return render_template('arrival-slip.html', **data)
