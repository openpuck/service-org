#!/usr/bin/env python

import sys
import os
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from boto.dynamodb2.types import NUMBER
import time

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from Connection import remoteconn as conn

table_name = "teams"

try:
    teams_table = Table(table_name, connection=conn)
    if teams_table.describe()['Table']['TableStatus'] == "CREATING":
        while teams_table.describe()['Table']['TableStatus'] == "CREATING":
            print "Waiting for CREATING to be done..."
            time.sleep(1)
        print "Table is done."
    teams_table.delete()
    while teams_table.describe()['Table']['TableStatus'] == "DELETING":
        print "Waiting for DELETING to be done..."
        time.sleep(1)
    print "Table is done."

except JSONResponseError:
    print "Table '%s' does not exist." % table_name

ProviderIndex = GlobalAllIndex("ProviderIndex",
                               parts=[
                                   HashKey("provider"),
                                   RangeKey("is_women", data_type=NUMBER),
                               ],
                               throughput={
                                   'read': 1,
                                   'write': 1,
                               })

ConferenceIndex = GlobalAllIndex("ConferenceIndex",
                                 parts=[
                                     HashKey("home_conference"),
                                     RangeKey("is_women", data_type=NUMBER),
                                 ],
                                 throughput={
                                     'read': 1,
                                     'write': 1,
                                 })

tble = Table.create(table_name,
                    schema=[
                        HashKey("id")
                    ],
                    throughput={
                        'read': 1,
                        'write': 1
                    },
                    global_indexes=[
                        ConferenceIndex,
                        ProviderIndex,
                    ],
                    connection=conn)

print "Created '%s' table" % table_name
