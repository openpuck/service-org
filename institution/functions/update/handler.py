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
    required_keys = ['id', 'cn', 'city']
    lib.validation.check_keys(required_keys, event)

    # Validation
    # @TODO: Name not in use

    # Relations

    # Update
    response = lib.perform_update(table=lib.InstitutionsTable, event=event,
                                  keys=required_keys)

    # Return
    return lib.get_json(response)
