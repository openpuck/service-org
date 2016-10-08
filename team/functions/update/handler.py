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
    lib.validation.check_keys(['pathId'], event, False)

    required_keys = ['id', 'nickname', 'institution', 'provider', 'is_women',
                     'league', 'conference', 'is_active', 'website']
    lib.validation.check_keys(required_keys, event)

    # Validation
    lib.validation.check_boolean(event, ['is_women', 'is_active'])

    # Relations
    lib.validation.check_relation(lib.LeaguesTable, 'id',
                                  event['body']['league'])
    lib.validation.check_relation(lib.ConferencesTable, 'id',
                                  event['body']['conference'])
    lib.validation.check_relation_attr(lib.ConferencesTable, 'id',
                                       event['body']['conference'], 'is_women',
                                       event['body']['is_women'])
    lib.validation.check_relation_attr(lib.ConferencesTable, 'id',
                                       event['body']['conference'], 'league',
                                       event['body']['league'])

    # Update
    response = lib.perform_update(table=lib.TeamsTable, event=event,
                                  keys=required_keys)

    # Return
    return lib.get_json(response)
