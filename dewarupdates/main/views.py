from flask import request, render_template, current_app, abort, jsonify, url_for
import requests
import json
from . import main
from .. import printer
from ..utils import dewar_filled_payload, dewar_departed_payload


def print_arrival_slip(dewar_name):
    url = url_for('.arrival_slip', dewar_name=dewar_name, _external=True)
    printer.print_page(url)


@main.route('/actions', methods=['POST'])
def actions():
    request.get_json(force=True)
    action = request.json
    if action['type'] == 'UPDATE_DEWAR' and action['update'].get('onsite'):
        print_arrival_slip(action['dewar'])
    else:
        return jsonify({'error': 'Unhandled action: %s' % action})
    return jsonify({'data': 'ok'})


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
