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
    'institution': '05d7ab17-68e2-4cbe-ae3c-62bf908462bd',
    'provider': 'SidearmResponsiveProvider',
    'is_women': 'yes',
    'league': 'ac99003b-845d-4cec-9c02-4dfe1acc1839',
    'conference': 'LOLZTHISSOULDFAIL',
    'is_active': 'yes',
    'website': 'http://ritathletics.com/index.aspx?path=whock'
}, overwrite=True)

Teams.put_item(data={
    'id': '549a67e2-5b2e-4341-af28-75a9f6e9d092',
    'nickname': 'Tigers',
    'institution': '05d7ab17-68e2-4cbe-ae3c-62bf908462bd',
    'provider': 'SidearmResponsiveProvider',
    'is_women': 'no',
    'league': 'ac99003b-845d-4cec-9c02-4dfe1acc1839',
    'conference': 'LOLZTHISSOULDFAIL',
    'is_active': 'yes',
    'website': 'http://ritathletics.com/index.aspx?path=mhock'
}, overwrite=True)

Teams.put_item(data={
    'id': '3fe7bfbd-dfc2-47f8-940b-e7853fdf9550',
    'nickname': 'Huskies',
    'institution': 'LOLZNOPE',
    'provider': 'SidearmAdaptiveProvider',
    'is_women': 'yes',
    'league': 'ac99003b-845d-4cec-9c02-4dfe1acc1839',
    'conference': 'LOLZTHISSOULDFAIL',
    'is_active': 'yes',
    'website': 'http://gonuathletics.com/index.aspx?path=whock'
}, overwrite=True)

entries = Teams.scan()
for entry in entries:
    print dict(entry)
