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
import decimal


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    # Query
    league_id = event['league']
    start_year = event['start_year']
    is_women = event['is_women']

    try:
        # You have to use == or Python gets stupid.
        if league_id == "" or start_year == "":
            return lib.get_json(lib.SeasonsTable.scan()['Items'])
        else:
            # Now find the conference.
            # for league in league_result['Items']:
            season_result = lib.SeasonsTable.query(
                IndexName='SeasonByLeagueStart',
                KeyConditionExpression=Key('league').eq(league_id) & Key('start_year').eq(decimal.Decimal(start_year))
            )
            return_results = []
            for season in season_result['Items']:
                if season['is_women'] == is_women:
                    return_results.append(season)
            if return_results is not []:
                return lib.get_json(return_results)
            raise lib.exceptions.NotFoundException("Season starting '%i' not found for league '%s' with is_women='%s'." % (start_year, league_id, is_women))
    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)
