from __future__ import print_function

import json
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# this adds the component-level `lib` directory to the Python import path
import sys, os
# get this file's directory independent of where it's run from
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
sys.path.append(os.path.join(here, "../vendored"))

# import the shared library, now anything in component/lib/__init__.py can be
# referenced as `lib.something`
import lib
from boto3.dynamodb.conditions import Key


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    # Tables
    teams_table = lib.get_table(lib.TEAMS_TABLE)

    # Query
    institution_id = event['institution']
    is_women = event['is_women']

    try:
        # You have to use == or Python gets stupid.
        if institution_id == "" or is_women == "":
            return lib.get_json(teams_table.scan()['Items'])
        else:
            team_results = teams_table.query(
                IndexName='TeamsByInstitutionGender',
                KeyConditionExpression=Key('institution').eq(institution_id) & Key(
                    'is_women').eq(is_women)
            )
            if len(team_results['Items']) < 1:
                raise lib.exceptions.NotFoundException(
                    "Teams of institution '%s' and is_women '%s' not found." % (
                        institution_id, is_women))
            return lib.get_json(team_results['Items'])

    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)