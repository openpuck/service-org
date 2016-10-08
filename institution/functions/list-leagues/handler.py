from __future__ import print_function

import json
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# this adds the component-level `lib` directory to the Python import path
import sys, os
# get this file's directory independent of where it's run from
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../"))
sys.path.append(os.path.join(here, "../../vendored"))

# import the shared library, now anything in component/lib/__init__.py can be
# referenced as `lib.something`
import lib
from boto3.dynamodb.conditions import Key

def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    # Test for required attributes
    if 'pathId' not in event:
        raise lib.exceptions.BadRequestException("Key 'id' is missing.")
    if event['pathId'] == "":
        raise lib.exceptions.BadRequestException("Key 'id' is missing.")

    try:
        leagues = []
        # Get Teams
        teams_result = lib.TeamsTable.query(
            IndexName='TeamsByInstitutionGender',
            KeyConditionExpression=Key('institution').eq(event['pathId'])
        )
        # Foreach team, grab it's league object
        for team in teams_result['Items']:
            league_response = lib.LeaguesTable.get_item(
                Key={'id': team['league']})
            # Check if the league is already there
            if not leagues:
                leagues.append(league_response['Item'])
            else:
                for league in leagues:
                    if league['id'] != league_response['Item']['id']:
                        leagues.append(league_response['Item'])
        # Done
        return lib.get_json(leagues)
    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)
