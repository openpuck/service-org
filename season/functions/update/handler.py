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
    required_keys = ['cn', 'is_women', 'abbr', 'website', 'league']
    lib.validation.check_keys(required_keys, event)
    lib.validation.check_keys(['pathId'], event, False)

    # Update
    try:
        response = lib.ConferencesTable.update_item(
            Key={
                'id': event['pathId']
            },
            UpdateExpression="set abbr = :abbr, cn = :cn, website = :website, is_women = :is_women, league = :league",
            ExpressionAttributeValues={
                ':abbr': event['body']['abbr'],
                ':cn': event['body']['cn'],
                ':website': event['body']['website'],
                ':is_women': event['body']['is_women'],
                ':league': event['body']['league']
            },
            ReturnValues="ALL_NEW"
        )
    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)

    # Return
    return lib.get_json(response['Attributes'])
