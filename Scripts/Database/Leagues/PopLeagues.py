#!/usr/bin/env python

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import create_table_obj

table_name = 'leagues'
Leagues = create_table_obj(conn, table_name)

Leagues.put_item(data={
    'id': '00b89928-f9e0-4f8e-a066-4983e02150ec',
    'abbr': 'NHL',
    'name': 'National Hockey League',
    'website': 'https://www.nhl.com/',
}, overwrite=True)

Leagues.put_item(data={
    'id': 'ac99003b-845d-4cec-9c02-4dfe1acc1839',
    'abbr': 'NCAA',
    'name': 'National Collegiate Athletic Association',
    'website': 'http://www.ncaa.com/',
}, overwrite=True)

Leagues.put_item(data={
    'id': '3390d8ef-7b4a-4959-a014-da1274927a99',
    'abbr': 'NWHL',
    'name': 'National Womens Hockey League',
    'website': 'http://nwhl.co/',
}, overwrite=True)

Leagues.put_item(data={
    'id': 'cb6732b1-7702-4371-973f-22c234bf485a',
    'abbr': 'CWHL',
    'name': 'Canadian Womens Hockey League',
    'website': 'http://cwhl.ca/view/cwhl',
}, overwrite=True)

entries = Leagues.scan()
for entry in entries:
    print dict(entry)
