#!/bin/bash

# Common Stuff
CURL="curl -v -H 'Content-Type: application/json'"

# Method-specific configuration
URL="https://mkvusbh1l7.execute-api.us-east-1.amazonaws.com/dev/league"
METHOD="POST"
PAYLOAD='{"abbr": "FOOBAR", "name": "foobar", "website": "lolz"}'

# Execute
eval ${CURL} -X ${METHOD} ${URL} -d \'${PAYLOAD}\' | json_pp