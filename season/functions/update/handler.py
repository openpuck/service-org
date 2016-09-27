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


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    # Test for required attributes
    required_keys = ['id', 'is_women', 'league', 'start', 'end']
    lib.validation.check_keys(required_keys, event)

    # Validation
    lib.validation.check_boolean(event, ['is_women'])
    lib.validation.check_decimal(event, ['start', 'end'])

    # Relations
    lib.validation.check_relation(lib.LeaguesTable, 'id', event['body']['league'])

    # Update
    try:
        response = lib.SeasonsTable.update_item(
            Key={
                'id': event['pathId']
            },
            UpdateExpression="end = :end, is_women = :is_women, league = :league, start = :start",
            ExpressionAttributeValues={
                ':start': event['body']['start'],
                ':end': event['body']['end'],
                ':is_women': event['body']['is_women'],
                ':league': event['body']['league'],
            },
            ReturnValues="ALL_NEW"
        )
    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)

    # Return
    return lib.get_json(response['Attributes'])
