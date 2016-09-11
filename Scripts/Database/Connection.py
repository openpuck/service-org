from boto.dynamodb2.table import Table
from boto.dynamodb2.layer1 import DynamoDBConnection

localconn = DynamoDBConnection(host='localhost', port=8000, aws_access_key_id='dummy', aws_secret_access_key='dummy', is_secure=False)
remoteconn = DynamoDBConnection()

Teams = Table('teams', connection=localconn)
ScheduleEntries = Table('schedule_entries', connection=localconn)
TeamAltnames = Table('team_altnames', connection=localconn)
Seasons = Table('seasons', connection=localconn)
SeasonPhases = Table('season_phases', connection=localconn)
Locations = Table('locations', connection=localconn)
LocationAltnames = Table('location_altnames', connection=localconn)