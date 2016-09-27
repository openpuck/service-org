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
from boto3.dynamodb.conditions import Key, Attr


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    # Query
    # search_abbr = event['abbr']
    # if search_abbr != "":
    #     try:
    #         result = lib.LeaguesTable.query(
    #             IndexName='AbbrIndex',
    #             KeyConditionExpression=Key('abbr').eq(search_abbr)
    #         )
    #         if result['Count'] is 0:
    #             raise lib.exceptions.NotFoundException(
    #                 "Abbreviated league '%s' not found." % search_abbr)
    #         # This will only return the first result. Pretty sure leagues
    #         # wont be duplicated.
    #         return lib.get_json(result['Items'][0])
    #     except lib.exceptions.ClientError as ce:
    #         raise lib.exceptions.InternalServerException(ce.message)

    # Regular Return
    try:
        return lib.get_json(lib.SeasonsTable.scan()['Items'])
    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)
