#!/usr/bin/env python

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import create_table_obj

table_name = 'conferences'
Conferences = create_table_obj(conn, table_name)

print "Straight Query"
print dict(Conferences.get_item(id='39162250-c85b-438d-a6ac-79e110f11c22'))

print "ConfByLeagueGender Query (league)"
for entry in Conferences.query(index='ConfByLeagueGender', league__eq="ac99003b-845d-4cec-9c02-4dfe1acc1839"):
    print dict(entry)

print "ConfByLeagueGender Query (league+gender)"
for entry in Conferences.query(index='ConfByLeagueGender', league__eq="ac99003b-845d-4cec-9c02-4dfe1acc1839", is_women__eq="yes"):
    print dict(entry)
