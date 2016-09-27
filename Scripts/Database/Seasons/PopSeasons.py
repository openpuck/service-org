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
    'league': 'ac99003b-845d-4cec-9c02-4dfe1acc1839',
    'start_year': 2016,
    'end_year': 2017,
}, overwrite=True)
Seasons.put_item(data={
    'id': 'eededae4-8219-4ae5-8d46-04e339933ecb',
    'is_women': 'no',
    'league': 'ac99003b-845d-4cec-9c02-4dfe1acc1839',
    'start_year': 2015,
    'end_year': 2016,
}, overwrite=True)
Seasons.put_item(data={
    'id': '2cf593d7-ed56-4245-81c1-af174f364ef9',
    'is_women': 'yes',
    'league': '3390d8ef-7b4a-4959-a014-da1274927a99',
    'start_year': 2016,
    'end_year': 2017,
}, overwrite=True)
Seasons.put_item(data={
    'id': '00b89928-f9e0-4f8e-a066-4983e02150ec',
    'is_women': 'no',
    'league': 'NHL',
    'start_year': 2016,
    'end_year': 2017,
}, overwrite=True)

entries = Seasons.scan()
for entry in entries:
    print dict(entry)
