#!/usr/bin/env python

from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table

import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn
from Connection import clear_table

table_name = "teams"
clear_table(conn, table_name)

TeamsByInstitutionGender = GlobalAllIndex("TeamsByInstitutionGender",
                           parts=[
                               HashKey("institution"),
                               RangeKey("is_women")
                           ],
                           throughput={
                               'read': 1,
                               'write': 1,
                           })
TeamsByLeagueGender = GlobalAllIndex("TeamsByLeagueGender",
                                          parts=[
                                              HashKey("league"),
                                              RangeKey("is_women")
                                          ],
                                          throughput={
                                              'read': 1,
                                              'write': 1,
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
                             TeamsByInstitutionGender,
                             TeamsByLeagueGender
                         ],
                         connection=conn)

print "Created '%s' table" % table_name
