#!/usr/bin/env python3
import os
import json
import shlex
import subprocess
from tempfile import NamedTemporaryFile

TRIGGER = 'mma '

op = os.environ.get('ALBERT_OP')

if op == 'METADATA':
    print(json.dumps({
      'iid': 'org.albert.extension.external/v2.0',
      'version': '1.0',
      'name': 'Mathematica eval',
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
        with NamedTemporaryFile() as f:
            f.write(bytes(query, 'utf-8'))
            f.flush()
            output = subprocess.check_output(['wolframscript', '-print', '-f', f.name])
        result = str(output.strip(), 'utf-8')
        success = True
        description = 'Result'
    else:
        result = ''
        description = 'Type a mathematica expression'
        success = False

    item = {
        'id': 'result',
        'name': result,
        'description': description,
        'icon': 'wolfram-mathematica.png',
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
