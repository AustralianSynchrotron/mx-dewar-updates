import json


def dewar_filled_payload(dewar_name):
    return json.dumps({
      'type': 'DEWAR_FILLED',
      'dewar': dewar_name,
    })


def dewar_departed_payload(dewar_name):
    return json.dumps({
      'type': 'SET_DEWAR_OFFSITE',
      'dewar': dewar_name,
    })
