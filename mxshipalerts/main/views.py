from flask import render_template, current_app, abort
import requests
from . import main
from .. import printer


@main.route('/actions', methods=['POST'])
def actions():
    return 'Works!'


@main.route('/arrival-slip/<dewar_id>')
def arrival_slip(dewar_id):
    url = '%s/dewars/%s' % (current_app.config['PUCKTRACKER_URL'], dewar_id)
    response = requests.get(url)
    body = response.json()
    data = body.get('data')
    if body.get('error') or not data:
        abort(404)
    return render_template('arrival-slip.html', **data)
