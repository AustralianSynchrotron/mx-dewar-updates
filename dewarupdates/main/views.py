import json

from flask import request, render_template, current_app, abort, jsonify, url_for
import requests
from dateutil.parser import parse as parse_datetime
from pytz import timezone

from . import main
from ..utils import dewar_filled_payload, dewar_departed_payload


def _convert_to_aest_str(dt_str):
    if dt_str is None:
        return dt_str
    dt = parse_datetime(dt_str)
    dt_aest = dt.astimezone(timezone('Australia/Melbourne'))
    return dt_aest.strftime('%Y-%m-%d %H:%M')


@main.route('/arrival-slip/<dewar_name>')
def arrival_slip(dewar_name):
    url = '%s/dewars/%s' % (current_app.config['PUCKTRACKER_URL'], dewar_name)
    response = requests.get(url)
    body = response.json()
    data = body.get('data')
    if body.get('error') or not data:
        abort(404)
    data['experimentStartTime'] = _convert_to_aest_str(data.get('experimentStartTime'))
    data['experimentEndTime'] = _convert_to_aest_str(data.get('experimentEndTime'))
    data['filled_payload'] = dewar_filled_payload(dewar_name)
    data['departed_payload'] = dewar_departed_payload(dewar_name)
    return render_template('arrival-slip.html', **data)
