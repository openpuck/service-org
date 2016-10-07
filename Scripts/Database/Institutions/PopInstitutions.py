#!/usr/bin/env python

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import create_table_obj, ready_table

table_name = 'institutions'
Institutions = create_table_obj(conn, table_name)

Institutions.put_item(data={
    'id': '05d7ab17-68e2-4cbe-ae3c-62bf908462bd',
    'cn': 'Rochester Institute of Technology',
    'city': 'Rochester'
}, overwrite=True)

Institutions.put_item(data={
    'id': 'b10fd78b-6e34-4f32-83a0-d4ae12700316',
    'cn': 'Boston Bruins',
    'city': 'Boston'
}, overwrite=True)

Institutions.put_item(data={
    'id': '52b48737-f854-44ed-bd71-dc96446ca280',
    'cn': 'National Womens Hockey League',
    'city': 'New York City'
}, overwrite=True)

Institutions.put_item(data={
    'id': '65058917-6137-4d0e-9cd2-c35ec55b2f1d',
    'cn': 'Bentley University',
    'city': 'Waltham'
}, overwrite=True)

entries = Institutions.scan()
for entry in entries:
    print dict(entry)
