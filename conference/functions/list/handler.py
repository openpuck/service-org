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
    league_abbr = event['league_abbr']
    conf_abbr = event['conf_abbr']
    is_women = event['is_women']

    try:
        # You have to use == or Python gets stupid.
        if league_abbr == "" or conf_abbr == "" or is_women == "":
            return lib.get_json(lib.ConferencesTable.scan()['Items'])
        else:
            # Query for the leagues matching the abbr given.
            league_result = lib.LeaguesTable.query(
                IndexName='AbbrIndex',
                KeyConditionExpression=Key('abbr').eq(league_abbr)
            )
            if league_result['Count'] is 0:
                raise lib.exceptions.NotFoundException(
                    "Abbreviated league '%s' not found." % league_abbr)

            # Now find the conference.
            for league in league_result['Items']:
                conf_result = lib.ConferencesTable.query(
                    IndexName='ConfByLeagueGender',
                    KeyConditionExpression=Key('league').eq(league['id'])
                )
                entries = []
                for conf in conf_result['Items']:
                    if conf['abbr'] == conf_abbr and conf['is_women'] == is_women:
                        entries.append(conf)
                if len(entries) >= 1:
                    return lib.get_json(conf)
                raise lib.exceptions.NotFoundException("Conference '%s' not found for league '%s' with is_women='%s'." % (conf_abbr, league_abbr, is_women))
            # return lib.get_json(league_result['Items'])
    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)
