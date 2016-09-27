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
        result = lib.SeasonsTable.query(
            IndexName='SeasonByLeagueGender',
            KeyConditionExpression=Key('league').eq(event['pathId'])
        )
        return lib.get_json(result['Items'])
    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)
