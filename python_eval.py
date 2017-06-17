#!/usr/bin/env python3
import os
import json
import shlex

# Imports for easy eval
from math import *

# math.pow doesn't support a 3rd argument
from builtins import pow

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

    query = query.strip()

    if query:
        try:
            result = eval(query)
            success = True
        except Exception as e:
            result = e
            success = False
        description = type(result).__name__
    else:
        result = ''
        description = 'Type a python expression'
        success = False

    result = str(result)
    description = str(description)

    item = {
        'id': 'result',
        'name': result,
        'description': description,
        'icon': 'albert-python-evaluate.svg',
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
