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


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))
    # return event

    # Query
    search_cn = event['cn']
    if search_cn != "":
        try:
            entries = []
            result = lib.InstitutionsTable.scan()
            for result in result['Items']:
                if result['cn'] == search_cn:
                    entries.append(result)
            if len(entries) >= 1:
                return lib.get_json(entries)

            raise lib.exceptions.NotFoundException("Institution '%s' not found." % search_cn)
        except lib.exceptions.ClientError as ce:
            raise lib.exceptions.InternalServerException(ce.message)

    # Return
    try:
        return lib.get_json(lib.InstitutionsTable.scan()['Items'])
    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)
