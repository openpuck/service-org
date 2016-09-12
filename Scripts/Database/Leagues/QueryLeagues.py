#!/usr/bin/env python

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import create_table_obj

table_name = 'leagues'
Leagues = create_table_obj(conn, table_name)

print "Straight Query"
print dict(Leagues.get_item(id='00b89928-f9e0-4f8e-a066-4983e02150ec'))

print "AbbrIndex Query"
for entry in Leagues.query(index='AbbrIndex', abbr__eq="NCAA"):
    print dict(entry)
