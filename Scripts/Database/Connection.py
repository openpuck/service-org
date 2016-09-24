from boto.dynamodb2.table import Table
from boto.dynamodb2.layer1 import DynamoDBConnection
import time
from boto.exception import JSONResponseError

localconn = DynamoDBConnection(host='localhost', port=8000, aws_access_key_id='dummy', aws_secret_access_key='dummy', is_secure=False)
remoteconn = DynamoDBConnection()

Teams = Table('teams', connection=localconn)
ScheduleEntries = Table('schedule_entries', connection=localconn)
TeamAltnames = Table('team_altnames', connection=localconn)
Seasons = Table('seasons', connection=localconn)
SeasonPhases = Table('season_phases', connection=localconn)
Locations = Table('locations', connection=localconn)
LocationAltnames = Table('location_altnames', connection=localconn)


def clear_table(conn, table_name):
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


def ready_table(conn, table_name):
    try:
        our_table = Table(table_name, connection=conn)
        if our_table.describe()['Table']['TableStatus'] == "CREATING":
            while our_table.describe()['Table']['TableStatus'] == "CREATING":
                print "Waiting for CREATING to be done..."
                time.sleep(1)
            print "Table is done."
        else:
            print "Table is ready."
    except JSONResponseError:
        print "Table '%s' does not exist." % table_name


def create_table_obj(conn, table_name):
    ready_table(conn, table_name)
    MyTable = Table(table_name, connection=conn)
    MyTable.use_boolean()
    return MyTable
