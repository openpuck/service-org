#!/usr/bin/env python

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import create_table_obj

table_name = 'institutions'
Institutions = create_table_obj(conn, table_name)

print "Straight Query"
print dict(Institutions.get_item(id='05d7ab17-68e2-4cbe-ae3c-62bf908462bd'))
