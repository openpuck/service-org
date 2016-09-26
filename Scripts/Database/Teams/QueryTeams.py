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
