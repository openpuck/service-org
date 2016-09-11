#!/usr/bin/env python

import sys
import os
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from boto.dynamodb2.types import NUMBER

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn


table_name = "seasons"

try:
    teams_table = Table(table_name, connection=conn)
    teams_table.delete()
except JSONResponseError:
    print "Table '%s' does not exist." % table_name

tble = Table.create(table_name,
                    schema=[
                        HashKey("id")
                    ],
                    throughput={
                        'read': 1,
                        'write': 1
                    },
                    global_indexes=[
                    ],
                    connection=conn)

print "Created '%s' table" % table_name
