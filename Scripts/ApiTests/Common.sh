#!/bin/bash

DEBUG=0
if [[ ${DEBUG} == 1 ]]; then
    DEBUG_OPTS="-v"
else
    DEBUG_OPTS=""
fi
# Common Stuff
CURL="curl -s ${DEBUG_OPTS} -H 'Content-Type: application/json'"

# Method-specific configuration
URL="https://mkvusbh1l7.execute-api.us-east-1.amazonaws.com/dev"