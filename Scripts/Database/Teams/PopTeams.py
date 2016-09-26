#!/usr/bin/env python

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import create_table_obj

table_name = 'teams'
Teams = create_table_obj(conn, table_name)

Teams.put_item(data={
    'id': '39162250-c85b-438d-a6ac-79e110f11c22',
    'nickname': 'Tigers',
    'institution': 'LOLZNOTIMPLEMENTEDYET',
    'provider': 'SidearmResponseiveProvider',
    'is_women': 'yes',
    'league': 'LOLZTHISSHOULDFAIL',
    'conference': 'LOLZTHISSOULDFAIL',
    'is_active': 'yes',
    'website': 'http://ritathletics.com/index.aspx?path=whock'
}, overwrite=True)

entries = Teams.scan()
for entry in entries:
    print dict(entry)
