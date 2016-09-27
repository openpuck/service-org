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
