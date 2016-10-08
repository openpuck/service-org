#!/usr/bin/env python

from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import clear_table

table_name = "conferences"
clear_table(conn, table_name)

ConfByLeagueGenderIndex = GlobalAllIndex("ConfByLeagueGender",
                                         parts=[
                                             HashKey("league"),
                                             RangeKey("is_women")
                                         ],
                                         throughput={
                                             'read': 1,
                                             'write': 1
                                         })

ConfAbbrIndex = GlobalAllIndex("ConfByAbbrGender",
                           parts=[
                               HashKey("abbr"),
                               RangeKey("is_women")
                           ],
                           throughput={
                               'read': 1,
                               'write': 1
                           })

new_table = Table.create(table_name,
                         schema=[
                             HashKey("id")
                         ],
                         throughput={
                             'read': 1,
                             'write': 1
                         },
                         global_indexes=[
                             ConfByLeagueGenderIndex,
                             ConfAbbrIndex
                         ],
                         connection=conn)

print "Created '%s' table" % table_name
