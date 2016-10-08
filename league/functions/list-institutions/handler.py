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
    lib.validation.check_keys(['pathId'], event, False)

    try:
        institutions = []
        # Get Teams
        teams_result = lib.TeamsTable.query(
            IndexName='TeamsByLeagueGender',
            KeyConditionExpression=Key('league').eq(event['pathId'])
        )
        # Foreach team in the league, grab it's institution object
        for team in teams_result['Items']:
            institution_result = lib.InstitutionsTable.get_item(
                Key={'id': team['institution']})
            # Check if the league is already there
            if not institutions:
                institutions.append(institution_result['Item'])
            else:
                for institution in institutions:
                    if institution['id'] != institution_result['Item']['id']:
                        institutions.append(institution_result['Item'])
        # Done
        return lib.get_json(institutions)
    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)
