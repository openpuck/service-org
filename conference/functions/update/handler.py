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
import lib
import lib.conferences as conferences


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    response = conferences.perform_update(event)

    # Return
    return lib.get_json(response)
