#!/usr/bin/env python

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import create_table_obj

table_name = 'seasons'
Seasons = create_table_obj(conn, table_name)

Seasons.put_item(data={
    'id': 'c33f5d78-34db-4ee4-aa63-1d8c9997adc2',
    'is_women': 'yes',
    'league': 'NCAA',
    'start': 2016,
    'end': 2017,
}, overwrite=True)
Seasons.put_item(data={
    'id': '2cf593d7-ed56-4245-81c1-af174f364ef9',
    'is_women': 'yes',
    'league': 'NWHL',
    'start': 2016,
    'end': 2017,
}, overwrite=True)
Seasons.put_item(data={
    'id': '7f057832-7461-4520-9518-410d74e3a449',
    'is_women': 'no',
    'league': 'NHL',
    'start': 2016,
    'end': 2017,
}, overwrite=True)

entries = Seasons.scan()
for entry in entries:
    print dict(entry)
