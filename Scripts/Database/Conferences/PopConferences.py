#!/usr/bin/env python

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import create_table_obj, ready_table

table_name = 'conferences'
Conferences = create_table_obj(conn, table_name)

Conferences.put_item(data={
    'id': '39162250-c85b-438d-a6ac-79e110f11c22',
    'abbr': 'WHEA',
    'cn': 'Hockey East Association',
    'is_women': "yes",
    'website': 'http://hockeyeastonline.com/women/index.php',
    'league': 'ac99003b-845d-4cec-9c02-4dfe1acc1839'
}, overwrite=True)

Conferences.put_item(data={
    'id': '13e76ddb-3dd4-42fd-b058-6b43bb88b77e',
    'abbr': 'HEA',
    'cn': 'Hockey East Association',
    'is_women': "no",
    'website': 'http://hockeyeastonline.com/men/index.php',
    'league': 'ac99003b-845d-4cec-9c02-4dfe1acc1839'
}, overwrite=True)

Conferences.put_item(data={
    'id': 'f6c4f13f-52b6-4f68-8419-b4988da5d4ea',
    'abbr': 'NHLE',
    'cn': 'Eastern',
    'is_women': "no",
    'website': None,
    'league': '00b89928-f9e0-4f8e-a066-4983e02150ec'
}, overwrite=True)

Conferences.put_item(data={
    'id': 'f550d8ed-bc80-407a-be09-ee1b85ba3bca',
    'abbr': 'WCHA',
    'cn': 'Western Collegiate Hockey Association',
    'is_women': "yes",
    'website': 'http://www.wcha.com/men/index.php',
    'league': 'ac99003b-845d-4cec-9c02-4dfe1acc1839'
}, overwrite=True)

entries = Conferences.scan()
for entry in entries:
    print dict(entry)
