#!/usr/bin/env python3
import os
import json
import shlex

# Imports for easy eval
from math import *

TRIGGER = 'py'

op = os.environ.get('ALBERT_OP')

if op == 'METADATA':
    print(json.dumps({
      'iid': 'org.albert.extension.external/v2.0',
      'version': '1.0',
      'name': 'Python eval',
      'trigger': TRIGGER,
      'author': 'Asger Hautop Drewsen',
      'dependencies': [],
    }))
elif op == 'QUERY':
    query = os.environ.get('ALBERT_QUERY')
    if query.startswith(TRIGGER):
        query = query[len(TRIGGER):]

    try:
        result = eval(query)
        success = True
    except Exception as e:
        result = 'Error: %s' % e
        success = False

    result = str(result)

    item = {
        'id': 'result',
        'name': result,
        'description': 'Result',
        'icon': 'accessories-calculator',
        'actions': []
    }

    copy_action = {
        'name': 'Copy to clipboard',
        'command': 'sh',
        'arguments': ['-c', 'echo -n %s | xclip -i -selection clipboard' % shlex.quote(result)]
    }

    if success:
        item['actions'].append(copy_action)

    print(json.dumps({'items': [item]}))
