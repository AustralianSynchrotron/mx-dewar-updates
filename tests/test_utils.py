from mxshipalerts import utils
import json


def test_dewar_filled_payload():
    payload = utils.dewar_filled_payload('d-123a-1')
    data = json.loads(payload)
    assert data['type'] == 'DEWAR_FILLED'
    assert data['dewar'] == 'd-123a-1'


def test_dewar_departed_payload():
    payload = utils.dewar_departed_payload('d-123a-1')
    data = json.loads(payload)
    assert data['type'] == 'SET_DEWAR_OFFSITE'
    assert data['dewar'] == 'd-123a-1'
