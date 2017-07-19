#!/usr/bin/env python3
import os
import json
import shlex
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

TRIGGER = 'pass '

op = os.environ.get('ALBERT_OP')

if op == 'METADATA':
    print(json.dumps({
        'iid': 'org.albert.extension.external/v2.0',
        'version': '1.0',
        'name': 'Pass',
        'trigger': TRIGGER,
        'author': 'Asger Hautop Drewsen',
        'dependencies': [],
    }))
elif op == 'QUERY':
    query = os.environ.get('ALBERT_QUERY')
    if query.startswith(TRIGGER):
        query = query[len(TRIGGER):]

    query = query.strip()

    names = []
    for p in sorted(Path.home().glob('.password-store/**/*.gpg')):
        full_relative_name = p.relative_to(os.path.join(Path.home()), '.password-store')
        name, ext = os.path.splitext(full_relative_name)
        if name.lower().find(query.lower()) != -1:
            names.append(name)

    items = []
    for name in names:
        copy_action = {
            'name': 'Copy to clipboard',
            'command': 'pass',
            'arguments': ['show', '-c', name]
        }

        items.append({
            'id': 'result',
            'name': name,
            'description': 'Copy password to clipboard',
            'icon': 'gcr-password',
            'actions': [copy_action]
        })

    print(json.dumps({'items': items}))
