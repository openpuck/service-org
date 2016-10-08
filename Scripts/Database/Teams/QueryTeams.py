#!/usr/bin/env python

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import create_table_obj

table_name = 'teams'
Teams = create_table_obj(conn, table_name)

print "Straight Query"
print dict(Teams.get_item(id='39162250-c85b-438d-a6ac-79e110f11c22'))

print "TeamsByInstitutionGender Query (Institution)"
for entry in Teams.query(index='TeamsByInstitutionGender', institution__eq="05d7ab17-68e2-4cbe-ae3c-62bf908462bd"):
    print dict(entry)

print "TeamsByInstitutionGender Query (Institution+Gender)"
for entry in Teams.query(index='TeamsByInstitutionGender', institution__eq="05d7ab17-68e2-4cbe-ae3c-62bf908462bd", is_women__eq="yes"):
    print dict(entry)
