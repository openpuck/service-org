#!/usr/bin/env python

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import create_table_obj

table_name = 'seasons'
Seasons = create_table_obj(conn, table_name)

print "Straight Query"
print dict(Seasons.get_item(id='c33f5d78-34db-4ee4-aa63-1d8c9997adc2'))

print "SeasonByLeagueGender Query"
for entry in Seasons.query(index='SeasonByLeagueGender', league__eq="ac99003b-845d-4cec-9c02-4dfe1acc1839", is_women__eq="yes"):
    print dict(entry)

print "SeasonByLeagueStart Query"
for entry in Seasons.query(index='SeasonByLeagueStart', league__eq="ac99003b-845d-4cec-9c02-4dfe1acc1839", start_year__eq=2016):
    print dict(entry)
