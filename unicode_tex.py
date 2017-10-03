#!/usr/bin/env python3
import os
import json
import shlex
import re
import unicodedata
from pylatexenc.latex2text import LatexNodes2Text

COMBINING_LONG_SOLIDUS_OVERLAY = '\u0338'

TRIGGER = 'tex '

op = os.environ.get('ALBERT_OP')

if op == 'METADATA':
    print(json.dumps({
        'iid': 'org.albert.extension.external/v3.0',
        'version': '1.0',
        'name': 'TeX to unicode',
        'trigger': TRIGGER,
        'author': 'Asger Hautop Drewsen',
        'dependencies': [],
    }))
elif op == 'QUERY':
    query = os.environ.get('ALBERT_QUERY')
    if query.startswith(TRIGGER):
        query = query[len(TRIGGER):]

    query = query.strip()

    success = False
    if query:
        if not query.startswith('\\'):
            query = '\\' + query

        # Remove double backslashes (newlines)
        query = query.replace('\\\\', ' ')

        # pylatexenc doesn't support \not
        query = query.replace('\\not', '@NOT@')

        # pylatexenc doesn't backslashes at end of string
        if not query.endswith('\\'):
            n = LatexNodes2Text()
            result = n.latex_to_text(query)
            if result:
                result = unicodedata.normalize('NFC', result)
                result = re.sub(r'@NOT@\s*(\S)', '\\1' + COMBINING_LONG_SOLIDUS_OVERLAY, result)
                result = result.replace('@NOT@', '')
                result = unicodedata.normalize('NFC', result)
                success = True
                description = 'Result'

    if not success:
        result = query
        description = 'Type some TeX math'
        success = False

    item = {
        'id': 'result',
        'name': result,
        'description': description,
        'icon': '',
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
